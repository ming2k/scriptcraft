import secrets
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

if __name__ == "__main__":
    password_length = int(input("请输入密码长度: "))
    generated_password = generate_password(password_length)
    print("生成的密码:", generated_password)
