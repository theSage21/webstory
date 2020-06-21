import os
import hashlib
import shutil

password = input("Please enter a password: ")
new_path = hashlib.sha512(password.encode()).hexdigest()

shutil.rmtree("www")
os.mkdir("www")
shutil.copytree("src/secret", f"www/{new_path}")
shutil.copy("src/index.html", f"www/index.html")
