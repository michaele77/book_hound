## This file collects all of the data in scraped_data and combines objects
## Each pickle file contains its own covered_books and covered_users lists
## We want to combine these lists through the following SOP:
##      --> Unpack all of the data in seperate lists
##      --> Go through the covered_users lists and conditionally append them.
##          --> If a user has been covered already in a seperate pickle, the only difference should be the book they
##              reviewed, which would be listed as a '4.5' rating on their book list
##      --> Go through the covered_books list and conditionally append them.
##          --> Make sure if we have already covered a book that has full parameters, keep that one
##          --> Otherwise, merge the raters lists (the reviewers lists would stay the same)
##              --> Double check you dont double-count users (2 of the same user being counted as 2 seperate raters)




#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import os
import pickle
from collections import Counter



#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#

directory_list = os.listdir('scraped_data/')
try:
    directory_list.pop('.DS_Store')
except:
    print('No DS_store to pop (thankfully)')


#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#


def get_repeated_instances(instance_arr, id_list_toCheck, ID_toCheck):
    repeated_indx = [i for i, x in enumerate(id_list_toCheck) if x == ID_toCheck]
    instance_list = [instance_arr[i] for i in repeated_indx]
    return instance_list, repeated_indx


def consolidate_user_list(fnc_master_list, fnc_id_list, fnc_user_inst, fnc_user_idx):

    indx_to_pop = []
    # For each repeated user, update one master node, and pop the rest from the master list
    for i in range(len(fnc_user_inst)):
        curr_user_list = fnc_user_inst[i]
        curr_indx_list = fnc_user_idx[i]

        # For users, the only difference is the last entree in the book list. doesnt matter which node is the master
        # Choose first index as the master node arbitrarily
        master_node = curr_user_list[0]

        for vv, other_node in enumerate(curr_user_list):
            if vv == 0:
                # Already set master node
                continue
            else:
                # New book will always exist at the last spot
                new_book = other_node.books[-1]
                new_ID = other_node.books_ID[-1]

                # Add it to the master node
                master_node.books.append( new_book )
                master_node.books_ID.append( new_ID )

                # Add it to the pop list
                indx_to_pop.append(curr_indx_list[vv])

    # Now go through the pop list backwards and pop em all off!
    indx_to_pop.sort() #sort it first inplace
    for i in reversed(indx_to_pop):
        fnc_master_list.pop(i)
        fnc_id_list.pop(i)




def consolidate_user_list(fnc_master_list, fnc_id_list, fnc_book_inst, fnc_book_idx):







# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#


# Create proper main structure
if __name__ == "__main__":
    master_user_list = []
    master_book_list = []

    for curr_pickle in directory_list:
        with open('scraped_data/' + curr_pickle, 'rb') as f:  # Python 3: open(..., 'rb')
            unpacked_user, unpacked_book = pickle.load(f)

            master_user_list = master_user_list + unpacked_user
            master_book_list = master_book_list + unpacked_book


    # Now that we have everything appended, let's see how many repeats we have
    master_user_IDs = [i.ID for i in master_user_list]
    master_book_IDs = [i.ID for i in master_book_list]

    c_users = Counter(master_user_IDs)
    c_books = Counter(master_book_IDs)

    # Let's report the effeciency
    user_eff = len(c_users.values()) / len(master_user_IDs)
    book_eff = len(c_books.values()) / len(master_book_IDs)

    print()
    print('Collected user effeciency = {0:0.2f}%'.format(user_eff * 100))
    print('Collected book effeciency = {0:0.2f}%'.format(book_eff * 100))

    # Now let's sort through the users first

    # Get a list of lists. Each entree is a list of the repeated user instances
    repeated_users_list = []
    repeated_indx = []
    id_counts = list(c_users.values())
    for i, curr_user_id in enumerate(list(c_users.keys())):
        if id_counts[i] > 1:
            temp_repeated_element = curr_user_id
            instance_list, temp_indices = get_repeated_instances(master_user_list, master_user_IDs, temp_repeated_element)

            repeated_users_list.append(instance_list)
            repeated_indx.append(temp_indices)

    x = 7

    # Now consolidate user lists
    consolidate_user_list(master_user_list, master_user_IDs, repeated_users_list, repeated_indx)





    # repeated_books = [ret]
    x = 7


    # Then we can
    repeated_books_id_list = []
    id_counts = list(c_books.values())
    for i, curr_book_id in enumerate(list(c_books.keys())):
        if id_counts[i] > 1:
            repeated_books_id_list.append( curr_book_id )

    # repeated_books = [ret]


