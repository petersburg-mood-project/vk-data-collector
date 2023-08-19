from django.db import models


class Community(models.Model):
    vk_id = models.IntegerField(null=True, blank=True)  # TODO to vk_id
    title = models.TextField(blank=True)
    link = models.TextField()
    icon = models.TextField(blank=True)
    category = models.TextField()
    address = models.TextField(blank=True, null=True)
    subscribers_count = models.PositiveIntegerField(blank=True, null=True)
    stat_start_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        ParsingQueue.objects.get_or_create(
            object_id=self.link,
            object_type='community',
        )
        return super().save(*args, **kwargs)


class Post(models.Model):
    vk_id = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(Community, on_delete=models.CASCADE)
    reply_post_id = models.IntegerField(null=True)
    date = models.DateTimeField()
    likes_count = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField()
    text = models.TextField()


class Comment(models.Model):
    vk_id = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    from_id = models.IntegerField()
    name = models.TextField(null=True)
    date = models.DateTimeField()
    text = models.TextField()
    reply_to_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class ParsingQueue(models.Model):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    ERROR = "ERROR"

    STATUS_CHOICES = (
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (FINISHED, "Finished"),
        (ERROR, "Error"),
    )

    TYPE_CHOICES = (
        ('community', 'Community'),
        ('post', 'Post'),
        ('comment', 'Comment'),
    )

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.CharField(max_length=200)
    object_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    kwargs = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ParsingQueue[{self.id}, {self.status}] {self.object_type}"
