from accounts.models import CustomUser
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        dt = datetime.datetime.now()
        birth_list = CustomUser.objects.filter(birthday__month=dt.month)
        for birth in birth_list:
            subject = render_to_string('app/mail_template/coupon_subject.txt', {'birth': birth})
            message = render_to_string('app/mail_template/coupon_message.txt', {'birth': birth})
            send_mail(subject, message, None, [birth.email])