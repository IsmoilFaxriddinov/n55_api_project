from django.contrib import admin

from users.models import CustomUserModel, ProfileModel, VerificationModel

admin.site.register(CustomUserModel)
admin.site.register(ProfileModel)
admin.site.register(VerificationModel)
