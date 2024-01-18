from django import forms

from django.db import models
import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Coupon(forms.Form):
    couponcode = forms.CharField(label='クーポンコード', max_length=20)

    
def validate_is_movie(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in ['.mp4', '.mkv', '.avi', '.zip']:
        raise ValidationError(_("動画ファイル形式ではありません。"), code="Not Movie File")

class MovieEdit(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200, required=False)
    movie_format = forms.IntegerField(label="フォーマット", required=False)
    voice = forms.fields.ChoiceField(label="音声", required=False, 
    choices  = (
    ("None","ボイス無し"),
    ("0","四国めたん あまあま"),
    ("1", "ずんだもん あまあま"),
    ("2","四国めたん ノーマル"),
    ("3", "ずんだもん ノーマル"),
    ),
    widget=forms.widgets.Select
    )
    language = forms.fields.ChoiceField(label="言語", required=False, 
    choices = (
        ("ja","日本語"),
        ("en", "英語"),
        ("ko", "韓国"),
        ("zh", "中国語"),
    ),
    widget=forms.widgets.Select
    )
    telopPos = forms.fields.ChoiceField(label="テロップ位置", required=False, 
    choices = (
        ("top", "上"),
        ("center","真ん中"),
        ("bottom", "下"),
    ),
    widget=forms.widgets.Select, initial="bottom")
    model = forms.fields.ChoiceField(label="学習レベル", required=False, 
    choices = (
        ("tiny","ライト版"),
        ("base","お手軽版"),
        ("small","小性能"),
        ("medium", "中性能"),
        ("large","高性能"),
    ),
    widget=forms.widgets.Select, initial="medium"
    )
    filter_effect = forms.IntegerField(label="フィルター", required=False)
    animations = forms.IntegerField(label="アニメーション", required=False)
    bgm = forms.IntegerField(label="BGM", required=False)
    volume = forms.IntegerField(label="音声調整", required=False)
    cut = forms.IntegerField(label="カット", required=False)
    translate = forms.fields.ChoiceField(label="翻訳", required=False,
    choices = (
        ("None","翻訳なし"),
        ("translate","英語へ翻訳する"),
    ),
    widget=forms.widgets.Select)
    upload = forms.FileField(label="動画ファイル",  required=True, widget=forms.widgets.FileInput, validators=[validate_is_movie])
    publish = forms.fields.ChoiceField(label="公開", required=False, 
    choices = (
        ("publish","公開"),
        ("limited","限定公開"),
        ("close","非公開")
    ),
    widget=forms.widgets.Select, initial="close"
    )
    # edited = forms.FileField(label="編集済みファイル",  required=True, widget=forms.widgets.FileInput, validators=[validate_is_movie])