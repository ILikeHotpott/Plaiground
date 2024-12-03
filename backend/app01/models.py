from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random


class BaseUser(models.Model):
    """
    抽象用户模型，共享基础字段
    """
    username = models.CharField(max_length=50, unique=True)  # 用户名
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)  # 头像
    bio = models.TextField(max_length=500, blank=True, null=True)  # 简介
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        abstract = True  # 设置为抽象模型，不会创建数据库表

    def __str__(self):
        return self.username


class AIUser(BaseUser):
    ai_role = models.CharField(max_length=50, choices=[
        ('news', 'News Commentator'),
        ('tech', 'Tech Blogger'),
        ('daily', 'Daily Life Blogger'),
    ], default='daily')  # AI 用户角色

    model_type = models.CharField(max_length=50, choices=[
        ('gpt-4o-2024-11-20', 'GPT-4o-2024-11-20'),
    ], default='gpt-4o-2024-11-20')  # 生成内容使用的模型类型

    min_creation_frequency = models.IntegerField(default=1)  # 动态生成的最小间隔天数
    max_creation_frequency = models.IntegerField(default=5)  # 动态生成的最大间隔天数

    def generate_creation_frequency(self):
        """
        随机生成动态发布频率
        """
        return random.randint(self.min_creation_frequency, self.max_creation_frequency)

    def __str__(self):
        return f"AIUser: {self.username} ({self.ai_role})"


class Post(models.Model):
    """
    动态内容模型，支持文字和多媒体内容
    """
    user = models.ForeignKey('AIUser', on_delete=models.CASCADE, related_name="posts")  # 发布者，仅限 AI 用户
    text = models.TextField(blank=True, null=True)  # 动态文本内容
    created_at = models.DateTimeField(auto_now_add=True)  # 动态发布时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return f"Post by {self.user.username}: {self.text[:30]}"


class PostMedia(models.Model):
    """
    动态多媒体内容模型
    """
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")  # 关联动态
    file = models.FileField(upload_to="post_media/")  # 文件路径
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)  # 文件类型

    def __str__(self):
        return f"Media for Post {self.post.id}: {self.media_type}"


class HumanUser(BaseUser, AbstractUser):
    """
    真人用户模型，继承 Django 的用户认证功能
    """

    def __str__(self):
        return f"HumanUser: {self.username}"


class Comment(models.Model):
    """
    评论模型，支持 AI 和真人用户
    """
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 用户类型（HumanUser 或 AIUser）
    user_id = models.PositiveIntegerField()  # 用户 ID
    user = GenericForeignKey('user_type', 'user_id')  # 泛型外键
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # 关联动态
    text = models.TextField(max_length=500)  # 评论内容
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="replies")  # 父评论
    created_at = models.DateTimeField(auto_now_add=True)  # 评论时间

    def __str__(self):
        return f"Comment by {self.user.username}: {self.text[:30]}"


class Like(models.Model):
    """
    点赞模型，支持 AI 和真人用户
    """
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 用户类型
    user_id = models.PositiveIntegerField()  # 用户 ID
    user = GenericForeignKey('user_type', 'user_id')  # 泛型外键
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", blank=True, null=True)  # 关联动态
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", blank=True, null=True)  # 关联评论
    created_at = models.DateTimeField(auto_now_add=True)  # 点赞时间

    def __str__(self):
        if self.post:
            return f"{self.user.username} liked post {self.post.id}"
        if self.comment:
            return f"{self.user.username} liked comment {self.comment.id}"
