import csv, re
BoolLog, UsernameInput,  PasswordInput, Duplicate, CorrectPass, Row = input('Do you want to [L]ogin or [R]egister? ').upper().strip() == 'R', "", "", False, False, 0
def CredentialAsk():
    global UsernameInput, PasswordInput, Duplicate, CorrectPass, Row
    Username()
    Password()
    if BoolLog: Password(PasswordInput, False)
    with open('./Credentials.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader]
        usernames, passwords = [row[0] for row in rows], [row[1] for row in rows]
        # passwords = [row[1] for row in rows]
    for x in range(0, len(usernames)):
        Duplicate, CorrectPass = UsernameInput == usernames[x],  PasswordInput == passwords[x]
        # CorrectPass = PasswordInput == passwords[x]
        Row = x
def ChangePassword():
    global Row
    if input("Do you want to change your password? [Y/N]").upper().strip() == 'Y':
        Password()
        with open('./Credentials.csv', 'r+') as file:
            for row in file: 
                if row[0] == UsernameInput: row[1] = PasswordInput
    else:
        exit("See you soon!")
def Username():
    global UsernameInput
    UsernameInput = input("Enter your username: ")
    while(not UsernameInput.isalnum() or 5 < len(UsernameInput) > 20):
        print("Username must be 5-20 characters, no spaces")
        UsernameInput = input("Enter your username: ")
def Password(oldpassword, changing = False):
    global PasswordInput
    PasswordInput = input("Enter your password: ")
    while(8 < len(PasswordInput) > 20 or PasswordInput.__contains__(" ") or not any(not c.isalnum() for c in PasswordInput) or not any(c.isnumeric() for c in PasswordInput) or not any(not c.isupper() for c in PasswordInput) or not any(not c.islower() for c in PasswordInput)):
        print("Password must be 8-20 characters, no spaces, with 1 upper character, lower character, digit, and special character")
        PasswordInput = input("Enter your password: ").lower()
    if changing:
        if PasswordInput != oldpassword: 
            print("Can't use the same passowrd")
            Password()
    elif(BoolLog):
        if PasswordInput == oldpassword: 
            print("Not the same password")
            Password()
while True:
    CredentialAsk()
    if (BoolLog):
        if(Duplicate): 
            print("This username is taken")
        else: 
            print(f"Welcome, {UsernameInput}!")
            with open('./Credentials.csv', 'a') as file:
                file.write(f"\n{UsernameInput},{PasswordInput}")
            break
    else:
        if(Duplicate and CorrectPass):
            print(f"Welcome, {UsernameInput}!")
            break
        elif(not Duplicate or not CorrectPass): 
            print("Your username/password is incorrect. Please try again")
            CredentialAsk()
ChangePassword()