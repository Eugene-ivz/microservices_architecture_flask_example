import bcrypt


def verify_password(plain_password, hashed_password):
    '''
    check hash of password with saved hash
    
    :param plain_password: password
    :param hashed_password: saved hash of password
    :return: bool
    
    '''
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password):
    '''
    get hash of password
    
    :param password: password
    :return: password hash
    
    '''
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
