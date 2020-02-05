from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import datetime
from django.utils.translation import ugettext_lazy as _

from django.utils.text import slugify
# Create your models here.


class UserProfileManger(BaseUserManager):
    user_for_related_fields = True

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)
    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs
    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(username=user.username)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(username=user.username)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


    def recommended(self, user, limit_to=50):
        profile = user
        following = profile.following.all().values_list('username')
        qs = self.get_queryset().exclude(username__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    A class implementing a fully featured User model with admin-compliant
    permissions.

    Email and password are required. Other fields are optional.
    """
    def get_avatar(self):
        return settings.STATIC_URL + str(self.avatar.name).split('/')[-1]
    email = models.EmailField(
        _('Email Address'), unique=True, blank=True, null=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    username = models.CharField(
        _('Username'), max_length=30, unique=True,
        help_text=_('30 characters or fewer. Letters, digits and _ only.'),

        error_messages={
            'unique': _("The username is already taken."),
        }
    )
    is_staff = models.BooleanField(
        _('Staff Status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), default=datetime.datetime.now())
    following = models.ManyToManyField('self', blank=True, related_name='followed_by')
    avatar = models.ImageField(upload_to='user_img/', null=True, blank=True)
    objects = UserProfileManger()
    USERNAME_FIELD = 'username'

    class Meta(object):
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfile')
        abstract = False

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.username)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username": self.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username": self.username})

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
#     following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
#     objects = UserProfileManger()
#
#
#     def __str__(self):
#         return str(self.following.all().count())
#
#     def get_following(self):
#         users = self.following.all()
#         return users.exclude(username=self.user.username)
#
#     def get_follow_url(self):
#         return reverse_lazy("profiles:follow", kwargs={"username": self.user.username})
#
#     def get_absolute_url(self):
#         return reverse_lazy("profiles:detail", kwargs={"username": self.user.username})
#
#     def post_save_user_receiver(sender, instance, created, *args, **kwargs):
#         if created:
#             new_profile = UserProfile.objects.get_or_created(user=instance)
#         post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)


# class UserData(models.Model):
#
#     user = models.OneToOneField(UserProfile, verbose_name=("user"), on_delete=models.CASCADE)
#     country = CountryField()
#     join_date = models.DateTimeField(default=datetime.datetime.now)
#     image = models.ImageField(upload_to='user_img', blank=True, null=True)
#     slug = models.SlugField(blank=True, null=True)
#
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.user.username)
#         super(UserData, self).save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = _("UserData")
#         verbose_name_plural = _("UserData")
#
#     def __str__(self):
#         return '%s' %(self.user)
#
#     def get_absolute_url(self):
#         return reverse("accounts:detail", kwargs={"slug": self.slug})
#
# def create_userData(sender, **kwargs):
#     if kwargs['created']:
#         user_data = UserData.objects.create(user=kwargs['instance'])
#
# post_save.connect(create_userData, sender=User)