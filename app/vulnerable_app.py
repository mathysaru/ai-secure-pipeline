import os

# 1. Hardcoded password (Vulnerability)
password = "admin123"

# 2. Command Injection
def run_command(user_input):
    os.system("echo " + user_input)

# 3. Insecure eval usage
def calculate(expression):
    return eval(expression)

# 4. Weak hashing
import hashlib
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

if __name__ == "__main__":
    run_command("Hello")
    print(calculate("2+2"))
    print(hash_password("test"))
