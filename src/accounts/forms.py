from django import forms
from allauth.account.forms import SignupForm
# from bootstrap_datepicker_plus import DatePickerInput
# import bootstrap_datepicker_plus.widgets as datetimepicker
from bootstrap_datepicker_plus.widgets import DatePickerInput

# from django.db import models
from accounts.models import CustomUser #カスタムユーザー
from django.core.exceptions import ValidationError


class ProfileForm(forms.Form):
    # def validate_screen_id(value):
    #     if "itc.tokyo" in value:
    #         raise ValidationError(
    #             _("「itc.tokyo」は使用できません。")
    #             code="no-itc"
    #         )

            #以下を追記
    # def clean_screen_id(self):
    #     user_screen_id = self.cleaned_data['user_screen_id']
    #     # user_screen_id = self.cleaned_data["user_screen_id"]
    #     # username = self.cleaned_data.get("username")
    #     if user_screen_id and CustomUser.objects.filter(user_screen_id=user_screen_id).exists():
    #         raise forms.ValidationError("既に使われています。別のIDに変更してください")
    #     return user_screen_id
    
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if email:
    #         if "itc.tokyo" in email:
    #             raise ValidationError(
    #                 _("「itc.tokyo」は使用できません。")
    #                 code="no-itc"
    #             )
    #     return data
    
    first_name = forms.CharField(max_length=30, label='姓', required=True)
    last_name = forms.CharField(max_length=30, label='名', required=True)
    nick_name = forms.CharField(max_length=30, label='ニックネーム', required=False)
    user_screen_id = forms.CharField(max_length=30, label='ユーザーID', required=True)
    
    
    # year = forms.CharField(max_length=8, label='生年月日')
    # year = forms.DateField(widget=forms.SelectDateWidget(), label='生年月日')
    # year = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label='生年月日')
    
    # zipcode = forms.CharField(max_length=8, label='郵便番号')
    # zipcode = forms.CharField(max_length=8, label='郵便番号')
    zipcode = forms.RegexField(label='郵便番号(ハイフンなし)',
        regex=r'^[0-9]+$',
        max_length=7,
        widget=forms.TextInput(), required=False
        )
    address = forms.CharField(max_length=30, label='住所', required=False)
    buildingname = forms.CharField(max_length=30, label='建物名(任意)', required=False)
    tel = forms.CharField(max_length=30, label='電話番号', required=False)
    job = forms.CharField(max_length=30, label='職業(任意)', required=False)
    
    # year = forms.CharField(
    #         label='生年月日',
    #         widget=DatePickerInput(format='%Y/%m/%d', #formに入る日付の書式を指定
    #         options={
    #         'locale': 'ja', #言語を指定
    #         'dayViewHeaderFormat': 'YYYY年 MMMM', #カレンダーの日付の表示書式を指定
    #         }))
    
    year = forms.CharField(
            label='生年月日',
            widget = DatePickerInput(
            format='%Y/%m/%d',
            attrs={'readonly': 'true','id': 'year'},
            options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                    'ignoreReadonly': True,
                    'allowInputToggle': True
                    }))
    
    avatar = forms.ImageField(label="プロフィール画像", required=False)


# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.conf import settings

# subject = "登録確認"
# message_template = "TEST"

# def get_activate_url(user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     return settings.FRONTEND_URL + "/activate/{}/{}/".format(uid, token)



class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    read_terms = forms.BooleanField(
        label="利用規約同意",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'check'}),
    )

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.read_terms = self.cleaned_data['read_terms']
        user.save()
        return user

    # def save(self, request, commit = True):
    #     user = super(SignupUserForm, self).save(request)
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']

    #     user.is_active = False

    #     user.save()

    #     if commit:
    #         user.save()
    #         activate_url = get_activate_url(user)
    #         message = message_template + activate_url
    #         user.email_user(subject, message)
    #     return user
    

# def activate_user(uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode()
#         user = User.objects.get(pk=uid)
#     except Exception:
#         return False

#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return True
#         return False


class Inquiry(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    first_name = forms.CharField(max_length=30, label="姓")
    last_name = forms.CharField(max_length=30, label="名")
    title = forms.CharField(max_length=100, label="件名")
    summary = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea)
    read_field = forms.BooleanField(
        label="お問い合わせ送信確認",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'check'}),
    )




# from django.contrib.auth.forms import (
#     AuthenticationForm, UserCreationForm
# )
# from django.contrib.auth import get_user_model

# User = get_user_model()
# class UserCreateForm(UserCreationForm):
#     """ユーザー登録用フォーム"""

#     class Meta:
#         model = User
#         fields = ('email',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         User.objects.filter(email=email, is_active=False).delete()
#         return email


# from django.contrib.auth.forms import (
#     AuthenticationForm, UserCreationForm, PasswordChangeForm
# )
# from django.contrib.auth import get_user_model

# class MyPasswordChangeForm(PasswordChangeForm):
#     """パスワード変更フォーム"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'