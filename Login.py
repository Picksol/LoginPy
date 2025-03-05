import csv
BoolLog, UsernameInput, PasswordInput, Duplicate, CorrectPass, Row = input('Do you want to [L]ogin or [R]egister? ').upper().strip() == 'R', "", "", False, False, 0
def PassHistory(username, new_password):
    try:
        with open('./PasswordHistory.csv', 'r') as history_file:
            csv_reader_history = csv.reader(history_file)
            for row in csv_reader_history:
                if row and row[0] == username and row[1] == new_password: return True
    except FileNotFoundError: return False
    return False
def CredentialAsk():
    global UsernameInput, PasswordInput, Duplicate, CorrectPass, Row
    Username()
    if BoolLog:
        Password('register')
        PasswordInput_confirm = input("Confirm your password: ")
        while PasswordInput != PasswordInput_confirm:
            print("Passwords do not match.")
            Password('register')
            PasswordInput_confirm = input("Confirm your password: ")
    else: Password('login')
    with open('./Credentials.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader]
        usernames, passwords = [row[0] for row in rows], [row[1] for row in rows]
    for x in range(0, len(usernames)):
        Duplicate, CorrectPass = UsernameInput == usernames[x], PasswordInput == passwords[x]
        Row = x
def Password(mode, oldpassword=None):
    global PasswordInput
    PasswordInput = input("Enter your password: ")
    if mode == 'register' or mode == 'change':
        while (8 > len(PasswordInput) or len(PasswordInput) > 20 or " " in PasswordInput or not any(c.isupper() for c in PasswordInput) or not any(c.islower() for c in PasswordInput) or not any(c.isdigit() for c in PasswordInput) or not any(not c.isalnum() for c in PasswordInput)):
            print("Password must be 8-20 characters, no spaces, with 1 upper character, lower character, digit, and special character")
            PasswordInput = input("Enter your password: ")
        if mode == 'change' and PasswordInput == oldpassword:
            print("Can't use your old password")
            Password('change', oldpassword)
    elif mode == 'login': pass
def ChangePassword():
    global Row, UsernameInput, PasswordInput
    if input("Do you want to change your password? [Y/N]").upper().strip() == 'Y':
        while True:
            OldPassword = input("Enter your existing password: ")
            StoredPassword = None
            with open('./Credentials.csv', 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row and row[0] == UsernameInput:
                        StoredPassword = row[1]
                        break
            if StoredPassword is None:
                print("User not found. Cannot change password.")
                return
            if OldPassword == StoredPassword: break
            else: print("Incorrect existing password. Please try again.")
        while True:
            Password('change', StoredPassword)
            NewPassword = input("Confirm your new password: ")
            if PasswordInput == NewPassword:
                if PassHistory(UsernameInput, PasswordInput):
                    print("Cannot use an old password. Please choose a new one.")
                    continue
                else: break
            else:
                print("New passwords do not match. Please try again.")
                continue
        with open('./Credentials.csv', 'r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
        with open('./Credentials.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            for r_index, row in enumerate(rows):
                if row and row[0] == UsernameInput:
                    RecordedPassword = rows[r_index][1]
                    rows[r_index][1] = PasswordInput
                    with open('./PasswordHistory.csv', 'a', newline='') as history_file:
                        csv_writer_history = csv.writer(history_file)
                        csv_writer_history.writerow([UsernameInput, RecordedPassword])
                    break
            csv_writer.writerows(rows)
        print("Password changed successfully!")
    else: exit("Logging out... See you soon!")
def Username():
    global UsernameInput
    UsernameInput = input("Enter your username: ")
    while (not UsernameInput.isalnum() or 5 > len(UsernameInput) or len(UsernameInput) > 20):
        print("Username must be 5-20 characters, no spaces")
        UsernameInput = input("Enter your username: ")
while True:
    CredentialAsk()
    if (BoolLog):
        if (Duplicate): print("This username is taken")
        else:
            print(f"Welcome, {UsernameInput}!")
            with open('./Credentials.csv', 'a', newline='') as file:
                file.write(f"{UsernameInput},{PasswordInput}")
            break
    else:
        if (Duplicate and CorrectPass):
            print(f"Welcome, {UsernameInput}!")
            break
        elif (not Duplicate or not CorrectPass): print("Your username/password is incorrect. Please try again")
ChangePassword()