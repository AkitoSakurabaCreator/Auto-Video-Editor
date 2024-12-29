from django.contrib import admin
from .models import CustomUser, Post_Inquiry

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class QuestionAdmin(admin.ModelAdmin):
    # list_display = ('complete')
    list_filter = ['complete', 'created']
    search_fields = ['title', 'first_name', 'last_name']

class UserAdmin(admin.ModelAdmin):
    # CustomUser = CustomUser.objects.filter().all()
    # def GetUserData(self):
    #     return f'名前: {self.first_name} ID: {self.user_screen_id} メール: {self.email}'
    # list_display = (GetUserData(CustomUser))
    list_display = ('email', 'first_name','last_name',  'is_active', 'is_staff')
    list_filter = (
        'is_active', 
        'is_staff'
    )
    ordering = ("email", 'is_active', 'is_staff')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Post_Inquiry, QuestionAdmin)

