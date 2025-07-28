import hashlib
method = hashlib.sha256()
method.update(b'password')
a = method.hexdigest()
print(b'password')
print(a)
