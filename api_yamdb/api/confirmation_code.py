import random
import string


def generate_confirmation_code():

    return ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase, k=10))
