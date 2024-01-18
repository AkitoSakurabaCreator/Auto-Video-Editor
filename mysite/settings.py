import os
from pathlib import Path

from datetime import timedelta  # JWT


DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = []


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')


STATIC_URL = '/static/'
MEDIA_URL = '/media/'


if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_ROOT = '/usr/share/nginx/html/static'
    MEDIA_ROOT = '/usr/share/nginx/html/media'


STATICFILES_DIRS = [
    (STATIC_DIR),
    ('account', STATIC_DIR + '/accounts/'),
    ('media', MEDIA_ROOT),
]

SECRET_KEY = ''


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'app',
    # 'ave',
    'accounts',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'django.contrib.humanize',  # カンマ

    'bootstrap_datepicker_plus',  # カレンダー 誕生日
    'django_cleanup',

    # Celery apps
    "celery", #追加
    "celery_progress", #追加
    'django_celery_results', # 追加


    
    # 'accounts_jwt',
    # 'rest_framework' #JWT認証

    # 'xadmin'
    # 'crispy_forms',
    # 'xadmin',

    # 'social_django',  # ソーシャルログイン
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'social_django.middleware.SocialAuthExceptionMiddleware',  # ソーシャルログイン
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.media', #プロフ画像で使用
                # 'social_django.context_processors.backends',  # ソーシャルログイン
                # 'social_django.context_processors.login_redirect', # ソーシャルログイン
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_I10N = True

USE_TZ = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# --------------------------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'  # 元
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


NUMBER_GROUPING = 3  # カンマ区切り

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# メールをコンソールに表示する
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# 自動ログアウト
# デフォルトは二週間後
# セッション時間
# SESSION_COOKIE_AGE = 60 * 60 #60 * 5 = 5分
# 最後にアクセスしてからの測定
SESSION_SAVE_EVERY_REQUEST = True



# CELERY_BROKER_URL = 'redis://localhost:6379/1'
# CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
# CELERY_TASK_TRACK_STARTED = True


# CELERY_BROKER_URL = "redis://127.0.0.1:6379/0" # ブローカーにredisを指定
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = "django-db" # 結果はdjango指定のDBに保存。本記事ではMySQLを想定。
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TASK_TRACK_STARTED = True # taskが開始状態になったことを確認できるための設定（後述）
