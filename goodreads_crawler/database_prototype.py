## Using SQLite to prototype the intended table structure in the final AWS RDS DB

#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import sys
import sqlite3
import pickle
from collections import Counter


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

        sys.setrecursionlimit(100000)
        with open('master_checkpoints/masterLists_prototype.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs], f)


    else:
        sys.setrecursionlimit(100000)
        with open('master_checkpoints/masterLists_prototype.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            master_consolidated_book_list, master_user_list, master_consolidated_book_IDs, master_user_IDs = pickle.load(f)


    print('finished loading data')



    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE employees (
                    first text,
                    last text,
                    pay integer)""")
    except:
        pass

    c.execute("INSERT INTO employees VALUES ('Michael', 'Ershov', 6969696)")
    c.execute("SELECT * FROM employees WHERE  last = 'Ershov'")

    var = c.fetchall()
    print(var)

    aa = 'deez'
    bb = 'nuts'
    cc = 420
    c.execute("INSERT INTO employees VALUES (?, ?, ?)", (aa,bb,cc))

    c.execute("SELECT * FROM employees WHERE  pay = 420")

    aa = 'john'
    bb = 'wick'
    cc = 1000000000
    c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': aa, 'last': bb, 'pay': cc})

    c.execute("SELECT * FROM employees WHERE  first = 'john'")

    var = c.fetchall()
    print(var)



    conn.commit()

    conn.close()
