import bcrypt


def hash_password(plain_password):
    """
    Hash a password with a different salt everytime.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password, salt)

    return hashed
