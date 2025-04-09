import argon2, string, random, pyodbc
def PassHistory(username, new_password):
    try: 
        return any(row[0] == username and VeryBerry(row[1], new_password) for row in cur.execute('select * from PasswordHistory').fetchall() if row)
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
    for row in cur.execute('select * from Credentials').fetchall():
        if row and row[0] == UsernameInput:
            Duplicate, CorrectPass = True, VeryBerry(row[1], PasswordInput)
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
def VeryBerry(Par1, Par2NotGolf):
    try: Var.verify(Par1, Par2NotGolf)
    except: return False
    return True
def Random8(length=8): return (''.join(random.choice(string.ascii_letters) for _ in range(length))).encode('utf-8')
def ChangePassword():
    global UsernameInput, PasswordInput
    if input("Change password? [Y/N] ").upper().strip() == 'Y':
        while True:
            old_password_input = input("Enter old password: ")
            StoredPassword = next((row[1] for row in cur.execute('select * from Credentials').fetchall() if row and row[0] == UsernameInput), None)
            if StoredPassword is None:
                print("User not found.")
                return
            try:
                if VeryBerry(StoredPassword, old_password_input): break
            except:
                print("Incorrect old password.")
        while True:
            Password('change', StoredPassword)
            new_password_confirm = input("Confirm new password: ")
            if PasswordInput == new_password_confirm:
                if PassHistory(UsernameInput, PasswordInput): print("Cannot use old password.")
                else: break
            else: print("Passwords mismatch.")
        for row in cur.execute('select * from Credentials').fetchall():
            if row and row[0] == UsernameInput:
                RecordedPassword = row[1]
                PasswordInput = Var.hash(PasswordInput, salt=(f'{Random8()}Love').encode('utf-8'))
                row[1] = PasswordInput
                cur.execute("INSERT INTO PasswordHistory (Username, Password) VALUES (?,?)", (UsernameInput, RecordedPassword))
            cur.execute("UPDATE Credentials SET Password=? WHERE Username=?", (PasswordInput, UsernameInput))
            cur.commit()
        print("Password changed!")
    else: exit("Logging out...")
def Username():
    global UsernameInput
    while True:
        UsernameInput = input("Enter username: ")
        if UsernameInput.isalnum() and 5 <= len(UsernameInput) <= 20: break
        print("Username must be 5-20 chars, alphanumeric only.")
BoolLog, UsernameInput, PasswordInput, Duplicate, CorrectPass, Row, LoginAttempts, Var, cur = input('Login [L] or Register [R]? ').upper().strip() == 'R', "", "", False, False, 0, 5, argon2.PasswordHasher(), pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' r'DBQ=p:\Access\LoginPy2.accdb;' r'PWD=JacobHoover').cursor()
while LoginAttempts>0:
    CredentialAsk()
    if BoolLog:
        if Duplicate: print("Username taken")
        else:
            print(f"Welcome, {UsernameInput}!")
            cur.execute("INSERT INTO Credentials (Username, Password) VALUES (?,?)", (UsernameInput, Var.hash(password=PasswordInput, salt=(f'{Random8()}Love').encode('utf-8'))))
            cur.commit()
            break
    elif Duplicate and CorrectPass:
        print(f"Welcome, {UsernameInput}!")
        break
    else:
        LoginAttempts -= 1
        print(f"Incorrect username/password. You have {LoginAttempts} left")
if LoginAttempts>0: ChangePassword()