import random
import string

def random_lower_string(len: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=len))

def random_email() -> str:
    return f"{random_lower_string(32)}@{random_lower_string(32)}.com"

def random_name() -> str:
    return f"{random_lower_string(12)}.{random_lower_string(3)}"


