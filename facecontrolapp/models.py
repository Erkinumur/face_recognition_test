from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# User = get_user_model()
#
#
# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,
#                              related_name='profile')
#
#     def __str__(self):
#         return self.user.username
#
#
# class Image(models.Model):
#     file = models.ImageField(verbose_name='Фото')
#     encoding = models.TextField(max_length=5000)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
#                                 related_name='image')
#
#     def __str__(self):
#         return str(self.file)
#
#
# @receiver(pre_delete, sender=Image)
# def delete_image(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     if instance.file:
#         instance.file.delete(False)