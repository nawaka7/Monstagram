# Monstagram
--<MONSTAGRAM>--
A Simple Social Network Service Developed with Python and MongoDB
This SNS app consists of 7 python py files: main, user, wall, post, follow, chat, and search. 


<<MAIN.PY>>
1) A user will first see the mainpage in the main.py file when it is run
2) A new user needs to sign up by pressing number '2', which will lead the user to the signup function in user.py file
3) If the user has created ID and PW already, he/she/they may sign in, which will be allowed by the signin function in user.py file


<<USER.PY>>
1) The signup function receives input for ID, PW and basic personal information from the user. If the ID does not already exist in the database, the user can use the ID
2) The signin function compares the ID and PW the user typed with those in the database
3) The userpage function shows the user the within-app functions
3) The mystatus function brings up the data from the database to show the number of the followers and following members


<<WALL.PY>>
1) Wall allows you to write, delete, update or comment on your post. The functions related to the posts themselves run from post.py file.
2) Newsfeed demonstrates the posts of those you follow. The user can browse or comment on the posts


<<POST.PY>>
1) A post can be written(inserted), updated, or deleted in the database
2) A comment can be only written(inseted) or deleted in the database


<<FOLLOW.PY>>
1) The follow function begins with searching the member a user wants to follow. By entering the name or id, the query runs and its results are printed. The user may choose the member he/she/they want to follow
2) A user may unfollow from the member he/she/they follow.

<<SEARCH.PY>>
1) The Search page enables a user to search posts by a writer's first name


<<CHAT.PY>>
1) The Chat page enables two users to chat
2) The host and port of both server and client should be checked before running the chat.py file



Thank you.

Haechan Jun

