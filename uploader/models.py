from django.db import models
from django.contrib.auth import get_user_model

from .functions import delete_from_minio

User = get_user_model()


class UploadedFile(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE,
                             verbose_name='User')

    file = models.FileField(null=True, blank=False)
    file_extension = models.CharField(max_length=155, null=True, blank=True,
                                      verbose_name='Extension')
    file_size = models.IntegerField(default=0, verbose_name='Size')

    def save(self, *args, **kwargs):
        if self.file:
            self.file_extension = self.file.name.split('.')[-1]
            self.file_size = self.file.size
        return super(UploadedFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            delete_from_minio(file_name=self.file.name)

        return super(UploadedFile, self).delete(*args, **kwargs)
