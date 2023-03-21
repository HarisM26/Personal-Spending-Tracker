from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from expenditure.choices import TOGGLE_CHOICE, LEAGUE


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
        # ///?? cannot create user in admin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"),
                              unique=True,
                              max_length=255,
                              blank=False,
                              )

    first_name = models.CharField(
        max_length=30,
    )

    last_name = models.CharField(
        max_length=150,
    )

    points = models.IntegerField(default=0)

    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='followees'
    )

    league_status = models.CharField(
        max_length=8,
        choices=LEAGUE.choices,
        default=LEAGUE.BRONZE,
    )

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    
    is_private = models.BooleanField(default=False)

    toggle_notification = models.CharField(
        max_length=3, choices=TOGGLE_CHOICE, default='ON')
        
    toggle_privacy = models.CharField(
        max_length=3, choices=TOGGLE_CHOICE, default='OFF')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def toggle_follow(self, followee):
        if followee == self:
            return
        if self.is_following(followee):
            self._unfollow(followee)
        else:
            self._follow(followee)

    def _follow(self, user):
        user.followers.add(self)

    def _unfollow(self, user):
        user.followers.remove(self)

    def is_following(self, user):
        return user in self.followees.all()
        
    def show_following(self):
    	return self.followees.all()

    def follower_count(self):
        return self.followers.count()

    def followee_count(self):
        return self.followees.count()

    def __str__(self):
        return self.email

    @property
    def user_id(self):
        return f'{self.first_name}@{self.id}'

    @property
    def get_points(self):
        return DailyPoint.objects.filter(user__pk=self.pk).count()

    def add_login_points(self):
        self.points += 1
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    def __str__(self):
        return self.user.first_name

    def __str__(self):
        return self.user.last_name


class DailyPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')
