from django.db import models
from django.shortcuts import get_object_or_404


class CommentManager(models.Manager):
    def create_comment(self, product_id, user, **comment_data):
        from .models import Product
        product = get_object_or_404(Product, id=product_id)
        self.create(product=product, author=user, **comment_data)

        product.update_rate()


class CommentLikeManager(models.Manager):
    def like_comment(self, comment_id, user):
        from .models import Comment

        comment = get_object_or_404(Comment, id=comment_id)
        self.create(comment=comment, user=user)
