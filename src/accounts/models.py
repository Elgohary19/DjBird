from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import datetime
from django.utils.translation import ugettext_lazy as _

from django.utils.text import slugify
# Create your models here.


class UserProfileManger(models.Manager):
    user_for_related_fields = True


    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs
    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


    def recommended(self, user, limit_to=50):
        profile = user.profile
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    objects = UserProfileManger()


    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username": self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username": self.user.username})

    def post_save_user_receiver(sender, instance, created, *args, **kwargs):
        if created:
            new_profile = UserProfile.objects.get_or_created(user=instance)
        post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)


class UserData(models.Model):

    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    country = CountryField()
    join_date = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to='user_img', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(UserData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("UserData")
        verbose_name_plural = _("UserData")

    def __str__(self):
        return '%s' %(self.user)

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"slug": self.slug})

def create_userData(sender, **kwargs):
    if kwargs['created']:
        user_data = UserData.objects.create(user=kwargs['instance'])

post_save.connect(create_userData, sender=User)