from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

turn_value = 5
move_value = 10
loop_value = 15


# Create your models here.
def user_directory_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/images/{1}'.format(instance.id, filename)


def user_directory_level_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/levels/{1}'.format(instance.by.id, filename)


class User(AbstractUser):
    image = models.ImageField(default='no_image.png', upload_to=user_directory_image_path)
    points = models.FloatField(default=10, blank=False)


class Mate(models.Model):
    a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='a', blank=False)
    b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='b', blank=False)

    a_confirmation = models.BooleanField(default=True, blank=False)
    b_confirmation = models.BooleanField(default=False, blank=False)

    date = models.DateTimeField(default=timezone.now, blank=False)


def mate_change(by, to):
    try:
        mate = Mate.objects.get(a=by, b=to)
        mate.a_confirmation = not mate.a_confirmation
    except ObjectDoesNotExist:
        try:
            mate = Mate.objects.get(a=to, b=by)
            mate.b_confirmation = not mate.b_confirmation
        except ObjectDoesNotExist:
            try:
                by = User.objects.get(id=by)
                to = User.objects.get(id=to)
                mate = Mate(a=by, b=to)
            except ObjectDoesNotExist:
                return
    mate.save()
    return mate


# TODO Levels, Comments,
class Level(models.Model):
    name = models.CharField(max_length=128, blank=False)
    date = models.DateTimeField(default=timezone.datetime.now, blank=False)

    by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    tilemap = models.TextField(max_length=1024)

    command_forward = models.IntegerField(blank=True)
    command_backward = models.IntegerField(blank=True)
    command_left = models.IntegerField(blank=True)
    command_right = models.IntegerField(blank=True)
    command_lo = models.IntegerField(blank=True)
    command_op = models.IntegerField(blank=True)

    hero_x = models.IntegerField(blank=False)
    hero_y = models.IntegerField(blank=False)
    hero_dir = models.IntegerField(blank=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    to = models.ForeignKey(Level, on_delete=models.CASCADE, blank=False, null=False)
    by = models.ForeignKey(User, related_name='comment_by', on_delete=models.CASCADE, blank=False, null=False)

    forward = models.ForeignKey(User, related_name='comment_forward', on_delete=models.CASCADE, blank=True, null=True)

    value = models.TextField(max_length=256)


class Rate(models.Model):
    to = models.ForeignKey(Level, on_delete=models.CASCADE, blank=False, null=False)
    by = models.ForeignKey(User, related_name='rate_by', on_delete=models.CASCADE, blank=False, null=False)

    value = models.IntegerField()


class Result(models.Model):
    to = models.ForeignKey(Level, related_name='result_to', on_delete=models.CASCADE, blank=False, null=False)
    by = models.ForeignKey(User, related_name='result_by', on_delete=models.CASCADE, blank=False, null=False)

    date = models.DateTimeField(default=timezone.now, blank=False)
    attempts = models.IntegerField(blank=False)
    program = models.TextField(max_length=512)

    result = models.BooleanField(default=False, blank=False)

    score = models.IntegerField(default=0, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=128, blank=True)
    value = models.TextField(max_length=512, blank=False)

    date = models.DateTimeField(default=timezone.now, blank=False)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
