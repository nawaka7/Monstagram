# search.py
from math import ceil
import datetime

def display_search(database, sign_result):
    '''
    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    :return: None
    '''
    sign_id = sign_result[0]['id']
    posts = database['posts']

    looper = True
    while looper:
        print('''
    ====================
     MONSTAGRAM
     << SEARCH, %s >>
    ====================
            ''' % (sign_result[0]['name']['first']))
        hashword = input("#")
        search_result = hash_search(database, hashword)
        page_num = ceil(len(search_result) / 3)
        while True:
            page_choice = input("\t what page do you want to see? [1-%d]" % page_num)
            post_result = search_result[0+(page_num-1)*3:3*(page_num)]
            for post in post_result:
                name_search = list(database.user.find({"id":post['id']}))
                name = name_search[0]['name']['first'] + ' ' + name_search[0]['name']['last']
                timestamp = str(datetime.datetime.fromtimestamp(post['timestamp']))
                print(
                    '''
        %s
        %s
        %s
                    ''' % (name, timestamp, post['content']))
            choice = input("do you want to see more? [y/n] ")
            if choice == 'y':
                pass
            else:
                break
        choice = input("do you want to search more? [y/n] ")
        if choice == 'y':
            looper = True
        else:
            looper = False



def hash_search(database, hashword):
    '''
    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    :return: query result in list type
    '''
    post = database['post']
    result = list(database.posts.find({"content":{"$regex":"#"+hashword}}).sort([('timestamp', -1)]))
    return result
