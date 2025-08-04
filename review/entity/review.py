from django.db import models

from account.entity.account import Account


class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="blog_posts")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"
        app_label = "review"
