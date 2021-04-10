## Using SQLite to prototype the intended table structure in the final AWS RDS DB

#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import sys
import sqlite3
import pickle
from collections import Counter
import time
import traceback

#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
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







###### SQL Related Functions below #########

def print_error(er):
    print('SQLite error: %s' % (' '.join(er.args)))
    print("Exception class is: ", er.__class__)
    print('SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))


def create_base_tables():
    ## Create Users table
    try:
        c.execute("""CREATE TABLE Users (
                    ID int,
                    name varchar,
                    link varchar,
                    ratings_link varchar,
                    
                    fk_books varchar,
                    
                    PRIMARY KEY (ID)
                    )""")
        print('Users Success')
    except sqlite3.Error as er:
        print('error occured on Users table!')
        print_error(er)

    ## Create Books table
    try:
        c.execute("""CREATE TABLE Books (
                    ID int,
                    title varchar,
                    href varchar,
                    author varchar,
                    meta varchar,
                    details varchar,
                    series varchar,
                    summary varchar,
                    image_source varchar,
                    image_binary varbinary,
                    full_params bool,
                    
                    fk_users varchar,
                    fk_genres int,
                    
                    PRIMARY KEY (ID)
                    )""")
        print('Books Success')
    except sqlite3.Error as er:
        print('error occured on Books table!')
        print_error(er)


    ## Now add indexes to the 2 base tables above!
    ## Create Users table
    try:
        c.execute("""CREATE UNIQUE INDEX idx_users_ID ON Users (ID)""")
        print('Created User Index')
    except sqlite3.Error as er:
        print('error occured on User Index Creation!')
        print_error(er)

    ## Create BOOKS table
    try:
        c.execute("""CREATE UNIQUE INDEX idx_BOOKS_ID ON BOOKS (ID)""")
        print('Created BOOKS Index')
    except sqlite3.Error as er:
        print('error occured on BOOKS Index Creation!')
        print_error(er)



def create_alt_base_tables():
    ## Create Users table
    try:
        c.execute("""CREATE TABLE Users (
                        ID int,
                        name varchar,
                        link varchar,
                        ratings_link varchar,

                        PRIMARY KEY (ID)
                        )""")
        print('Users Success')
    except sqlite3.Error as er:
        print('error occured on Users table!')
        print_error(er)

    ## Create Books table
    try:
        c.execute("""CREATE TABLE Books (
                        ID int,
                        title varchar,
                        href varchar,
                        author varchar,
                        meta varchar,
                        details varchar,
                        series varchar,
                        summary varchar,
                        image_source varchar,
                        image_binary varbinary,
                        full_params bool,

                        fk_genres int,

                        PRIMARY KEY (ID)
                        )""")
        print('Books Success')
    except sqlite3.Error as er:
        print('error occured on Books table!')
        print_error(er)

    ## Create Edge Table
    try:
        c.execute("""CREATE TABLE Edges (
                        ID int,
                        book_ID int,
                        user_ID int,
                        rating float,

                        PRIMARY KEY (ID)
                        )""")
        print('Books Success')
    except sqlite3.Error as er:
        print('error occured on Edges table!')
        print_error(er)

    ## Now add indexes to the 3 base tables above!
    ## Create Users table
    try:
        c.execute("""CREATE UNIQUE INDEX idx_users_ID ON Users (ID)""")
        print('Created User Index')
    except sqlite3.Error as er:
        print('error occured on User Index Creation!')
        print_error(er)

    ## Create BOOKS table
    try:
        c.execute("""CREATE UNIQUE INDEX idx_BOOKS_ID ON Books (ID)""")
        print('Created BOOKS Index')
    except sqlite3.Error as er:
        print('error occured on BOOKS Index Creation!')
        print_error(er)

    ## Create Edges table
    try:
        c.execute("""CREATE INDEX idx_Edges ON Edges (book_ID, user_ID)""")
        print('Created Edges Index')
    except sqlite3.Error as er:
        print('error occured on Edges Index Creation!')
        print_error(er)



## Helper function to add a single node to the books table
def SQL_add_book_node(book_node):
    ## Have the following structure:
    ## 1) ID 2) title 3) href 4) author 5) meta
    ## 6) details 7) series 8) summary 9) image_source
    ## 10) image_binary 11) full_params bool 12) fk_users 13) fk_genres
    global global_book_errors
    ID          = book_node.ID
    title       = book_node.title
    href        = book_node.href
    author      = book_node.author
    meta        = book_node.meta
    details     = book_node.details
    series      = book_node.series
    summary     = book_node.summary
    im_src      = book_node.imageSource
    im_bin      = book_node.imageBinary
    full_param  = book_node.has_full_params
    fk_linker    = 'b_linker_' + str(ID)
    fk_genres   = ID ## Should this be something else??

    try:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (ID, title, href, author, meta, details, series, summary, im_src, im_bin, full_param, fk_linker, fk_genres ))
        # print("Success adding: {0}".format(title))
    except sqlite3.Error as er:
        print('error occured on adding {0}!'.format(title))
        print_error(er)
        global_book_errors += 1


## Helper function to add a single node to the books table
def SQL_add_alt_book_node(book_node):
    ## Have the following structure:
    ## 1) ID 2) title 3) href 4) author 5) meta
    ## 6) details 7) series 8) summary 9) image_source
    ## 10) image_binary 11) full_params bool 12) fk_users 13) fk_genres
    global global_book_errors
    ID          = book_node.ID
    title       = book_node.title
    href        = book_node.href
    author      = book_node.author
    meta        = book_node.meta
    details     = book_node.details
    series      = book_node.series
    summary     = book_node.summary
    im_src      = book_node.imageSource
    im_bin      = book_node.imageBinary
    full_param  = book_node.has_full_params
    fk_genres   = ID ## Should this be something else??

    try:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (ID, title, href, author, meta, details, series, summary, im_src, im_bin, full_param, fk_genres ))
        # print("Success adding: {0}".format(title))
    except sqlite3.Error as er:
        print('error occured on adding {0}!'.format(title))
        print_error(er)
        global_book_errors += 1




## Helper function to add a single node to the users table
def SQL_add_user_node(user_node):
    ## Have the following structure:
    ## 1) ID 2) name 3) link 4) rlink 5) fk_books
    ID          = user_node.ID
    name        = user_node.name
    link        = user_node.link
    rlink       = user_node.ratingsLink
    fk_linker    = 'u_linker_' + str(ID)

    try:
        c.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?)",
              (ID, name, link, rlink, fk_linker))
        # print("     -Success adding: {0}".format(name))
    except sqlite3.Error as er:
        print('     -error occured on adding {0}!'.format(name))
        print_error(er)


## Helper function to add a single node to the users table
def SQL_add_alt_user_node(user_node):
    ## Have the following structure:
    ## 1) ID 2) name 3) link 4) rlink 5) fk_books
    ID          = user_node.ID
    name        = user_node.name
    link        = user_node.link
    rlink       = user_node.ratingsLink

    try:
        c.execute("INSERT INTO Users VALUES (?, ?, ?, ?)",
              (ID, name, link, rlink))
        # print("     -Success adding: {0}".format(name))
    except sqlite3.Error as er:
        print('     -error occured on adding {0}!'.format(name))
        print_error(er)



## Helper function that adds a list of users
def SQL_add_user_node_list(user_list):
    for cur_user in user_list:
        ## First check if the user is already in DB
        ## IF not, then add it
        if is_ID_in_table('Users', cur_user.ID):
            continue
        else:
            SQL_add_user_node(cur_user)

            ## Also need to add user linker table here as well...
            ## Weird that we have the linker table addition at different places in the code but whatevez
            linker_str = 'u_linker_{0}'.format(cur_user.ID)
            linker_elements = cur_user.books
            # for ttuple in cur_user.books:
            #     bookNode = ttuple[0]
            #     rating_2_book = ttuple[1]
            #     linker_elements.append((bookNode, rating_2_book))

            SQL_add_linker_table(linker_str, linker_elements)

## Helper function that adds a list of users
def SQL_add_alt_user_node_list(user_list):
    for cur_user in user_list:
        ## First check if the user is already in DB
        ## IF not, then add it
        if is_ID_in_table('Users', cur_user.ID):
            continue
        else:
            SQL_add_alt_user_node(cur_user)


## Helper function to add linker table for either a book (with table of users) or a user (with table of books)
def SQL_add_linker_table(linker_str, linker_elements):
    global global_linker_errors
    global global_blinker_tracker

    ## First create our linker table
    exec_str = 'CREATE TABLE {0} (ID int, rating float)'.format(linker_str)
    try:
        c.execute(exec_str)
        # print('linker table {0} Success'.format(linker_str))
    except sqlite3.Error as er:
        print('error occured on creating linker table {0}!'.format(linker_str))
        print_error(er)
        global_linker_errors += 1
        global_blinker_tracker.append( linker_str.split('_')[-1] )
        return ## Dont want to insert values into some rando table

    ## Next, append all of the elements as parts of this table
    ## Rows should be book or user node ID + user_2_book rating


    for cur_tuple in linker_elements:
        node_ID = cur_tuple[0].ID
        rating = cur_tuple[1]

        try:
            c.execute("INSERT INTO {0} VALUES (?,?)".format(linker_str),
                      (node_ID, rating))
            # print("     -Success adding: {0} to linker table {1}".format(node_ID, linker_str))
        except sqlite3.Error as er:
            print('     -error occured on adding {0} to linker table {1}!'.format(node_ID, linker_str))
            print_error(er)


## Helper function to add all the edges of raters that rated a given book
## For N raters, add N rows, where row will be book_ID -- user_x, for x in range(N)
def SQL_add_graphEdge_rows(book_ID, book_raters_list):
    global global_linker_errors
    global global_numberOfEdges

    ## Next, append all of the elements as parts of this table
    ## Rows should be book or user node ID + user_2_book rating

    for cur_tuple in book_raters_list:
        user_ID = cur_tuple[0].ID
        rating = cur_tuple[1]
        if not rating:
            print('adding none rater')
            rating = 2.5

        try:
            c.execute("INSERT INTO Edges VALUES (?,?,?,?)", (global_numberOfEdges, book_ID, user_ID, rating))
            global_numberOfEdges += 1
        except sqlite3.Error as er:
            print('     -error occured on adding {0} and {1} to Edges Table!'.format(book_ID, user_ID))
            global_linker_errors += 1
            print_error(er)


## Helper function to return boolean of whether the input ID is in the given table
def is_ID_in_table(table_name, input_ID):
    # exec_str = "SELECT CASE WHEN EXISTS (SELECT TOP 1 *\
    #                      FROM {0} \
    #                      WHERE ID = {1}) \
    #         THEN CAST (1 AS BIT) \
    #         ELSE CAST (0 AS BIT) END ".format(table_name, input_ID)

    exec_str = "SELECT * FROM {0} WHERE  ID = {1}".format(table_name, input_ID)


    try:
        c.execute(exec_str)
        found_element = c.fetchall()
        if not found_element:
            return False
            # print("Search completed, ID {0} not found in {1}".format(input_ID, table_name))
        else:
            return True
            # return found_element
    except sqlite3.Error as er:
        print('error occured on finding {0} in {1}!'.format(input_ID, table_name))
        print_error(er)
        return False


####### API LEVEL INTERFACE FUNCTIONS #######

## Functin to return a list of book IDs based on input book ID
## For the input book ID, get the b_linker table from SQL
## Iterate through b_linker table to get all the user nodes that rated the input book
## Iterate through each of the u_linker tables
## Return a dictionary, where the keys are the first order related books, and the values are their occurance
def first_order_books(test_ID):
    book_dict       = {} ## Store first-order relationed book ID occurances
    og_rating_dict  = {} ## Store average rating for user_2_original book
    new_rating_dict = {}  ## Store average rating for user_2_new book


    linker_str = 'b_linker_{0}'.format(test_ID)
    try:
        linked_users_list = c.execute('SELECT * FROM {0}'.format(linker_str)).fetchall()
    except sqlite3.Error as er:
        print('Error accessing {0} table'.format(linker_str))
        print_error(er)
        return


    for cur_user_tuple in linked_users_list:
        cur_user_ID = cur_user_tuple[0]
        rating_user_2_og = cur_user_tuple[1]
        if not rating_user_2_og:
            print('{0} has a none review for book {1}'.format(cur_user_ID, test_ID))
            rating_user_2_og = 2.5

        linker_str = 'u_linker_{0}'.format(cur_user_ID)
        try:
            linked_books_list = c.execute('SELECT * FROM {0}'.format(linker_str)).fetchall()
        except sqlite3.Error as er:
            print('Error accessing {0} table'.format(linker_str))
            print_error(er)
            return
        if cur_user_ID == 51213745:
            print(linked_books_list)

        for cur_book_tuple in linked_books_list:
            cur_book_ID = cur_book_tuple[0]
            rating_user_2_new = cur_book_tuple[1]
            if not rating_user_2_new:
                print('{0} has a none review for book {1}'.format(cur_user_ID, cur_book_ID))
                rating_user_2_new = 2.5

            ## finally, add to the dictionaries here:
            if cur_book_ID in book_dict.keys():
                og_rt = book_dict[cur_book_ID]
                book_dict[cur_book_ID] += 1

                new_rating_dict[cur_book_ID] = (og_rt*new_rating_dict[cur_book_ID] + rating_user_2_new) / (og_rt + 1)
            else:
                book_dict[cur_book_ID]          = 1
                og_rating_dict[cur_book_ID]     = rating_user_2_og
                new_rating_dict[cur_book_ID]    = rating_user_2_new

    ## Before we return, we want to remove the original book from these dict... duh
    del book_dict[test_ID]
    del og_rating_dict[test_ID]
    del new_rating_dict[test_ID]

    return book_dict, og_rating_dict, new_rating_dict






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





    ##############
    ## SQL Time ##
    ##############

    conn = sqlite3.connect('bookhound_graphtest_2.db')
    c = conn.cursor()

    build_database = input('Do you want to build up the database? (1 for yes)')
    if build_database == str(1):
        DB_type = input('What type of database? 1 for multi-table, 2 for edge-table graph approach')

        if DB_type == str(1):

            ## Test creating the book and user table

            ## Create the basic tables
            ## This is Books, Users, RatUSR_users, RatBOOK_users
            create_base_tables()


            # ## Now update tables with foreign keys to each other
            # ## Books should have fk_raters, Users fk_books, RatUSR_users fk_user_x, and RatBOOK_books fk_book_x
            # #addColumn = "ALTER TABLE student ADD COLUMN Address varchar(32)"
            # add_fk_columns() # Then add the FOREIGN KEY stuff

            ## Let's start iterating through our master_consolidated_book_list
            ## Add book to a book node, add it's users tp a user node, and create a table linking the book with the users
            count_tracker = 0
            global_book_errors = 0
            global_linker_errors = 0

            global_blinker_tracker = []
            for this_book in master_consolidated_book_list:
                if count_tracker == 1000:
                    ## Stop the databse prematurely
                    break
                if count_tracker % 100 == 0:
                    print('On book {0} / {1}'.format(count_tracker, len(master_consolidated_book_list)))
                    print('     -->we have encountered {0} linker errors so far'.format(global_linker_errors))
                count_tracker += 1

                # print("Book title: {0}".format(this_book.title))

                SQL_add_book_node(this_book)

                raters_for_book = [i[0] for i in this_book.raters]
                # user_2_book_rating = [i[1] for i in this_book.raters]

                ## We have a list of raters for the book and a list for their corresponding ratings to this book
                ## Call a function to add each of these nodes
                ## Then create a new linker table for this book
                SQL_add_user_node_list(raters_for_book)

                linker_str = 'b_linker_{0}'.format(this_book.ID)
                linker_elements = this_book.raters
                # for i in range(this_book.raters):
                #     linker_elements.append( (raters_for_book[i], user_2_book_rating[i]))

                SQL_add_linker_table(linker_str, linker_elements)


            print("Done adding to prototype database!")

            print('We encountered {0} book node errors'.format(global_book_errors))
            print('We encountered {0} linker duplicate errors! See the list of IDs printed below:'.format(
                global_linker_errors))
            print(global_blinker_tracker)



        elif DB_type == str(2):
            create_alt_base_tables()

            count_tracker = 0
            global_book_errors = 0
            global_linker_errors = 0
            global_numberOfEdges = 0
            global_blinker_tracker = []
            for this_book in master_consolidated_book_list:
                if count_tracker == 1000:
                    ## Stop the databse prematurely
                    break
                if count_tracker % 100 == 0:
                    print('On book {0} / {1}'.format(count_tracker, len(master_consolidated_book_list)))
                    print('     -->we have encountered {0} linker errors so far'.format(global_linker_errors))
                count_tracker += 1

                SQL_add_alt_book_node(this_book)

                raters_for_book = [i[0] for i in this_book.raters]
                # user_2_book_rating = [i[1] for i in this_book.raters]

                ## We have a list of raters for the book and a list for their corresponding ratings to this book
                ## Call a function to add each of these nodes
                ## Then create a new linker table for this book
                SQL_add_alt_user_node_list(raters_for_book)

                SQL_add_graphEdge_rows(this_book.ID, this_book.raters)


            print("Done adding to prototype database!")

            print('We encountered {0} book node errors'.format(global_book_errors))
            print('We encountered {0} linker duplicate errors! See the list of IDs printed below:'.format(
                global_linker_errors))
            print(global_blinker_tracker)




    ## TESTING THE GENERATED DB!
    ## some Book IDs to play with:
    ## 1846017 -- City Of Saints And Madmen
    ## 1 -- HP and half blood prince
    ## 3 -- HP and sorcerors stone
    ## 49529403 -- Paris Adrift
    ## 67700 -- The Persian Boy (Alexander the Great, #2)

    print("Testing book linkage for: Persian Boy")
    test_ID = 67700
    linked_books, og_ratings, new_ratings = first_order_books(test_ID)
    ## Now let's get the books with the most amount of users agreeing/pointing to it:
    closest_book_ID = max(linked_books, key=lambda x: linked_books[x])
    closest_title = c.execute('SELECT title FROM Books WHERE ID = {0}'.format(closest_book_ID)).fetchall()

    print("Testing book linkage for: HP sorcerors stone")
    test_ID = 3
    linked_books, og_ratings, new_ratings = first_order_books(test_ID)
    ## Now let's get the books with the most amount of users agreeing/pointing to it:
    closest_book_ID = max(linked_books, key=lambda x: linked_books[x])
    closest_title = c.execute('SELECT title FROM Books WHERE ID = {0}'.format(closest_book_ID)).fetchall()

    print("Testing book linkage for: Paris Adrift")
    test_ID = 49529403
    linked_books, og_ratings, new_ratings = first_order_books(test_ID)
    ## Now let's get the books with the most amount of users agreeing/pointing to it:
    closest_book_ID = max(linked_books, key=lambda x: linked_books[x])
    closest_title = c.execute('SELECT title FROM Books WHERE ID = {0}'.format(closest_book_ID)).fetchall()

    print("Testing book linkage for: The Space Between Worlds")
    test_ID = 48848254
    linked_books, og_ratings, new_ratings = first_order_books(test_ID)
    ## Now let's get the books with the most amount of users agreeing/pointing to it:
    closest_book_ID = max(linked_books, key=lambda x: linked_books[x])
    closest_title = c.execute('SELECT title FROM Books WHERE ID = {0}'.format(closest_book_ID)).fetchall()





    print('start 1')
    exec_str = 'SELECT ID FROM Books WHERE ID = {0}'.format(9732202)
    c.execute(exec_str)
    print(c.fetchall())
    print('end 1')


    print('start 2')
    c.quert(exec_str)
    r = c.use_result()
    print(r.fetch_row())
    print('end 2')


    conn.commit()
    conn.close()








    ## Some notable errors:
    ## Revival, Vol. 8: Stay Just A Little Bit Longer (Revival, #8) ----- 33632812



    # ## Double check some stuff...
    # print( is_ID_in_table('Books', 9732202) ) ## Should output the affirmation
    #
    # c.execute("SELECT * FROM books")
    # print(c.fetchall()) ## Prints the execution statement above








    #################################
    #### BELOW IS DEAD ZONE!!!! #####
    #################################

    #
    # # Let's insert 2 books and 2 users
    # # Have 1 user point to only 1 book, while secnd user points to both
    # ID = 1
    # name = 'johny ive'
    # link = 'whatsgood.com'
    # ratings_link = 'myratings.com'
    #
    # c.execute("INSERT INTO users VALUES (?, ?, ?)", (0, bb, cc))
    #
    #
    #
    #
    # c.execute("SELECT * FROM employees WHERE  first = 'john'")
    #
    # var = c.fetchall()
    # print(var)
    #
    #
    # ## Reference code below!
    # ## COMMENT OUT LATER!!
    # # User table
    # # ss = 'CREATE TABLE newtable (' + 'first text,' + 'last text,' + 'pay integer)'
    # try:
    #     c.execute("""CREATE TABLE newtable_4 (
    #                 first text,
    #                 last text,
    #                 pay integer,
    #                 PersonID int,
    #                 FOREIGN KEY (PersonID) REFERENCES newtable_10(PersonID))""")
    # except:
    #     print('ERROR!')
    #
    #
    # c.execute("INSERT INTO employees VALUES ('Michael', 'Ershov', 6969696)")
    # c.execute("SELECT * FROM employees WHERE  last = 'Ershov'")
    #
    # var = c.fetchall()
    # print(var)
    #
    # aa = 'deez'
    # bb = 'nuts'
    # cc = 420
    # c.execute("INSERT INTO employees VALUES (?, ?, ?)", (aa,bb,cc))
    #
    # c.execute("SELECT * FROM employees WHERE  pay = 420")
    #
    # aa = 'john'
    # bb = 'wick'
    # cc = 1000000000
    # c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': aa, 'last': bb, 'pay': cc})
    #
    # c.execute("SELECT * FROM employees WHERE  first = 'john'")
    #
    # var = c.fetchall()
    # print(var)
    #
    #
    #
    # conn.commit()
    #
    # conn.close()
