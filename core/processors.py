import datetime

from core.clients.clients import *
from core import models
from core.models import Community


def save_group_data(link: str, category: str, start_time: datetime.datetime):
    group_id = link.split('/')[-1]
    group_info = get_group_info(group_id)

    group = models.Community(**{
        "id": group_info['id'],
        "link": link,
        "title": group_info["name"],
        "icon": group_info["photo_200"],
        "category": category,
        "address": None,  # TODO
        "subscribers_count": group_info["members_count"],
        "stat_start_time": start_time
    })

    return group


def save_posts(group: Community, start_time: int):
    count = 100
    offset = 0

    while True:
        posts_json = get_posts(group.vk_id, offset, count)

        for post_json in posts_json:
            if post_json["date"] < start_time:
                break

            post = models.Post(
                id=post_json["id"],
                owner=group,
                reply_post_id=post_json.get("reply_post_id", None),
                date=datetime.datetime.fromtimestamp(post_json["date"]),
                likes_count=post_json["likes"]["count"],
                views_count=post_json["views"]["count"],
                text=post_json["text"]
            )
            post.save()  # TODO bulk save

            if post_json["comments"]["count"] != 0:
                save_comments(group_id, post.id)

        if len(posts_json) == 0 or posts_json[-1]["date"] < start_time:
            break

        offset += count


def save_comments(group_id: int, post_id: int):
    count = 100
    offset = 0

    post = models.Post.objects.get(pk=post_id)

    while True:
        comments_json, profiles_json, groups_json = get_comments(group_id, post_id, offset=offset, count=count)

        id_to_name = {0: None}
        id_to_name.update(map(lambda json: (json['id'], json['first_name'] + ' ' + json['last_name']), profiles_json))
        id_to_name.update(map(lambda json: (-json['id'], json['name']), groups_json))

        for comment_json in comments_json:
            comment = models.Comment(
                id=comment_json['id'],
                from_id=comment_json['from_id'],
                post=post,
                name=id_to_name[comment_json['from_id']],
                date=datetime.datetime.fromtimestamp(comment_json['date']),
                text=comment_json['text']
            )
            comment.save()

        if len(comments_json) < count:
            break

        offset += count
