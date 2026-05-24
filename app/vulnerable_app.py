# Vulnerable code
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


# non-vulnerable code
# import os
# import subprocess
# import hashlib
# import ast

# # Secure password using environment variable
# password = os.getenv("APP_PASSWORD")

# # Safe command execution (no shell injection)
# def run_command(user_input):
#     try:
#         result = subprocess.run(
#             ["echo", user_input],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         return result.stdout.strip()
#     except Exception as e:
#         return str(e)

# # Safe evaluation (no eval)
# def calculate(expression):
#     try:
#         return ast.literal_eval(expression)
#     except Exception:
#         return "Invalid expression"

# # Strong hashing (SHA-256)
# def hash_password(pwd):
#     return hashlib.sha256(pwd.encode()).hexdigest()

# if __name__ == "__main__":
#     print(run_command("Hello Secure World"))
#     print(calculate("2+2"))
#     print(hash_password("test"))
