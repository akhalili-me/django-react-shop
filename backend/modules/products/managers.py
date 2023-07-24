from django.db import models
from django.shortcuts import get_object_or_404


class CommentLikeManager(models.Manager):
    def like_comment(self, comment_id, user):
        from .models import Comment
        comment = get_object_or_404(Comment,id=comment_id)
        self.create(comment=comment,user=user)

