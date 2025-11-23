from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField


# from django.contrib.auth.models import User, UserManager


class UserStatusChoice(models.IntegerChoices):
    ACTIVED = 1
    UNACTIVE = 2
    LOCKED = 3


class OAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):

        if not realname:
            raise ValueError("必须设置真实姓名")
        email = self.normalize_email(email)

        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoice.ACTIVED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)


# 重写User模型
class OAUser(AbstractBaseUser, PermissionsMixin):
    """
    自定义的User模型
    """
    uid = ShortUUIDField(primary_key=True)
    realname = models.CharField(max_length=150, unique=False)
    email = models.EmailField(blank=False, unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    is_staff = models.BooleanField(default=True)

    status = models.IntegerField(choices=UserStatusChoice, default=UserStatusChoice.UNACTIVE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = OAUserManager()

    # 员工的部门表,一个员工只能在一个部门,一个部门有多个员工
    department = models.ForeignKey('OADepartment', null=True, on_delete=models.SET_NULL, related_name='staffs',
                                   related_query_name='staffs')

    EMAIL_FIELD = "email"
    # from django.contrib.auth import authenticate
    # USERNAME_FIELD：是用来做鉴权的，会把authenticate的username参数，传给USERNAME_FIELD指定的字段
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS：指定哪些字段是必须要传的，但是不能重复包含USERNAME_FIELD和EMAIL_FIELD已经设置过的值
    REQUIRED_FIELDS = ["realname", "password"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        return self.realname


class OADepartment(models.Model):
    # 部门名称
    name = models.CharField(max_length=100)
    # 部门介绍
    intro = models.CharField(max_length=200)
    # 部门领导,设定每个部门只有一个领导
    leader = models.OneToOneField(OAUser, null=True, on_delete=models.SET_NULL, related_name='leader_department',
                                  related_query_name='leader_department')
    # 部门管理者,设定多个部门可以被一个管理者管理
    manager = models.ForeignKey(OAUser, null=True, on_delete=models.SET_NULL, related_name='manager_departments',
                                related_query_name='manager_departments')
