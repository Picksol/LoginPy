import csv, argon2, string, random
Type = argon2.Type
def PassHistory(username, new_password):
    try: 
        with open('./PasswordHistory.csv', 'r') as f: return any(row[0] == username and Var.verify(row[1], new_password) for row in csv.reader(f, delimiter=';') if row)
    except FileNotFoundError: return False
def CredentialAsk():
    global UsernameInput, PasswordInput, Duplicate, CorrectPass, Row, BoolLog
    Username()
    if BoolLog:
        while True:
            Password('register')
            PasswordInput_confirm = input("Confirm password: ")
            if PasswordInput == PasswordInput_confirm: break
            print("Passwords mismatch.")
    else: Password('login')
    with open('./Credentials.csv', 'r') as f:
        rows = list(csv.reader(f, delimiter=';'))
        for Row, row in enumerate(rows):
            if row and row[0] == UsernameInput:
                Duplicate, CorrectPass = True, Var.verify(row[1], PasswordInput)
                # Duplicate, CorrectPass = True, row[1] == PasswordInput
                return
        Duplicate, CorrectPass = False, False
def Password(mode, oldpassword=None):
    global PasswordInput
    while True:
        PasswordInput = input("Enter password: ")
        if mode in ['register', 'change']:
            if not (8 <= len(PasswordInput) <= 20 and " " not in PasswordInput and any(c.isupper() for c in PasswordInput) and any(c.islower() for c in PasswordInput) and any(c.isdigit() for c in PasswordInput) and any(not c.isalnum() for c in PasswordInput)):
                print("Password must be 8-20 chars, no spaces, and include: upper, lower, digit, special char")
                continue
            if mode == 'change' and PasswordInput == oldpassword:
                print("Cannot reuse old password")
                continue
        break
def Random5(length=5): return ''.join(random.choice(string.ascii_letters) for _ in range(length))
def ChangePassword():
    global UsernameInput, PasswordInput
    if input("Change password? [Y/N] ").upper().strip() == 'Y':
        while True:
            old_password_input = input("Enter old password: ")
            with open('./Credentials.csv', 'r') as f: StoredPassword = next((row[1] for row in csv.reader(f, delimiter=';') if row and row[0] == UsernameInput), None)
            if StoredPassword is None:
                print("User not found.")
                return
            if Var.verify(StoredPassword, old_password_input): break
            print("Incorrect old password.")
        while True:
            Password('change', StoredPassword)
            new_password_confirm = input("Confirm new password: ")
            if PasswordInput == new_password_confirm:
                if PassHistory(UsernameInput, PasswordInput): print("Cannot use old password.")
                else: break
            else: print("Passwords mismatch.")
        with open('./Credentials.csv', 'r') as f: rows = list(csv.reader(f,delimiter=';'))
        with open('./Credentials.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for row in rows:
                if row and row[0] == UsernameInput:
                    RecordedPassword = row[1]
                    PasswordInput = Var.hash(PasswordInput)
                    row[1] = PasswordInput
                    with open('./PasswordHistory.csv', 'a', newline='') as history_file: csv.writer(history_file, delimiter=';').writerow([UsernameInput, RecordedPassword])
                writer.writerow(row)
        print("Password changed!")
    else: exit("Logging out...")
def Username():
    global UsernameInput
    while True:
        UsernameInput = input("Enter username: ")
        if UsernameInput.isalnum() and 5 <= len(UsernameInput) <= 20: break
        print("Username must be 5-20 chars, alphanumeric only.")
BoolLog, UsernameInput, PasswordInput, Duplicate, CorrectPass, Row, LoginAttempts, Var = input('Login [L] or Register [R]? ').upper().strip() == 'R', "", "", False, False, 0, 5, argon2.PasswordHasher(type=Type.ID)
while LoginAttempts>0:
    CredentialAsk()
    if BoolLog:
        if Duplicate: print("Username taken")
        else:
            print(f"Welcome, {UsernameInput}!")
            with open('./Credentials.csv', 'a', newline='') as f: csv.writer(f, delimiter=';').writerow([UsernameInput, Var.hash(password=PasswordInput)])
            break
    elif Duplicate and CorrectPass:
        print(f"Welcome, {UsernameInput}!")
        break
    else:
        LoginAttempts -= 1
        print(f"Incorrect username/password. You have {LoginAttempts} left")
ChangePassword()