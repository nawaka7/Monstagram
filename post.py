#post.py
import time

def post_main(database, sign_result):
    '''
    :param database: pymongo.MongoClient['database']
    :param sign_result: database query result for sign_in
    '''
    looper = True
    while looper:
        print('''
    ====================
     MONSTAGRAM
     << NEW POST, %s >>
    ====================
        '''%sign_result[0]['name']['first'])
        content = input("what will you write? ")
        post_insert(database, content, sign_result)
        choice = input("do you want to write more? [y/n] ")
        if choice == 'y':
            pass
        else:
            looper = False

def post_insert(database, content, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param content: string
    :param sign_result: database query result for sign_in
    :return: post_id (object id)
    '''
    posts = database['posts']
    # Authorization
    sign_id = sign_result[0]['id']
    sign_obj_id = sign_result[0]['_id']
    authorization = False
    if sign_obj_id == list(database.user.find({"id": sign_id}))[0]['_id']:
        authorization = True
    else:
        print("Authorization falied")

    if authorization:
        try:
            ts = time.time()
            post_id = database.posts.insert({"id":sign_id,"content":content, "comment": [], 'timestamp':ts})
            if post_id:
                pass
            else:
                print("error occured during posting. sorry, try it again.")
            return post_id
        except:
            print("During the attempt to connect to the db, there occurred an unexpected error.")

def post_update(database, post_id, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param post_id: object_id of the post in mongodb
    :param sign_result: database query result for sign_in
    :return: boolean (result['updatedExisting'])
    '''
    posts = database['posts']
    new_content = input("update: ")
    sign_id = sign_result[0]['id']
    sign_obj_id = sign_result[0]['_id']
    authorization = False
    #Authorization
    if sign_obj_id == list(database.user.find({"id":sign_id}))[0]['_id']:
        authorization = True
    else:
        print("Authorization falied")

    if authorization:
        try:
            result = database.posts.update({"_id":post_id, 'id':sign_id},{"$set":{"content":new_content}})
            if result['updatedExisting'] == True:
                print('update successful')
            else:
                print('update failed')
            return result['updatedExisting']
        except:
            print("During the attempt to connect to the db, there occurred an unexpected error.")

def post_delete(database, post_id, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param post_id: string
    :param sign_result: database query result for sign_in
    :return: boolean
    '''
    posts = database['posts']
    # Authorization
    sign_id = sign_result[0]['id']
    sign_obj_id = sign_result[0]['_id']
    authorization = False
    if sign_obj_id == list(database.user.find({"id": sign_id}))[0]['_id']:
        authorization = True
    else:
        print("Authorization falied")

    if authorization:
        confirm = input("Are you sure you want to delete the post? [y/n] ")
        if confirm == 'y':
            try:
                posts.delete_one({'_id':post_id, "id":sign_id})
                result = posts.find({'_id':post_id})
                if bool(list(result)) == False:
                    print('delete successful')
                    return True
                else:
                    print('delete failed')
                    return False
            except:
                print("During the attempt to connect to the db, there occurred an unexpected error.")

def comment_insert(database, post_id, sign_result):
    '''

    :param database: pymongo.MongoClient['database']
    :param post_id: string
    :param sign_result: database query result for sign_in
    :return: boolean
    '''
    posts = database['posts']
    content = input("comment: ")
    if len(content) == 0:
        print("comment is empty")
        raise ValueError
    sign_id = sign_result[0]['id']
    sign_obj_id = sign_result[0]['_id']
    authorization = False

    try:
        ts = time.time()
        comment2write = {"id": sign_id, "name": sign_result[0]['name']['first'] + ' ' + sign_result[0]['name']['last'], "content": content, "timestamp": ts}
        # print(comment2write)
        post_id = database.posts.update_one({"_id":post_id},{"$push":{"comment":{"$each":[comment2write]}}})
        if post_id:
            return True
        else:
            print("error occured during commenting. sorry, try it again.")
            return False

    except:
        print("During the attempt to connect to the db, there occurred an unexpected error.")
        return False


def comment_delete(database, post_id, sign_result, comment_num):
    '''

    :param database: pymongo.MongoClient['database']
    :param post_id: string
    :param sign_result: database query result for sign_in
    :param comment_num: integer index of the comment in the array
    :return: boolean
    '''
    posts = database['posts']
    # Authorization
    sign_id = sign_result[0]['id']
    sign_obj_id = sign_result[0]['_id']
    authorization = False
    if sign_obj_id == list(database.user.find({"id": sign_id}))[0]['_id']:
        authorization = True
    else:
        print("Authorization falied")

    if authorization:
        confirm = input("Are you sure you want to delete the post? [y/n] ")
        if confirm == 'y':
            try:
                posts.update_one({'_id':post_id, "comment.id":sign_id,}, {"$set":{"comment.%d"%comment_num:"null"}})
                posts.update_one({'_id': post_id, }, {"$pull": {"comment":"null"}})
                print('delete successful')
                return True

            except:
                print("During the attempt to connect to the db, there occurred an unexpected error.")
                return False
