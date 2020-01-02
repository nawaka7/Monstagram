# wall.py
import datetime
from math import ceil
from mg_post import *

def getWall(database,sign_result):
    '''
    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    '''
    """
    Display your posts. Of course, get all posts would be fine.
    However, the function that supports displaying a few posts, e.g., five posts, looks much better than displaying all posts.
    Remind the lab8 that dealt with cursor.
    """
    sign_id = sign_result[0]['id']
    posts = database['posts']
    page_num = ceil(database.posts.find({"id":sign_id}).count() / 3 )
    looper = True
    while looper:
        print('''
    ====================
     MONSTAGRAM
     << MY WALL, %s >>
    ====================
    There are %d pages.
        ''' % (sign_result[0]['name']['first'], page_num))
        page_choice = int(input("\t what page do you want to see? [1-%d]"%page_num))
        post_result = list(database.posts.find({"id": sign_id}).sort([('timestamp',-1)]).skip((page_choice-1)*3).limit(3))
        post_id_bucket = []
        for i in range(len(post_result)):
            post = post_result[i]
            name = sign_result[0]['name']['first'] + ' ' + sign_result[0]['name']['last']
            post_id_bucket.append(post['_id'])
            timestamp = str(datetime.datetime.fromtimestamp(post['timestamp']))
            print(
            '''
    %d)
    %s
    %s
    %s
            '''%(i, name, timestamp, post['content']))
        choice = input("1. Del \t 2. Update \t 3.Comment \t 4. Next \n")
        if choice == '1':
            del_choice = input("Which post on the page [0-%d]"%(len(post_result)-1))
            try:
                post_id = post_id_bucket[int(del_choice)]
            except IndexError:
                print("try again")
                del_choice = input("Which post on the page [0-%d]" % (len(post_result) - 1))
            post_delete(database, post_id, sign_result)
        elif choice == '2':
            up_choice = input("Which post on the page [0-%d]"%len(len(post_result)-1))
            try:
                post_id = post_id_bucket[int(up_choice)]
            except IndexError:
                print("try again")
                up_choice = input("Which post on the page [0-%d]" % len(len(post_result) - 1))
            post_update(database, post_id, sign_result)
        elif choice == '3':
            com_choice = input("Which post on the page [0-%d]"%(len(post_result)-1))
            try:
                post_id = post_id_bucket[int(com_choice)]
            except IndexError:
                print("try again")
                com_choice = input("Which post on the page [0-%d]" % (len(post_result) - 1))
            post2comment = list(database.posts.find({"_id":post_id}))[0]
            if post2comment["comment"]:
                for i in range(len(post2comment["comment"])):
                    comm = post2comment["comment"][i]
                    print(
                        '''
                %d)
                %s
                %s
                %s
                        ''' % (i, comm["name"], comm["timestamp"], comm["content"]))
            print('''
                1.Write \t 2.Delete \t 3.Exit
                   ''')
            choice = input('[1-3] ')
            if choice == '1':
                comment_insert(database, post_id, sign_result)
                choice2 = input("do you want to see more? [y/n] ")
                if choice2 == 'y':
                    looper = True
                else:
                    looper = False
            elif choice == '2':
                choice_com_del = input("which comment? [0-%d] "%(len(post2comment["comment"])-1))
                try:
                    comment_num = int(choice_com_del)
                except ValueError:
                    print("error: integer only")
                comment_delete(database, post_id, sign_result, comment_num)
            elif choice == '3':
                more_choice = input("do you want to see more? [y/n] ")
                if more_choice == 'y':
                    looper = True
                else:
                    looper = False
        else:
            choice2 = input("do you want to see more? [y/n] ")
            if choice2 == 'y':
                looper = True
            else:
                looper = False

def getNewsfeed(database,sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    '''
    sign_id = sign_result[0]['id']
    posts = database['posts']
    follows = list(database.user.find({"id":sign_id}))[0]["following"]
    follows.append(sign_id)
    page_num = ceil(database.posts.find({"id":{"$exists":follows}}).count() / 3)
    looper = True
    while looper:
        print('''
    ====================
     MONSTAGRAM
     << NEWSFEED, %s >>
    ====================
    There are %d pages.
            ''' % (sign_result[0]['name']['first'], page_num))
        page_choice = int(input("\t what page do you want to see? [1-%d]" % page_num))
        post_result = list(
            database.posts.find({"id": {"$exists": follows}}).sort([('timestamp', -1)]).skip((page_choice - 1) * 3).limit(3))
        post_id_bucket = []
        for i in range(len(post_result)):
            post = post_result[i]
            post_id_bucket.append(post['_id'])
            name_search = list(database.user.find({"id":post['id']}))
            name = name_search[0]['name']['first'] + ' ' + name_search[0]['name']['last']
            timestamp = str(datetime.datetime.fromtimestamp(post['timestamp']))
            print(
                '''
    %d
    %s
    %s
    %s
                ''' % (i, name, timestamp, post['content']))

        choice = input("1. Comment \t 2. Next \n")
        if choice == '1':
            com_choice = input("Which post on the page [0-%d]" % (len(post_result) - 1))
            try:
                post_id = post_id_bucket[int(com_choice)]
            except IndexError:
                print("try again")
                com_choice = input("Which post on the page [0-%d]" % (len(post_result) - 1))
            post2comment = list(database.posts.find({"_id": post_id}))[0]
            if post2comment["comment"]:
                for i in range(len(post2comment["comment"])):
                    comm = post2comment["comment"][i]
                    print(
                        '''
                %d)
                %s
                %s
                %s
                        ''' % (i, comm["name"], comm["timestamp"], comm["content"]))
            print('''
                1.Write \t 2.Delete \t 3.Exit
                   ''')
            choice = input('[1-3] ')
            if choice == '1':
                comment_insert(database, post_id, sign_result)
                choice2 = input("do you want to see more? [y/n] ")
                if choice2 == 'y':
                    looper = True
                else:
                    looper = False
            elif choice == '2':
                choice_com_del = input("which comment? [0-%d] "%(len(post2comment["comment"])-1))
                try:
                    comment_num = int(choice_com_del)
                except ValueError:
                    print("error: integer only")
                comment_delete(database, post_id, sign_result, comment_num)
            elif choice == '3':
                more_choice = input("do you want to see more? [y/n] ")
                if more_choice == 'y':
                    looper = True
                else:
                    looper = False

        elif choice == '2':
            more_choice = input("do you want to see more? [y/n] ")
            if more_choice == 'y':
                looper = True
            else:
                looper = False
