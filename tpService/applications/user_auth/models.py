from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户类拓展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='用户资料')
    role = models.CharField(max_length=10, default="tester", verbose_name="角色")
    avatar = models.CharField(max_length=100, null=True, blank=True, verbose_name="头像")
    phone = models.CharField(unique=True, null=True, max_length=11, verbose_name='手机号码')
    status = models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')
    description = models.CharField(max_length=4096, blank=True, null=True, verbose_name='描述')

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user.__str__())
