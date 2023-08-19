from .utils import request_wrapper
from .exceptions import VkApiException


def get_posts(owner_id: int, offset: int = 0, count: int = 100):
    print(owner_id, offset, count)
    response = request_wrapper('wall.get', params={
        'owner_id': -int(owner_id),
        'offset': offset,
        'count': count
    })

    if "error" in response:
        raise VkApiException(response["error"])

    return response["response"]["items"]


def get_group_info(group_id: str):
    response = request_wrapper('groups.getById', params={
        'group_id': group_id,
        "fields": ["addresses", "members_count"]
    })

    if "error" in response:
        raise VkApiException(response["error"])

    return response["response"][0]


def get_comments(group_id: int, post_id: int, offset: int = 0, count: int = 100):
    response = request_wrapper('wall.getComments', params={
        'owner_id': -int(group_id),
        'post_id': post_id,
        'need_likes': 1,
        'extended': 1,
        'offset': offset,
        'count': count,
    })

    if "error" in response:
        raise VkApiException(response["error"])

    return response["response"]["items"], response["response"]["profiles"], response["response"]["groups"]
