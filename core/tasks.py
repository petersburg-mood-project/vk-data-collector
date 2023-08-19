import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from django.db import transaction
from core.models import ParsingQueue, Community, Post, Comment
from core.clients.clients import get_group_info, get_posts, get_comments


def parse_queue_items():
    # Выбираем первые 5 непроцессированных объектов из очереди
    items_to_parse = list(ParsingQueue.objects.filter(status=ParsingQueue.NEW)[:5].all())
    (
        ParsingQueue
        .objects
        .filter(id__in=[v.id for v in items_to_parse])
        .update(status=ParsingQueue.IN_PROGRESS)
    )

    objects_to_create = defaultdict(list)

    for item in items_to_parse:
        try:
            if item.object_type == 'community':
                parse_community(item, objects_to_create)
            elif item.object_type == 'post':
                parse_post(item, objects_to_create)
            elif item.object_type == 'comment':
                parse_comment(item, objects_to_create)
            item.status = ParsingQueue.FINISHED
        except Exception as e:
            print(e)
            item.status = ParsingQueue.ERROR
            continue

    ParsingQueue.objects.bulk_update(items_to_parse, fields=["object_id", "status"])

    with transaction.atomic():
        for model_class, objs in objects_to_create.items():
            model_class.objects.bulk_create(objs)


def parse_community(item, objects_to_save):
    group_id = item.object_id.strip("/").split('/')[-1]
    group_info = get_group_info(group_id)

    # Создаем и сохраняем объект Community
    community = Community.objects.filter(link=item.object_id)
    community.update(**{
        "vk_id": group_info['id'],
        "link": f"https://vk.com/{group_info['screen_name']}",
        "title": group_info["name"],
        "icon": group_info["photo_200"],
        "subscribers_count": group_info["members_count"],
    })
    item.object_id = group_info["id"]

    for offset in range(0, 1000, 100):  # Пример: парсим 1000 постов с шагом 100
        parsing_item = ParsingQueue(
            object_type='post',
            object_id=group_info['id'],
            status=ParsingQueue.NEW,
            kwargs={'offset': offset, 'count': 100},
            parent=item,
        )
        objects_to_save[ParsingQueue].append(parsing_item)


def parse_post(item, objects_to_save):
    posts = get_posts(item.object_id, **(item.kwargs or {}))

    for post_json in posts:
        post = Post(
            vk_id=post_json["id"],
            owner=Community.objects.filter(vk_id=item.object_id).first(),
            reply_post_id=post_json.get("reply_post_id", None),
            date=datetime.datetime.fromtimestamp(post_json["date"]),
            likes_count=post_json["likes"]["count"],
            views_count=post_json["views"]["count"],
            text=post_json["text"]
        )
        objects_to_save[Post].append(post)

    for post in posts:
        parsing_item = ParsingQueue(
            object_type='comment',
            object_id=post['id'],
            status=ParsingQueue.NEW,
            kwargs={'offset': 0, 'count': 100},
            parent=item,
        )
        objects_to_save[ParsingQueue].append(parsing_item)


def parse_comment(item, objects_to_save):
    comments, profiles, groups = get_comments(
        item.parent.object_id,
        item.object_id,
        **(item.kwargs or {})
    )

    for comment_json in comments:
        comment = Comment(
            vk_id=comment_json['id'],
            from_id=comment_json['from_id'],
            post=Post.objects.filter(vk_id=item.object_id).first(),
            date=datetime.datetime.fromtimestamp(comment_json['date']),
            text=comment_json['text']
        )
        objects_to_save[Comment].append(comment)
