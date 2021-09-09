from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from .models import Invitation as model_cls,InvitationChoices
from .invite_code import generate_random_code_for_invite
from ..account import services
"""
This signal assigns a randomly generated avatar to a new user.
"""
@receiver(pre_save,sender=model_cls)
def generated_invite_code_pre_save(sender,instance,*args,**kwargs):
    if not instance.invite_token:
        instance.invite_token = generate_random_code_for_invite()



# custom signals
invite_is_created = Signal(providing_args=["invite"])
invite_is_accepted = Signal(providing_args=["user"])

# custom signal handler (receivers)
@receiver(invite_is_created)
def new_invited_created_reciever(sender,**kwargs):
    invite = kwargs.get('invite')
    # create user
    user = services.\
        create_inactive_user_account_from_email(user_email=invite.invite_to_email,
        invite_code=invite.invite_token)
    invite.invite_to_user = user
    invite.save(update_fields=["invite_to_user"])


@receiver(invite_is_accepted)
def new_invited_created_reciever(sender,**kwargs):
    user = kwargs.get('user')
    invite = model_cls._default_manager.get(invite_token__iexact=user.invite_code)
    invite.invite_status = InvitationChoices.ACCEPTED
    invite.save(update_fields=["invite_status"])