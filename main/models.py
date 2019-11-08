from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.dispatch import receiver
from django.db.models.signals import post_save

DAY_CHOICES = [
    (0, 'Saturday'),
    (1, 'Sunday'),
    (2, 'Monday'),
    (3, 'Tuesday'),
    (4, 'Wednesday'),
]


class Course(models.Model):
    department = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    course_number = models.IntegerField()
    group_number = models.IntegerField()
    teacher = models.CharField(max_length=120)
    start_time = models.CharField(max_length=120)
    end_time = models.CharField(max_length=120)
    first_day = models.IntegerField(choices=DAY_CHOICES)
    second_day = models.IntegerField(choices=DAY_CHOICES)
    exam_date = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile-image/', blank=True , null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        if instance.profile is not None :
            instance.profile.save()
