from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User,AbstractUser
# from .models import CustomUser
# from django.contrib import admin
#
# # Register your models here.
# admin.site.register(CustomUser)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'get_gender','get_location','get_birthday','get_usertype','get_FavoriteLanguage'
                    )
    list_select_related = ('profile', )

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_gender(self, instance):
        return instance.profile.gender
    get_gender.short_description = 'gender'

    def get_birthday(self,instance):
        return instance.profile.birthdate

    get_birthday.short_description = 'birthday'

    def get_usertype(self,instance):
        return instance.profile.userType

    get_usertype.short_description = 'usertype'

    def get_FavoriteLanguage(self,instance):
        return instance.profile.FavoriteLanguage

    get_FavoriteLanguage.short_description = 'Favorite Language'


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Solutions)