# user.py
from pymongo import MongoClient
from mg_post import *
from mg_wall import *
from mg_follow import *
from mg_search import *

client = MongoClient()
mg_db = client['mg_db']
user = mg_db['user']

def signup(database):
    '''
    1. Get his/her information.
    2. Check if his/her password is equal. Confirm the password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''
    #bring database
    user = database['user']
    user_database = []
    for i in database.user.find({},{"id":1}):
        user_database.append(i['id'])
    # print(user_database)
    #GUI
    print('''
    ====================
    << SING UP PAGE >>
    ====================
    ''')

    #user info
    looper = True
    while looper:
        id = input("what do you want for your id? ")
        id_confirm = input("your id is : %s [y/n]"%id)
        if id_confirm == 'y':
            if id not in user_database:
                print("Your id is ", id)
                looper = False
            else:
                print("Your id exists already. Try again")
        else:
            pass

    looper = True
    while looper:
        pw = input("what's your password? ")
        pw_confirm = input("type again to confirm: ")
        if pw == pw_confirm:
            print("your password is ", pw)
            looper = False
        else:
            print("your password doesn't match. Try it again")


    first = input("What's your first name? ")
    last = input("What's your last name? ")
    age = int(input("How old are you? "))
    school = input("what is the last school you went to? ")
    print('''
    Your first name: %s
    Your last name: %s
    Your age: %d
    Your school: %s        
    '''%(first,last,age,school))

    #insert
    try:
        result = database.user.insert_one({"id":id, "pw":pw, "name":{"first":first,"last":last},"age":age,"school":school,
                                       "follower":[], "following":[]})
    except:
        print("Can't read the database.")

    if result.inserted_id:
        print("Thank you for signing up")
    else:
        print("Sorry. The server is temporarily not working")


def signin(database):
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''
    #bring database
    user = database['user']

    #GUI
    print('''
    ====================
    << SIGN IN PAGE >>
    ====================
    ''')

    #signin
    looper = True
    while looper:
        sign_id = input("ID: ")
        sign_pw = input("PW: ")
        try:
            sign_result = list(database.user.find({"id":sign_id,"pw":sign_pw}))
            if sign_result:
                print("Welcome! ", sign_result[0]['name']['first'], sign_result[0]['name']['last'])
                looper = False
            else:
                print("Your information is not correct. Try again")
        except:
            print("Can't read the database.")

    return sign_result


def mystatus(database, sign_result):
    '''
    print user profile, # followers, and # followings
    '''
    print('''
    ====================
    << MY STATUS, %s >>
    ====================
    Followers: %d
    Following: %d
    %s
    * exit [x]
    '''%(sign_result[0]['name']['first'],len(sign_result[0]['follower']),len(sign_result[0]['following']),sign_result[0]['following']))
    looper = True
    while looper:
        choice = input("exit[x] ")
        if choice == 'x':
            looper = False

def userpage(database, sign_result):
    '''
    user page
    '''
    sign_id = sign_result[0]['id']
    looper = True
    while looper:
        print('''
    ====================
    MONSTAGRAM
    << USER PAGE, %s >>
    ====================
    1. My Status
    2. News Feed
    3. Wall
    4. Post
    5. Follow
    6. Unfollow
    7. Search
    8. Chat
    9. Logout
        '''
          % sign_result[0]['name']['first'])

        choice = input("Choose the menu [1-9]: ")
        if choice == '1':
            mystatus(database, sign_result)
        elif choice == '2':
            getNewsfeed(database, sign_result)
        elif choice == '3':
            getWall(database, sign_result)
        elif choice == '4':
            post_main(database, sign_result)
        elif choice == '5':
            follow(database, sign_result)
        elif choice == '6':
            unfollow(database, sign_result)
        elif choice == '7':
            display_search(database, sign_result)
        elif choice == '8':
            chat(database, sign_result)
        elif choice == '9':
            looper = False
            print('Log Out')
        else:
            print("Unprepared service")
