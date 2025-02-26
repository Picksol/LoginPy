import csv
BoolLog, UsernameInput,  PasswordInput, Duplicate, CorrectPass, Row = input('Do you want to [L]ogin or [R]egister? ').upper().strip() == 'R', "", "", False, False, 0
def CredentialAsk():
    global UsernameInput
    global PasswordInput
    UsernameInput = input("Enter your username: ")
    while(not UsernameInput.isalnum() or 5 < len(UsernameInput) > 20):
            print("Username must be 5-20 characters, no spaces")
            UsernameInput = input("Enter your username: ")
    PasswordInput = input("Enter your password: ")
    while(8 < len(PasswordInput) > 20 or PasswordInput.__contains__(" ") or not any(not c.isalnum() for c in PasswordInput) or not any(c.isnumeric() for c in PasswordInput) or not (not c.isupper() for c in PasswordInput) or not (not c.islower() for c in PasswordInput)):
            print("Password must be 8-20 characters, no spaces, with 1 upper character, lower character, digit, and special character")
            PasswordInput = input("Enter your password: ").lower()
    global Duplicate
    global CorrectPass
    with open('./Credentials.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader]
        usernames = [row[0] for row in rows]
        passwords = [row[1] for row in rows]
    for x in range(0, len(usernames)):
        Duplicate = UsernameInput == usernames[x]
        CorrectPass = PasswordInput == passwords[x]
def ChangePassword():
    global Row
    if input("Do you want to change your password? [Y/N]").upper().strip() == 'Y':
        
    else:
        pass
CredentialAsk()
if (BoolLog):
    if(Duplicate): 
        print("This username is taken")
        CredentialAsk()
    else: 
        print(f"Welcome, {UsernameInput}!")
        with open('./Credentials.csv', 'a') as file:
            file.write(f"\n{UsernameInput},{PasswordInput}")
else:
    if(Duplicate and CorrectPass): print(f"Welcome, {UsernameInput}!")
    elif(not Duplicate or not CorrectPass): 
        print("Your username/password is incorrect. Please try again")
        CredentialAsk()
ChangePassword()