from django.contrib import admin
from django.utils.text import capfirst
from collections import OrderedDict as SortedDict

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from applications.user_auth.models import UserProfile


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        for app in template_response.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return template_response

    return inner


registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
admin.site.site_header = '测试平台-后台管理'
admin.site.siteTitle = '后台管理'
display = ()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
