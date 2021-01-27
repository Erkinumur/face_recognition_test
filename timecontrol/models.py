from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name="profiles")
    position = models.CharField(max_length=50)
    subscription = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class TimeControl(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name="timecontrols")
    incoming = models.DateTimeField()
    outcoming = models.DateTimeField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.profile} - {self.incoming} - {self.outcoming}'


class Image(models.Model):
    file = models.ImageField(verbose_name='Фото', upload_to='photos')
    encoding = models.TextField(max_length=5000)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,
                                related_name='image')

    def __str__(self):
        return str(self.file)


@receiver(pre_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)