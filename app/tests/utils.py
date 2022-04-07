from django.contrib.auth.models import User

from app.tests.constants import USERNAME_USER_DEFAULT, EMAIL_USER_DEFAULT, PASSWORD_USER_DEFAULT, NAME_USER_DEFAULT


def delete_user(username):
    qs = User.objects.filter(username=username)
    if qs.exists():
        object = qs.first()
        object.delete()
    return User.objects.filter(username=username).count() == 0


def create_user():
    user = User.objects.create_user(username=USERNAME_USER_DEFAULT, email=EMAIL_USER_DEFAULT,
                                    password=PASSWORD_USER_DEFAULT, **{'first_name': NAME_USER_DEFAULT})
    return user
