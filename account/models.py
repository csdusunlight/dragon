#coding:utf-8
from django.db import models
from .tools import random_str
# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
import datetime
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from decimal import Decimal
class MyUserManager(BaseUserManager):

    def _create_user(self, email, mobile, username, password,
                     is_staff, is_superuser):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = datetime.datetime.now()
        if not email or not mobile or not username:
            raise ValueError('The given email, mobile and username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, username=username, 
                          is_staff=is_staff, 
                          is_active=True, is_superuser=is_superuser,
                          date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, mobile, username, password=None, **extra_fields):
        return self._create_user(email, mobile, username, password, False, False)

    def create_superuser(self,email, mobile, username, password):
        return self._create_user(email, mobile, username, password, True, True)
    def get_by_natural_key(self, username):
        try:
            return self.get(**{'mobile': username})
        except MyUser.DoesNotExist:
            return self.get(**{'username': username})
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255)
    mobile = models.CharField('mobile number', max_length=11, unique=True,)
    username = models.CharField(u'用户昵称', max_length=30, unique=True)
    inviter = models.ForeignKey('self', related_name = 'invitees', 
                                blank=True, null=True, on_delete=models.SET_NULL)
    invite_code = models.CharField(u"邀请码", unique=True, blank=True, max_length=20)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    accu_income = models.DecimalField(u'累计收益', default = Decimal(0.00), decimal_places = 2, max_digits=10)
    accu_scores = models.IntegerField(u'累计获得积分', default = 0)
    invite_account = models.DecimalField(u'邀请奖励结余', default = Decimal(0.00), decimal_places = 2, max_digits=10)
    invite_income = models.DecimalField(u'邀请奖励现金', default = Decimal(0.00), decimal_places = 2, max_digits=10)
    invite_scores = models.IntegerField(u'邀请奖励积分', default = 0)
    balance = models.DecimalField(u'现金余额', default = Decimal(0.00), decimal_places = 2, max_digits=10)
    scores = models.IntegerField(u'积分余额', default = 0)
    isSigned = models.BooleanField('是否签到', default=False,
        help_text='Designates whether the user had signed in today.')
    last_login_time =  models.DateTimeField(u'上一次登录时间', null=True, blank=True)
    this_login_time =  models.DateTimeField(u'最近登录时间', null=True, blank=True, default=timezone.now)
    pay_password = models.CharField(u'支付密码', max_length=128, blank=True)
    is_email_authenticated =  models.BooleanField('是否通过邮箱认证', default=False)
    zhifubao = models.CharField(u'支付宝账号', max_length=64, blank=True, default='')
    zhifubao_name = models.CharField(u'支付宝姓名', max_length=30, blank=True, default='')
    admin_permissions = models.ManyToManyField('AdminPermission',
        verbose_name='admin permissions', blank=True,
        related_name="user_set", related_query_name="user")
    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']
    
    def set_pay_password(self, raw_password):
        self.pay_password = make_password(raw_password)
    def check_pay_password(self, raw_password):
        return check_password(raw_password, self.pay_password)
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        if not self.pk:
            self.invite_code = random_str(5) + str(MyUser.objects.count())
        return AbstractBaseUser.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']
    def get_full_name(self):
        return self.mobile
    def get_short_name(self):
        return self.mobile
    def get_abbre_name(self):
        username = self.username
        if len(username) > 4:
            username = username[0:4] + '****'
        else:
            username = username + '****'
        return username
    def has_admin_perms(self, code):
        return self.admin_permissions.filter(code=code).exists()
    def __unicode__(self): 
        return self.mobile
    
# class InviteDetail(MyUser):
#     inviter = models.ForeignKey(MyUser, related_name="user_inviter_ditail")
#     invitee = models.OneToOneField(MyUser, related_name="user_invitee_ditail")
#     message_num = models.IntegerField()
class Userlogin(models.Model):
    user = models.ForeignKey(MyUser, related_name="user_login_history")
    time = models.DateTimeField(u'登录时间', default = timezone.now)
    class Meta:
        ordering = ["-time"]
    def __unicode__(self):
        return self.user.mobile
class UserSignIn(models.Model):
    user = models.ForeignKey(MyUser, related_name="user_signin_history")
    date = models.DateField(u'签到日期', default = timezone.now)
    signed_conse_days = models.PositiveIntegerField("连续签到天数", default=1)
    class Meta:
        ordering = ["-date"]
        unique_together = (('user', 'date'),)
class MobileCode(models.Model):
    mobile = models.CharField('mobile number', max_length=11, )
    identifier = models.CharField('identifier', max_length=10, blank=True,)
    rand_code = models.CharField('random code', max_length=6)
    create_at = models.DateTimeField("created at", auto_now_add=True, editable=True)
    remote_ip = models.CharField('remote_ip', max_length=15, blank=True)
    def __unicode__(self):
        return self.identifier + ':' + self.mobile + ':' + self.remote_ip
    class Meta:
        ordering = ['-create_at']
class EmailActCode(models.Model):
    email = models.EmailField('email address', max_length=255, unique=True,)
    rand_code = models.CharField('random code', max_length=50, unique=True,)
    create_at = models.DateTimeField(u"created at", auto_now=True, editable=True)
    def __unicode__(self):
        return self.email
    class Meta:
        ordering = ['-create_at']
class Access_Token(models.Model):
    app_id = models.CharField(u"app_id",max_length=20,unique=True,)
    app_secret = models.CharField(u"app_secret",max_length=40,)
    access_token = models.CharField(u"access_token",max_length=60,)
    expire_stramp = models.IntegerField(u"expire_time")
    
class AdminPermission(models.Model):
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField('name', max_length=255)
    def __unicode__(self):
        return self.code + ',' + self.name