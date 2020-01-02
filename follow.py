# follow.py
from mg_chat import *

def follow(database, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    :param following: user id to follow
    :return: None
    '''
    """
    Get the followers.
    This function updates information that is user's followers or followings.
    Note that if a user asks following to someone, the follower's information should be also updated.
    Remember, you may regard duplicates and the situation that the follower does not exists.
    """
    user = database['user']
    sign_id = sign_result[0]['id']
    looper = True
    while looper:
        print('''
    ====================
    MONSTAGRAM
    << SEARCH USER TO FOLLOW >>
    ====================
        ''')
        search = input("user name or id: ").split()
        if len(search) == 2:
            query = list(database.user.find({"name.first": search[0],"name.last": search[1]}))
        elif len(search) == 1:
            query = list(database.user.find({"$or":[{"name.first": search[0]}, {"name.last": search[0]}, {"id":search[0]}]}))
        elif len(search) == 0:
            print("No Result")

        try:
            for i in range(len(query)):
                print('''
                %d) Name: %s \t ID: %s
                '''%(i, (query[i]['name']['first']+' '+query[i]['name']['last']), query[i]['id']))
        except:
            pass
        print('''
    ====================
    CHOOSE NUMBER FROM RESULT
    ====================
        ''')
        choice = input("[0-%d]"%(len(query)-1))
        choice = int(choice)

        try:
            database.user.update_one({"id":sign_result[0]['id']},{"$addToSet": {"following":query[choice]['id']}})
            database.user.update_one({"id":query[choice]['id']}, {"$addToSet": {"follower": sign_result[0]['id']}})
            print("followed %s" % query[choice]['id'])
        except:
            print("fail")
        looper = False

def unfollow(database, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    :param following: user id to follow
    :return: None
    '''
    """
    Unfollow someone.
    A user hopes to unfollows follwings.
    You can think that this function is the same as the follow but the action is opposite.
    The information apply to followings and followers both.
    Again, the confimation is helpful whether the user really wants to unfollow others.
    """
    user = database['user']
    sign_id = sign_result[0]['id']
    looper = True
    while looper:
        print('''
    ====================
    MONSTAGRAM
    << SEARCH USER TO UNFOLLOW >>
    ====================
        ''')
        search = input("user name or id: ").split()
        if len(search) == 2:
            query = list(database.user.find({"name.first": search[0],"name.last": search[1]}))
        elif len(search) == 1:
            query = list(database.user.find({"$or":[{"name.first": search[0]}, {"name.last": search[0]}, {"id":search[0]}]}))
        elif len(search) == 0:
            print("No Result")

        try:
            for i in range(len(query)):
                print('''
                %d) Name: %s \t ID: %s
                '''%(i, (query[i]['name']['first']+' '+query[i]['name']['last']), query[i]['id']))
        except:
            pass
        print('''
    ====================
    CHOOSE NUMBER FROM RESULT
    ====================
        ''')
        choice = input("[0-%d]" % (len(query)-1))
        choice = int(choice)

        try:
            database.user.update_one({"id":sign_result[0]['id']},{"$pull": {"following":query[choice]['id']}})
            database.user.update_one({"id":query[choice]['id']}, {"$pull": {"follower": sign_result[0]['id']}})
            print("followed %s" % query[choice]['id'])
        except:
            print("fail")
        looper = False
