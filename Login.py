BoolLog = input('Do you want to [L]ogin or [R]egister? ').upper().strip() == 'R'
print(BoolLog)
UsernameInput = ""
PasswordInput = ""
Duplicate = False
CorrectPass = False
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
def CredentialCheck():
    global Duplicate
    global CorrectPass
    with open('./UN.txt', 'r') as file: 
        usernames = [line.strip() for line in file]
    with open('./PW.txt', 'r') as file: 
        passwords = [line.strip() for line in file]
    for x in range(0, len(usernames)):
        Duplicate = UsernameInput == usernames[x]
        CorrectPass = PasswordInput == passwords[x]
CredentialAsk()
CredentialCheck()
if (BoolLog):
    if(Duplicate): 
        print("This username is taken")
        CredentialAsk()
        CredentialCheck()
    else: 
        print(f"Welcome, {UsernameInput}!")
        with open('./UN.txt', 'a') as file: 
            file.write(UsernameInput)
        with open('./PW.txt', 'a') as file: 
            file.write(PasswordInput)
else:
    if(Duplicate and CorrectPass): 
        print(f"Welcome, {UsernameInput}!")
    elif(not Duplicate or not CorrectPass): 
        print("Your username/password is incorrect. Please try again")
        CredentialAsk()
        CredentialCheck()