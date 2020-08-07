from .base import *
import environ

DEBUG = False

env = environ.Env(DEBUG=(bool,False),)
env.read_env(os.path.join(BASE_DIR,'.env'))

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DATABASES = {
    'default':env.db(),
}

STATIC_ROOT = '/usr/share/nginx/html/static'

MEDIA_ROOT = '/usr/share/nginx/html/media'