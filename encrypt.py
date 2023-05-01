import bcrypt
pwd="\\x243262243132247670756b526e6a474e384b56346d7635376e316e446538425a48416e3535444d37775147566956525333302f64426f6c4e51514e4f"
real_pass="dumm4"

def hash_pass(password:str):
    salt=bcrypt.gensalt()
    bytes=password.encode('utf-8')
    hash_pass=bcrypt.hashpw(bytes, salt)
    return hash_pass.decode('utf-8')

def check_pass(user_pwd:str, pwd:str):
    user_bytes=user_pwd.encode('utf-8')
    pwd=pwd.encode('utf-8')
    result=bcrypt.checkpw(user_bytes,pwd)
    return result

#print(str(hash_pass(real_pass)))
#print(check_pass(real_pass, pwd))