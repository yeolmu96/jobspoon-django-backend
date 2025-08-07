from django.db import models

class ImageGallery(models.Model):
    title = models.CharField(max_length=255)  # 이미지 제목
    image_url = models.CharField(max_length=128)  # S3 이미지 URL을 저장 (문자열)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    def __str__(self):
        return self.title

    class Meta:
        db_table = "image_gallery"
        app_label = "image_gallery"
