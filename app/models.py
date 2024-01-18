from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import CustomUser #カスタムユーザー
import os

from datetime import datetime
import hashlib

import uuid

from django.urls import reverse

# class OrderItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     ordered_date = models.DateTimeField(default=timezone.now)
    
#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def __str__(self):
#         return f'{self.item.title}:{self.quantity}'
    
#     class Meta:
#         verbose_name = "注文一覧"
#         verbose_name_plural = "注文一覧"

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     items = models.ManyToManyField(OrderItem)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)
#     payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_total_item_price()
#         return total
    
#     def __str__(self):
#         return self.user.email
    
#     class Meta:
#         verbose_name = "注文履歴"
#         verbose_name_plural = "注文履歴"

# class Payment(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
#     stripe_change_id = models.CharField(max_length=50)
#     amount = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.email
    
#     class Meta:
#         verbose_name = "支払一覧"
#         verbose_name_plural = "支払一覧"

# class LikeForPost(models.Model):
#     """投稿に対するいいね"""
#     target = models.ForeignKey(Item, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)

# class Like(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # target = models.ForeignKey(FashionSaveList, on_delete=models.CASCADE)

def CouponWeek():
    return timezone.now() + timezone.timedelta(days=7)

class Section(models.Model):
    banner = models.ImageField("バナー画像", default='Users/site/test.jpg')
    content = models.TextField("メイン紹介文")
    content_sub = models.TextField("サブ紹介文")
    product = models.TextField("商品紹介文")
    product_image = models.ImageField("商品画像", default='Users/site/test.jpg')
    created = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return str(f"{self.content[:10]} | {self.content_sub[:10]}")
    
    class Meta:
        verbose_name = "メインページ紹介文"
        verbose_name_plural = "メインページ紹介文"

class News(models.Model):
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "ニュース一覧"
        verbose_name_plural = "ニュース一覧"

def uploadFile(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'Users/MovieEdit/'
    return '%s%s' % (saved_path, hs_filename)

from django.utils.crypto import get_random_string
def create_id():
    return get_random_string(10)

class Publish(models.Model):
    publishName = models.CharField("公開範囲", max_length=10)
    title = models.CharField("タイトル", max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "公開範囲一覧"
        verbose_name_plural = "公開範囲一覧"
    
class Editor(models.Model):
    editorId = models.SlugField(
        "EditorID", max_length=30, unique=True, default=create_id, null=False)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload = models.FileField("動画ファイル", upload_to=uploadFile)
    # created = models.DateTimeField("作成日", default=timezone.now)
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, blank=True, null=True)
    status_choices = (
        ("1","未着手"),
        ("2", "作成中"),
        ("3", "完了"),
    )
    status = models.CharField(max_length=20, choices=status_choices, default=status_choices[0][0])
    edited = models.FileField("編集済みファイル", blank=True, null=True)
    textFile = models.FileField("テキストファイル", blank=True, null=True)
    # edited = models.FileField("編集済みファイル", blank=True, null=True)

    # publish = models.BooleanField(default=False)
    publish = models.ForeignKey('Publish', on_delete=models.SET_NULL, blank=True, null=True)

    task_id = models.CharField("タスクID", max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.template.title)

    class Meta:
        verbose_name = "動画編集"
        verbose_name_plural = "動画編集"

class Filters(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "フィルタ一覧"
        verbose_name_plural = "フィルタ一覧"

class Animations(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "アニメーション一覧"
        verbose_name_plural = "アニメーション一覧"
        
class BGM(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    upload = models.FileField("BGMファイル", upload_to=uploadFile, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "BGM一覧"
        verbose_name_plural = "BGM一覧"

class Format(models.Model):
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "フォーマット一覧"
        verbose_name_plural = "フォーマット一覧"
    
class Model(models.Model):
    modelId = models.CharField("モデル", max_length=10)
    title = models.CharField("タイトル", max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "音声認識モデル一覧"
        verbose_name_plural = "音声認識モデル一覧"

class Telop(models.Model):
    telopName = models.CharField("位置", max_length=10)
    title = models.CharField("タイトル", max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "テロップ一覧"
        verbose_name_plural = "テロップ一覧"

class Language(models.Model):
    code = models.CharField("言語コード", max_length=10)
    title = models.CharField("タイトル", max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "言語一覧"
        verbose_name_plural = "言語一覧"
        
class Voice(models.Model):
    VoiceId = models.CharField("モデル", max_length=10)
    title = models.CharField("タイトル", max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "読み上げ音声モデル一覧"
        verbose_name_plural = "読み上げ音声モデル一覧"

class Template(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("動画のタイトル", max_length=200, default="無題のタイトル")
    # movie_format = models.IntegerField("フォーマット", default=-1)
    movie_format = models.ForeignKey('Format', on_delete=models.SET_NULL, blank=True, null=True)
    # filter_effect = models.IntegerField("フィルター", default=-1)
    filter_effect = models.ForeignKey('Filters', on_delete=models.SET_NULL, blank=True, null=True)
    animations = models.ForeignKey('Animations', on_delete=models.SET_NULL, blank=True, null=True)
    # animations = models.IntegerField("アニメーション", default=-1)
    bgm = models.ForeignKey('BGM', on_delete=models.SET_NULL, blank=True, null=True)
    # bgm = models.IntegerField("BGM", default=-1)
    cut = models.IntegerField("カット", default=-1)
    volume = models.IntegerField("音声調整", default=-1)
    # model_choices = (
    # ("tiny","ライト版"),
    # ("base","お手軽版"),
    # ("small","小性能"),
    # ("medium", "中性能"),
    # ("large","高性能"),
    # )
    # model = models.CharField(max_length=20, choices=model_choices, default=model_choices[0][0])
    model = models.ForeignKey('Model', on_delete=models.SET_NULL, blank=True, null=True)
    # voice_choices = (
    # ("-1","ボイス無し"),
    # ("0","四国めたん あまあま"),
    # ("1", "ずんだもん あまあま"),
    # ("2","四国めたん ノーマル"),
    # ("3", "ずんだもん ノーマル"),
    # )
    # voice = models.CharField(max_length=20, choices=voice_choices, default=voice_choices[0][0])
    voice = models.ForeignKey('Voice', on_delete=models.SET_NULL, blank=True, null=True)
    # language_choices = (
    #     ("ja","日本語"),
    #     ("en", "英語"),
    #     ("ko", "韓国"),
    #     ("zh", "中国語"),
    # )
    # language = models.CharField(max_length=20, choices=language_choices, default=language_choices[0][0])
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, blank=True, null=True)
    # telopPos_choices = (
    # ("top", "上"),
    # ("center","真ん中"),
    # ("bottom", "下"),
    # )
    # telopPos = models.CharField(max_length=20, choices=telopPos_choices, default=telopPos_choices[0][0])
    telopPos = models.ForeignKey('Telop', on_delete=models.SET_NULL, blank=True, null=True)
    translate_choices = (
        ("None","翻訳なし"),
        ("translate","英語へ翻訳する"),
    )
    translate = models.CharField(max_length=20, choices=translate_choices, default=translate_choices[0][0], blank=True, null=True)
    templateId = models.SlugField(
        "テンプレートID", max_length=30, unique=True, default=create_id, null=False)
    # publish_choices = (
    #     ("publish","公開"),
    #     ("limited","限定公開"),
    #     ("close","非公開")
    # )
    # publish = models.CharField(max_length=20, choices=publish_choices, default=publish_choices[2][1])
    publish = models.ForeignKey('Publish', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "テンプレート"
        verbose_name_plural = "テンプレート"

class Plan(models.Model):
    title = models.CharField("プランレベル", max_length=200)
    content = models.TextField("内容")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "プラン一覧"
        verbose_name_plural = "プラン一覧"