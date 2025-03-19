import hashlib

password_value = 'sgf'


hashlib.sha256(password_value.encode('utf-8')).hexdigest()