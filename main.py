# main.py
from pymongo import MongoClient
from mg_user import *

client = MongoClient()
mg_db = client['mg_db']


def mainpage(database):
    '''
    call signup() or signin()
    '''
    looper = True
    while looper:
        print('''
    ====================
    Welcome to Monstagram
    Your one and only SNS
    Sing up NOW for fun!!
    ====================
    1. Sign Up
    2. Sign In
    3. Exit
            ''')
        choice = input("Choose the menu: ")
        if choice == '1':
            signup(database)
        elif choice == '2':
            sign_result = signin(database)
            sign_id = sign_result[0]['id']
            userpage(database, sign_result)
        elif choice == "3":
            looper = False
            print('Bye')
        else:
            print("wrong choice")

if __name__ == "__main__":
    '''
    call mainpage()
    '''
    mainpage(mg_db)
