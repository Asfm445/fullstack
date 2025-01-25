from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validation import validate_icon_image_size, validate_image_file_extention


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"


def catagory_icon_upload_path(instance, filename):
    return f"catagory/{instance.id}/catagoty_icon/{filename}"


class catagory(models.Model):
    name = models.CharField(max_length=100)
    descroption = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=catagory_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extention],
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(catagory, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(catagory, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="api.catagory")
    def catagory_delete_files(sender, instance, **kwargs):
        for i in instance._meta.fields:
            if i.name == "icon":
                file = getattr(instance, i.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name


class server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    catagory = models.ForeignKey(
        catagory, on_delete=models.CASCADE, related_name="server_catagory"
    )
    descroption = models.CharField(max_length=250, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        blank=True,
        null=True,
        validators=[validate_image_file_extention],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extention],
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(server, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(catagory, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="api.server")
    def catagory_delete_files(sender, instance, **kwargs):
        for i in instance._meta.fields:
            if i.name == "icon":
                file = getattr(instance, i.name)
                if file:
                    file.delete(save=False)

        def save(self, *args, **kwargs):
            self.name = self.name.lower()
            super(channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
