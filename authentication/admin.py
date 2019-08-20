from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext, gettext_lazy as _
from authentication.models import User, UserProfile
from authentication.forms import UserChangeForm, UserCreationForm
from django.contrib import admin


class UserProfileInline(admin.StackedInline) :
    model = UserProfile
    can_delete = False


class MyUserAdmin(auth_admin.UserAdmin):

    def get_inline_instances(self, request, obj=None) :
        if not obj :
            return list()
        return super(MyUserAdmin, self).get_inline_instances(request, obj)

    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('email', 'is_player', 'is_coach', 'date_joined',
                    'is_admin', 'is_active', 'is_staff', 'is_superuser',
                    'last_login')  #
    # Contain
    # only
    # fields in your
    # `custom-user-model`
    list_filter = ('is_player', 'is_coach',)  # Contain only fields in your #
    # `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    search_fields = ('is_player', 'is_player',)  # Contain only fields in your
    # `custom-user-model` intended for searching
    ordering = ('is_player', 'is_coach',)  # Contain only fields in your
    # `custom-user-model` intended to ordering
    filter_horizontal = ()  # Leave it empty. You have neither `groups` or `user_permissions`
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields' : ('mobile',)}),
    # )
    readonly_fields = ['date_joined', 'last_login', ]

    fieldsets = (
        (_('Personal info'),
         {'fields' : ('email', 'password', 'is_player', 'is_coach',)}),
        (_('Permissions'), {'fields' : ('is_admin', 'is_staff',
                                        'is_superuser', 'is_active'), }),
        (_('Important dates'), {'fields' : ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'password1', 'password2')}
         ),
    )
    inlines = (UserProfileInline, )


# admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

# from django.contrib import admin
# from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.admin import UserAdmin
# from .models import UserProfile, User
# 
# class ProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
# 
# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
# 
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)
# 
#     list_display = ()
#     list_filter = ()
# 
#     fieldsets = (
#         ('Regular Expressions',
#          {'fields' : []}),
#     )
# 
#     search_fields = ()
#     ordering = ()
# 
#     filter_horizontal = ()
# 
# 
# # admin.site.unregister(groups)
# admin.site.register(User, CustomUserAdmin)
