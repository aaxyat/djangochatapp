from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from server import validators


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path,
        blank=True,
        null=True,
        validators=[
            validators.validate_icon_image_size,
            validators.validate_image_file_extension,
        ],
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, *args, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.TextField(blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="server_members")

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        blank=True,
        null=True,
        validators=[validators.validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        blank=True,
        null=True,
        validators=[
            validators.validate_icon_image_size,
            validators.validate_image_file_extension,
        ],
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        return super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, *args, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)
