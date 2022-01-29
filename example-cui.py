import os

import Ingress.account
import Ingress.login as l

def Pause():
    input("Press enter to continue...")

def main():
    login = l.Login()
    login.SetDatabase()
    while True:
        print("==============================================")
        print("=       Ingress Example CUI > Commands       =")
        print("=--------------------------------------------=")
        print("=    > login               > register        =")
        print("=--------------------------------------------=")
        print("=    > print                                 =")
        print("==============================================")
        UsrInput = input("Enter a command: ")
        if UsrInput == "login":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            status = login.Login(username, password, True)
            if status[0] == True:
                print("Login successful!")
            else:
                print(f"Login failed: {status[1]}")
            Pause()
        elif UsrInput == "register":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            status = login.Register(username, password, verbose=True)
            if status[0] == True:
                print("New account created")
            else:
                print(f"Register failed: {status[1]}")
            Pause()
        elif UsrInput == "print":
            login._ShowDatabase()
            Pause()
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()