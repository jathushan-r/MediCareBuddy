import streamlit_authenticator as stauth

import database as db


usernames = ['saman', 'chathura', 'hasini', 'dasun', 'tharindu', 'lakshmi', 'rajesh', 'saranya', 'vijay', 'anitha']
firstnames = ["Saman", "Chathura", "Hasini", "Dasun", "Tharindu",  "Lakshmi", "Rajesh", "Saranya", "Vijay", "Anitha"]
lastnames =  ["Fernando", "Perera", "Silva", "Ratnayake", "Samarawickrama", "Sivasubramanian", "Venkatesh", "Balasubramanian", "Murali", "Shankar"]
ages = [30, 28, 35, 27, 40, 33, 45, 32, 28, 35]
phones = ["0777678678", "0777123123", "0712342345", "0765456789", "0759876543", "0723456789", "0781234567", "0768765432", "0706543210", "0719876543"]

passwords = ["abc123", "def456", "ghi789", "jkl012", "mno345", "pqr678", "stu901", "vwx234", "yz567", "123abc"]

hashed_passwords = stauth.Hasher(passwords).generate()


for (username, firstname,lastname,age,phone, hash_password) in zip(usernames, firstnames, lastnames,ages,phones, hashed_passwords):
    db.insert_user(username, firstname,lastname,age,phone, hash_password)