import secrets

from ..users.models import User as model_cls


def generate_random_code_for_invite():
    '''
    > assume user model as a invite_code field
    > use signals to assign code to that field when user is created

    user.invite_code = generate_random_code_for_invite()

    '''
    code = generate_random_code()
    while is_available_random_code(code):
        code = generate_random_code(code)
    return code



def generate_random_code():
    # generate code in format "ABCD-FGHI-JKLM"
    code = secrets.token_hex(nbytes=6).upper()
    return "-".join(code[i : i + 4] for i in range(0, len(code), 4)) 



def is_available_random_code(code):
    return model_cls._default_manager.filter(invite_code__iexact=code).exists()