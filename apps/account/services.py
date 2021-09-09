from django.db import transaction as tx
from django.db import IntegrityError
from django.apps import apps

from ..users.models import User as model_cls


@tx.atomic
def create_username_from_email(email:str) -> str:
    # use regex. to validate username

    username = email.split("@")[0]
    dot = "."
    if dot in username:
        username = username.replace(dot,"_")

    qs = model_cls._default_manager.filter(username__iexact=username)

    while qs.exists():
        str_ = string.digits[3:6]
        username = username + str_
        return create_username_from_email(username)
    return username


@tx.atomic
def create_inactive_user_account_from_email(*,user_email:str,invite_code:str=None):
    # NB: signals can't handle this tasks. - celery is great !
    email = user_email
    username = create_username_from_email(user_email)

    user = model_cls._default_manager.create_user(
        username=username,
        email=email)
    user.is_active = False
    user.set_unusable_password()
    if invite_code:
        user.invite_code = invite_code
    try:
        user.save()
    except IntegrityError:
        raise ValueError("User is already registered")

    return user


def is_user_already_registered(*, username:str, email:str) -> (bool, str):
    """
    Checks if a specified user is already registred.

    Returns a tuple containing a boolean value that indicates if the user exists
    and in case he does whats the duplicated attribute
    """

    if model_cls.objects.filter(username=username):
        return (True, _("Username is already in use."))

    if model_cls.objects.filter(email=email):
        return (True, _("Email is already in use."))

    return (False, None)