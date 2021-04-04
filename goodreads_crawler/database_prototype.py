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
                    
                    fk_books int
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
                    fk_genres int
                    )""")
        print('Books Success')
    except sqlite3.Error as er:
        print('error occured on Books table!')
        print_error(er)



    ## Create RatUSR_users table
    ## Apparently, limit to number of columns per table is 1-2k...Instead, let's make a table per book
    ## Table will have rows of users that rated a book, columns will be fk to user, user ID, rating, etc
    # rattable_fk_num = 9000
    # ratusr_users_string = 'CREATE TABLE RatUSR_users (ID int, '
    # for i in range(rattable_fk_num):
    #     temp_str = 'fk_user_{0} int,'.format(i)
    #     ratusr_users_string += temp_str
    # ratusr_users_string = ratusr_users_string[0:-1] + ')'
    #
    # try:
    #     c.execute(ratusr_users_string)
    #     print('RatUSR_users Success')
    # except sqlite3.Error as er:
    #     print('error occured on RatUSR_users table!')
    #     print_error(er)


    ## Create RatBOOK_books table
    rattable_fk_num = 200
    ratusr_books_string = 'CREATE TABLE RatBOOK_books (ID int, '
    for i in range(rattable_fk_num):
        temp_str = 'fk_book_{0} int,'.format(i)
        ratusr_books_string += temp_str
    ratusr_books_string = ratusr_books_string[0:-1] + ')'

    try:
        c.execute(ratusr_books_string)
        print('RatBOOK_books Success')
    except sqlite3.Error as er:
        print('error occured on RatBOOK_books table!')
        print_error(er)

# def add_fk_columns():
#     addColumn = 'ALTER TABLE Users ADD COLUMN fk_books int;'
#     # addFK = 'ALTER TABLE Users ADD FOREIGN KEY (fk_books) REFERENCES RatBOOK_books(fk_books);'
#     try:
#         c.execute(addColumn)
#         print('Users add column Success')
#     except:
#         print('error occured on altering users for add column!')
#     # try:
#     #     c.execute(addFK)
#     #     print('Users add FK Success')
#     # except:
#     #     print('error occured on altering users for add FK!')




####### SQL HELPER FUNCTIONS!!!!#######


## Helper function to add a single node to the books table
def SQL_add_book_node(book_node):
    ## Have the following structure:
    ## 1) ID 2) title 3) href 4) author 5) meta
    ## 6) details 7) series 8) summary 9) image_source
    ## 10) image_binary 11) full_params bool 12) fk_users 13) fk_genres
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
    fk_users    = 'book_link_' + str(ID)
    fk_genres   = ID ## Should this be something else??

    try:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (ID, title, href, author, meta, details, series, summary, im_src, im_bin, full_param, fk_users, fk_genres ))
        print("Success adding: {0}".format(title))
    except sqlite3.Error as er:
        print('error occured on adding {0}!'.format(title))
        print_error(er)


## Helper function to add a single node to the users table
def SQL_add_user_node(user_node):
    ## Have the following structure:
    ## 1) ID 2) name 3) link 4) rlink 5) fk_books
    ID          = user_node.ID
    name        = user_node.name
    link        = user_node.link
    rlink       = user_node.ratingslink
    fk_books    = ID

    try:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)",
              (ID, name, link, rlink, fk_books))
        print("     -Success adding: {0}".format(name))
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


## Helper function to add linker table for either a book (with table of users) or a user (with table of books)
def SQL_add_linker_table(linker_str, linker_elements):
    
    pass



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

        print('Done with distilling trackers!')

        # sys.setrecursionlimit(100000)
        # with open('master_checkpoints/masterLists_prototype.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump([master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs], f)


    else:
        pass
        # sys.setrecursionlimit(100000)
        # with open('master_checkpoints/masterLists_prototype.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        #     master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs = pickle.load(f)





    print('finished loading data')
    print('Loading time is {0} minute'.format((time.time()-startTime)/60))
    print('next')





    ##############
    ## SQL Time ##
    ##############

    conn = sqlite3.connect('bookhound_test_25.db')
    c = conn.cursor()

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
    for this_book in master_consolidated_book_list:
        print("Book title: {0}".format(this_book.title))

        SQL_add_book_node(this_book)

        raters_for_book = [i[0] for i in this_book.raters]
        user_2_book_rating = [i[1] for i in this_book.raters]

        ## We have a list of raters for the book and a list for their corresponding ratings to this book
        ## Call a function to add each of these nodes
        ## Then create a new linker table for this book
        SQL_add_user_node_list(raters_for_book)

        linker_str = 'b_linker_{0}'.format(this_book.ID)
        linker_elements = []
        for i in range(this_book.raters):
            linker_elements.append( (raters_for_book[i], user_2_book_rating[i]))

        SQL_add_linker_table(linker_str, linker_elements)



    ## Double check some stuff...
    print( is_ID_in_table('Books', 9732202) ) ## Should output the affirmation

    c.execute("SELECT * FROM books")
    print(c.fetchall()) ## Prints the execution statement above










    conn.commit()

    conn.close()




    #################################
    #### BELOW IS DEAD ZONE!!!! #####
    #################################

    #
    # # Create RatUser tables
    # rattable_fk_num = 9000
    # ratusr_users_string = 'CREATE TABLE ratusr_users (ID int, '
    # for i in range(rattable_fk_num):
    #     temp_str = 'fk_user_{0} int,'.format(i)
    #     ratusr_users_string += temp_str
    #
    # # temp_str = 'PRIMARY KEY (ID),'
    # # ratusr_users_string += temp_str
    #
    # #FOREIGN KEY (PersonID) REFERENCES newtable_10(PersonID))
    # for i in range(rattable_fk_num):
    #     temp_str = 'FOREIGN KEY (fk_user_{0}) REFERENCES Users(fk_user_{0}),'.format(i)
    #     ratusr_users_string += temp_str
    #
    # ratusr_users_string = ratusr_users_string[0:-1] + ')'
    #
    # try:
    #     c.execute("""CREATE TABLE Users (
    #                 ID int,
    #                 name varchar,
    #                 link varchar,
    #                 ratings_link varchar,
    #                 books enum,
    #                 books_rating enum,
    #                 books_id
    #                 )""")
    # except:
    #     print('error occured!')
    #
    # try:
    #     c.execute(ratusr_users_string)
    # except:
    #     print("error occured!")
    #
    # try:
    #     c.execute("""CREATE TABLE books (
    #                 ID int,
    #                 title varchar,
    #                 href varchar,
    #                 PersonID int FOREIGN KEY REFERENCES Persons(PersonID)
    #                 fk_raters int FOREIGN KEY REFERENCES
    #                 raters enum,
    #                 raters_rating enum,
    #                 raters_id enum
    #                 )""")
    # except:
    #     print('error occured!')
    #
    #
    # # Book table
    # try:
    #     c.execute("""CREATE TABLE books (
    #                 ID int,
    #                 title varchar,
    #                 href varchar,
    #                 PersonID int FOREIGN KEY REFERENCES Persons(PersonID)
    #                 fk_raters int FOREIGN KEY REFERENCES
    #                 raters enum,
    #                 raters_rating enum,
    #                 raters_id enum
    #                 )""")
    # except:
    #     print('error occured!')
    #
    # # User table
    # try:
    #     c.execute("""CREATE TABLE users (
    #                 ID int,
    #                 name varchar,
    #                 link varchar,
    #                 ratings_link varchar,
    #                 books enum,
    #                 books_rating enum,
    #                 books_id
    #                 )""")
    # except:
    #     print('error occured!')
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
