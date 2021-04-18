#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import sys
import sqlite3
import pickle
from collections import Counter
import time
import traceback
import pymongo



#-----------------------------------------------------------------------------#
#                                Functions                                    #
#-----------------------------------------------------------------------------#

def fill_element_dictionaries():
    for cb in master_book_list:
        if cb.ID in ID_dict.keys():
            ID_dict[cb.ID].append(cb)
        else:
            ID_dict[cb.ID] = [cb]

        if cb.title in TITLE_dict.keys():
            TITLE_dict[cb.title].append(cb)
        else:
            TITLE_dict[cb.title] = [cb]

        if cb.href in HREF_dict.keys():
            HREF_dict[cb.href].append(cb)
        else:
            HREF_dict[cb.href] = [cb]

## Helper function to get a master node from the repeated list
## Prioritize: 1) fully defined nodes 2) nodes with the most raters pointing to them
def identify_master_book(repeat_list):
    master_node = None

    # 1) fully defined node
    for i,node in enumerate(repeat_list):
        if node.reviewers != 0:
            master_node = node
            ## Let's fix the reviewer error!
            ## add all reviewers from a fully defined book as a rater as well!
            for cur_reviewer in master_node.reviewers:
                master_node.raters.append( (cur_reviewer, 4.5) )
            return master_node, i

    # 2) node with most raters pointing to it
    mast_indx = 0
    for i,node in enumerate(repeat_list):
        if not master_node:
            master_node = node
        elif len(node.raters) > len(master_node.raters):
            master_node = node
            mast_indx = i
    return node, mast_indx




#### MONGO DB FUNCTIONS ######

def Mongo_check_existance(id_string, ID_to_check):
    if id_string == 'users':
        query = { "_id": ID_to_check }
        mydoc = userCol.find(query)
        for i in mydoc:
            return True
        else:
            return False

    else:
        Exception("update function 'Mongo_check_existance' to include other checks!!")


def Mongo_add_book_node(book_node):
    global global_book_errors
    book_raters = [i[0].ID for i in book_node.raters]
    rater_ratings = [i[1] for i in book_node.raters]
    bookJSON = {"_id": book_node.ID, "title": book_node.title, "href": book_node.href, "author": book_node.author, \
              "meta": book_node.meta, "details": book_node.details, "series": book_node.series, \
              "summary": book_node.summary, "imageSource": book_node.imageSource, "imageBinary": book_node.imageBinary, \
              "fullParameter": book_node.has_full_params, "ratersID": book_raters, "ratersRating": rater_ratings}

    try:
      x = bookCol.insert_one(bookJSON)
    except:
      print('error occured on adding {0}!'.format(book_node.title))
      global_book_errors += 1


def Mongo_add_user_node_list(user_list):
    for cur_user in user_list:
      ## First check if the user is already in DB
      ## IF not, then add it
      if Mongo_check_existance('users', cur_user.ID):
        continue
      else:
        Mongo_add_user_node(cur_user)

def Mongo_add_user_node(user_node):
    global global_book_errors
    user_books = [i[0].ID for i in user_node.books]
    rater_ratings = [i[1] for i in user_node.books]
    userSON = {"_id": user_node.ID, "name": user_node.name, "link": user_node.link, \
                "ratingsLink": user_node.ratingsLink, "booksID": user_books, "raterRatings": rater_ratings}

    try:
      x = userCol.insert_one(userSON)
    except:
      print('error occured on adding {0}!'.format(user_node.name))
      global_book_errors += 1



def Mongo_first_order_search(book_id):
    book_JSON = Mongo_get_book_JSON(book_id)

    ## Now that we have the book JSON, go through and find all of the users linked to the book and get their JSON
    ## For each of the users, look at their linked users' books, and store those books in a dictionary
    ## Accumulate rating value in that dictionary
    ## At the end, sort the dicionary and return highest value book (besides this one)
    userID_list = book_JSON['ratersID']
    userRatings_list = book_JSON['ratersRating']

    first_order_dict = {}
    for i, curUserID in enumerate(userID_list):
        if i % 100 == 0:
            print(i)

        user_JSON = Mongo_get_user_JSON(curUserID)

        booksID_list = user_JSON['booksID']
        booksRatings_list = user_JSON['raterRatings']

        for j, curBookID in enumerate(booksID_list):
            first_order_dict[curBookID] = first_order_dict.get(curBookID, 0) + userRatings_list[i]*booksRatings_list[j]

    sorted_IDs = sorted(first_order_dict.keys(), key = first_order_dict.get, reverse = True)
    return Mongo_get_book_JSON(sorted_IDs[1])


def Mongo_get_book_JSON(book_id):
    return [*bookCol.find({"_id": book_id})][0]

def Mongo_get_user_JSON(user_id):
    return [*userCol.find({"_id": user_id})][0]


#-----------------------------------------------------------------------------#
#                                  PreMAIN                                    #
#-----------------------------------------------------------------------------#

#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["books"]
#
# addStuff = False
#
# if addStuff:
#     mylist = { "_id": book_node.ID, "title": book_node.title, "href": book_node.href, "author": book_node.author, \
#         "meta": book_node.meta, "details": book_node.details, "series": book_node.series, \
#         "summary": book_node.summary, "imageSource": book_node.imageSource, "imageBinary": book_node.imageBinary, \
#         "fullParameter": book_node.has_full_params}
#
#
#     x = mycol.insert_one(mylist)
#     #print list of the _id values of the inserted documents:
#     print(x.inserted_ids)
#     x = mycol.find_one()
#     print(x)
#
#
#

# if addStuff:
#   mylist = [
#     { "_id": 21, "name": "John", "address": "Highway 37"},
#     { "_id": 22, "name": "Peter", "address": "Lowstreet 27"},
#     { "_id": 23, "name": "Amy", "address": "Apple st 652"},
#     { "_id": 24, "name": "Hannah", "address": "Mountain 21"},
#     { "_id": 25, "name": "Michael", "address": "Valley 345"},
#     { "_id":26, "name": "Sandy", "address": "Ocean blvd 2"},
#     { "_id": 27, "name": "Betty", "address": "Green Grass 1"},
#     { "_id": 28, "name": "Richard", "address": "Sky st 331"},
#     { "_id": 29, "name": "Susan", "address": "One way 98"},
#     { "_id": 210, "name": "Vicky", "address": "Yellow Garden 2"},
#     { "_id": 211, "name": "Ben", "address": "Park Lane 38"},
#     { "_id": 212, "name": "William", "address": "Central st 954"},
#     { "_id": 213, "name": "Chuck", "address": "Main Road 989"},
#     { "_id": 214, "name": "Viola", "address": "Sideway 1633"}
#   ]
#
#   x = mycol.insert_many(mylist)
#   #print list of the _id values of the inserted documents:
#   print(x.inserted_ids)
#   x = mycol.find_one()
#   print(x)
#


# for x in mycol.find():
#   print(x)








#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#

if __name__ == "__main__":

    user_in = input('Do you want to re-run booklist reconsolidation? (1 for yes)')

    if int(user_in) == 1:

        ## Load in pickled data
        startTime = time.time()

        sys.setrecursionlimit(100000)
        file_str = 'masterUserList_ref.pkl'
        with open('master_checkpoints/' + file_str, 'rb') as f:  # Python 3: open(..., 'rb')
            master_user_list, master_user_IDs = pickle.load(f)


        ## FIRST FIX THE NONE ISSUE
        ## If a user rates a book as "None", then set that rating to be 2.5 by default
        None_sum = 0
        for cur_usr in master_user_list:
            for indxx, jj in enumerate(cur_usr.books):
                if jj[1] is None:
                    tmp_jj = list(jj)
                    tmp_jj[1] = 2.5
                    jj = tuple(tmp_jj)
                    cur_usr.books[indxx] = jj
                    None_sum += 1
        print(None_sum)


        master_book_list = []
        master_book_IDs = []
        for i,cur_user in enumerate(master_user_list):
            if i % 1000 == 0:
                print('On user {0}'.format(i))

            for cur_book in cur_user.books:
                master_book_list.append(cur_book[0])

            for cur_book_IDs in cur_user.books_ID:
                master_book_IDs.append(cur_book_IDs)



        ## Report metrics for book effeciency

        c_users = Counter(master_user_IDs)
        c_books = Counter(master_book_IDs)

        # Let's report the effeciency
        user_eff = len(c_users.values()) / len(master_user_IDs)
        book_eff = len(c_books.values()) / len(master_book_IDs)

        print()
        print('Collected user effeciency = {0:0.2f}%'.format(user_eff * 100))
        print('Collected book effeciency = {0:0.2f}%'.format(book_eff * 100))

        # Let's look through all books and check how many are fully defined to double check that we have everything
        full_books = 0
        full_books_dict = {}
        for cur_book in master_book_list:
            if cur_book.reviewers != 0:
                full_books += 1
                if cur_book.ID in full_books_dict.keys():
                    full_books_dict[cur_book] += 1
                else:
                    full_books_dict[cur_book] = 1

        print('Have {0} full books collected, expect 718'.format(full_books))
        print('Have {0} full books collected excluding repeated books, expect 718'.format(len(full_books_dict.keys())))
        ## Stop here to look at it lol
        print("loaded in master user list")



        ## Consolidate books! Currently, user effeciency is 100%, book effeciency is low
        ##      --> Create a dictionary for each matchable element we are looking for
        ##              -ID
        ##              -HREF
        ##              -Title
        ##      --> do an OR operation for all books matching a current element
        ##      --> Migrate book parameters to a "master book"
        ##              -Prefer fully defined bok
        ##              -Secondly prefer book with the most reviewers
        ##          -For each book migrated, need to update pointers from user reviewers to new consolidated master node
        ID_dict = {}
        HREF_dict = {}
        TITLE_dict = {}
        fill_element_dictionaries()
        print('Element dictionaries filled...')

        # Based on what I assume to be true, books are more strongly linked to the title string
        # Let's just use that to construct our repeated books list
        distilled_titles = TITLE_dict.keys() # these are the "unique" titles of our dataset
        master_consolidated_book_list = []
        master_consolidated_book_IDs = []

        for tracker,cur_title in enumerate(distilled_titles):
            if tracker % 100 == 0:
                print('we are {0} / {1} through our titles'.format(tracker, len(distilled_titles)))
            repeated_books = TITLE_dict[cur_title]

            master_book, master_indx = identify_master_book(repeated_books)
            master_consolidated_book_list.append(master_book)
            master_consolidated_book_IDs.append(master_indx)

            for jj, cur_node in enumerate(repeated_books):
                ## Apparently we need this check...
                if cur_node == master_book:
                    continue

                ## Apparently, doing a + operation creates an N^2 runtime which matters here...
                ## Iterate through length of raters and append items individually (do in the loop below):
                # master_book.raters = master_book.raters + cur_node.raters
                # master_book.raters_ID = master_book.raters_ID + cur_node.raters_ID

                ## Now for each rater that we switch over to the master, we need to update the pointer to the book
                ## After that is done, delete the current book object
                for indx,tuple_user in enumerate(cur_node.raters):
                    cur_user = tuple_user[0]

                    ## do the master_book appending here to avoid N^2 runtime above
                    ## First, check that the user is not already in the master book raters
                    if tuple_user in master_book.raters:
                        continue
                    master_book.raters.append(tuple_user)
                    master_book.raters_ID.append(cur_node.raters_ID[indx])

                    user_books_list = cur_user.books
                    user_IDs_list = cur_user.books_ID

                    for iiii in range(len(user_books_list)):
                        if user_books_list[iiii][0] == cur_node: # we are looking for the exact same object
                            temp_tuple = user_books_list[iiii]
                            temp_list = list(temp_tuple)
                            temp_list[0] = master_book
                            user_books_list[iiii] = tuple(temp_list)
                            user_IDs_list[iiii] = master_book.ID
                            break

                del cur_node


        print('About to enter this sum territory')

        None_sum = 0
        for cur_bk in master_consolidated_book_list:
            for indxx, jj in enumerate(cur_bk.raters):
                if jj[1] is None:
                    tmp_jj = list(jj)
                    tmp_jj[1] = 2.5
                    jj = tuple(tmp_jj)
                    cur_bk.raters[indxx] = jj
                    None_sum += 1
        print(None_sum)

        print('Done with distilling trackers!')

        # sys.setrecursionlimit(1000000)
        # with open('master_checkpoints/masterLists_golden.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump([master_consolidated_book_list, master_user_list], f)

        print('finished loading data')
        print('Loading time is {0} minute'.format((time.time() - startTime) / 60))

        # sys.setrecursionlimit(1000000)
        # with open('master_checkpoints/masterLists_golden.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        #     master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs = pickle.load(f)


    else:
        pass
        # sys.setrecursionlimit(100000)
        # with open('master_checkpoints/masterLists_prototype.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        #     master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs = pickle.load(f)



    print('next')









                                    ####################
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## MongoDB Time!! ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                    ####################

    dbName = "bookhound_proto_2"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbName]
    print("Got it")

    bookCol = mydb["books"]
    userCol = mydb["users"]

    ## Create database

    build_database = input('Do you want to build up the database? (1 for yes)')
    if build_database == str(1):
        DB_type = input('What type of database? 1 for normal Mongo DB')

        if DB_type == str(1):

            count_tracker = 0
            global_book_errors = 0
            global_linker_errors = 0
            global_numberOfEdges = 0
            global_blinker_tracker = []
            for this_book in master_consolidated_book_list:
                # if count_tracker == 1000:
                #     ## Stop the databse prematurely
                #     break
                if count_tracker % 100 == 0:
                    print('On book {0} / {1}'.format(count_tracker, len(master_consolidated_book_list)))
                    print('     -->we have encountered {0} linker errors so far'.format(global_linker_errors))
                    print('     -->have seen {0} edges so far'.format(global_numberOfEdges))
                count_tracker += 1

                Mongo_add_book_node(this_book)

                raters_for_book = [i[0] for i in this_book.raters]
                # user_2_book_rating = [i[1] for i in this_book.raters]

                ## We have a list of raters for the book and a list for their corresponding ratings to this book
                ## Call a function to add each of these nodes
                ## Then create a new linker table for this book
                Mongo_add_user_node_list(raters_for_book)

            print("Done adding to prototype database!")

            print('We encountered {0} book node errors'.format(global_book_errors))
            print('We encountered {0} linker duplicate errors! See the list of IDs printed below:'.format(
                global_linker_errors))
            print(global_blinker_tracker)

    else:

        ## Here if we don't want to rebuild the table
        ## First count up total number of books and users
        DB_books = [*bookCol.find()]
        DB_users = [*userCol.find()]

        print('We have {0} books and {1} users in the database'.format(len(DB_books), len(DB_users)))
        x = Mongo_first_order_search(3)
        print("Closest book to HP is {0}".format(x['title']))

        ## Now let's calculate the average number of books each user has
        users_avgBookNum = [len(i['booksID']) for i in DB_users]
        avgBookNum = sum(users_avgBookNum) / len(users_avgBookNum)
        print("Users have on average {0} books linked!".format(avgBookNum))
        print("Worst case user has {0} books linked".format(max(users_avgBookNum)))

        ## Let's also calculate the average number of users each book has (should be around 100 originally)
        books_avgUserNum = [len(i['ratersID']) for i in DB_books]
        avgUserNum = sum(books_avgUserNum) / len(books_avgUserNum)
        print("Books have on average {0} users linked!".format(avgUserNum))
        print("Worst case book has {0} users linked".format(max(books_avgUserNum)))


        x = Mongo_first_order_search(1846017)
        print("Closest book to City of Saints and Madmen is {0}".format(x['title']))

        x = Mongo_first_order_search(1)
        print("Closest book to HP half blood prince is {0}".format(x['title']))

        x = Mongo_first_order_search(49529403)
        print("Closest book to PAris Adrift is {0}".format(x['title']))

        x = Mongo_first_order_search(186074)
        print("Closest book to The name of the wind is {0}".format(x['title']))



                                    ####################
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## MongoDB Time!! ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                    ####################





    ## TESTING THE GENERATED DB!
    ## some Book IDs to play with:
    ## 1846017 -- City Of Saints And Madmen
    ## 1 -- HP and half blood prince
    ## 3 -- HP and sorcerors stone
    ## 49529403 -- Paris Adrift
    ## 67700 -- The Persian Boy (Alexander the Great, #2)
