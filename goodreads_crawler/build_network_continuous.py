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

## NOTE: This differs from build_network in that here we are creating the repeated indices list and calculating the
# combination algo all in one step, which hopefully relieves the RAM issue that we ran into with build_network




#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import os
import pickle
from collections import Counter
import numpy as np
import datetime
import sys
import gc


#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#

directory_list = os.listdir('scraped_data/')
try:
    directory_list.remove('.DS_Store')
    print('Removed DS_Store')
except:
    print('No DS_store to pop (thankfully)')


#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#


def get_repeated_instances(instance_arr, id_list_toCheck, ID_toCheck):
    # Check IDs
    repeated_indx = [i for i, x in enumerate(id_list_toCheck) if x == ID_toCheck]
    instance_list = [instance_arr[i] for i in repeated_indx]
    return instance_list, repeated_indx

def get_repeated_book_instances(instance_arr, id_list_toCheck, title_to_check):
    # Check titles
    # Use numpy to speed this up a bit
    # string_comp_list = [i.title for i in instance_arr]
    # string_comp_arr = np.array(string_comp_list)
    # bool_arr = string_comp_arr == title_to_check

    repeated_indx = []
    instance_list = []
    for i, curr_Inst in enumerate(instance_arr):
        curr_str = curr_Inst.title
        if curr_str == title_to_check:
            repeated_indx.append(i)
            instance_list.append(instance_arr[i])

    return instance_list, repeated_indx

    # repeated_indx = [i for i, x in enumerate(instance_arr) if x.title == title_to_check]
    # instance_list = [instance_arr[i] for i in repeated_indx]
    # return instance_list, repeated_indx



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




def continuous_consolidate_book_list(fnc_master_list, fnc_id_list, fnc_book_inst, fnc_book_idx):
    indx_to_pop = []
    # For each repeated book, update one master node, and pop the rest from the master list
    # Master shall be the book with full params, index 0 otherwise

    has_master_flag = False

    curr_book_list = fnc_book_inst
    curr_indx_list = fnc_book_idx

    # If one of the books has full params set that as the master
    truthArr = [curI.has_full_params for curI in curr_book_list]
    if any(truthArr):
        print('We got a full parameters book!')
        find_true_list = [cci for cci, x in enumerate(truthArr) if x]
        master_node = curr_book_list[ find_true_list[0] ]
        master_idx = find_true_list[0]
        has_master_flag = True
    # Otherwise, choose the instance with the most raters! one to be the master
    else:
        max_rater_len = 0
        chosen_one = None
        try:
            pointing_val = int(curr_book_list[0].href.split('/')[-1].split('-')[0])
        except:
            pointing_val = int(curr_book_list[0].href.split('/')[-1].split('.')[0])
        for ii, cb in enumerate(curr_book_list):
            if len(cb.raters) > max_rater_len and cb.ID == pointing_val:
                max_rater_len = len(cb.raters)
                chosen_one = cb
                master_idx = ii

        master_node = chosen_one
        # master_node = curr_book_list[0]
        # master_idx = 0

    for vv, other_node in enumerate(curr_book_list):
        if vv == master_idx:
            # Already set master node
            pass
        else:
            # Now lets combine raters lists
            # Check to make sure that the user is not double represented!
            new_user_list = other_node.raters
            new_ID_list = other_node.raters_ID
            for iterC in range(len(new_ID_list)):
                curr_user = new_user_list[iterC]
                curr_ID   = new_ID_list[iterC]


                # If we check that its not double represented, then we're in baby
                if curr_ID not in master_node.raters_ID:
                    # print('adding a new one...')

                    # Add it to the master node
                    master_node.raters.append(curr_user)
                    master_node.raters_ID.append(curr_ID)

                else:
                    pass

            # Add it to the pop list
            if has_master_flag:
                print('before: {0}'.format(len(indx_to_pop)))
            indx_to_pop.append(curr_indx_list[vv])
            if has_master_flag:
                print('after: {0}'.format(len(indx_to_pop)))



    # Now go through the pop list backwards and pop em all off!
    # indx_to_pop.sort()  # sort it first inplace
    # Now, because we were searching for title only, we can get a repeat offense of a duplicate ID AND a mismatch string
    # So it would be double counted in our indx_to_pop list
    # So reduce the list down to only the unique elements
    unique_popList = list(Counter(indx_to_pop).keys())
    unique_popList.sort()
    for i in reversed(unique_popList):
        fnc_master_list.pop(i)
        fnc_id_list.pop(i)


def search_book_list(master_list, search_term, search_field = 'title'):
    if search_field == 'title':
        searched_list_indx = [i for i,v in enumerate(master_list) if v.title == search_term]
    elif search_field == 'ID':
        searched_list_indx = [i for i, v in enumerate(master_list) if v.ID == search_term]
    elif search_field == 'href':
        searched_list_indx = [i for i, v in enumerate(master_list) if v.href == search_term]
    elif search_field == 'rater number greater than':
        out_instance_list = []
        out_idx_list = []
        for curI, curr_search in enumerate(master_list):
            if len(curr_search.raters) > search_term:
                out_instance_list.append(curr_search)
                out_idx_list.append(curI)
        return out_idx_list, out_instance_list

    elif search_field == 'title contains':
        out_instance_list = []
        out_idx_list = []
        for curI, curr_search in enumerate(master_list):
            if search_term.lower() in curr_search.title.lower():
                out_instance_list.append(curr_search)
                out_idx_list.append(curI)
        return out_idx_list, out_instance_list


    # TODO: Add more terms here! For example genre (contains any), reviewer number, etc

    searched_indx = searched_list_indx[0]
    return searched_indx, master_list[searched_indx]


# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#


# Create proper main structure
if __name__ == "__main__":
    master_user_list = []
    master_book_list = []

    distilled_book_list = [] # These are the final lists with repeated books/indices removed
    distilled_book_IDs = [] # These are the final lists with repeated books/indices removed

    gc.disable()

    for curr_pickle in directory_list:

        with open('scraped_data/' + curr_pickle, 'rb') as f:  # Python 3: open(..., 'rb')
            print('loaded {0}'.format(curr_pickle))
            unpacked_user, unpacked_book = pickle.load(f)

        master_user_list = master_user_list + unpacked_user

        master_book_list = master_book_list + unpacked_book
        distilled_book_list = distilled_book_list + unpacked_book

    gc.enable()



    # Report  collected number
    print()
    print('We have collected the following number of nodes:')
    print('{0} users'.format(len(master_user_list)))
    print('{0} books'.format(len(master_book_list)))


    # Now that we have everything appended, let's see how many repeats we have
    master_user_IDs = [i.ID for i in master_user_list]
    master_book_IDs = [i.ID for i in master_book_list]
    distilled_book_IDs = master_book_IDs.copy()

    c_users = Counter(master_user_IDs)
    c_books = Counter(master_book_IDs)

    # Let's report the effeciency
    user_eff = len(c_users.values()) / len(master_user_IDs)
    book_eff = len(c_books.values()) / len(master_book_IDs)

    print()
    print('Collected user effeciency = {0:0.2f}%'.format(user_eff * 100))
    print('Collected book effeciency = {0:0.2f}%'.format(book_eff * 100))

    # Now let's sort through the users first

    print()
    print('Initiating User List')
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

    print('Finished User List')

    # Now consolidate user lists
    consolidate_user_list(master_user_list, master_user_IDs, repeated_users_list, repeated_indx)

    # First, save the user network
    sys.setrecursionlimit(100000)
    currTime = str(datetime.datetime.now())
    with open('master_checkpoints/masterUserList_' + currTime + '.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([master_user_list, master_user_IDs], f)



    # Get a list of lists. Each entree is a list of the repeated user instances
    repeated_books_list = []
    repeated_books_indx = []
    id_counts = list(c_books.values())

    save_period = 100000
    update_period = 100
    prevSave = 0
    repet_iter = 0

    for i, curr_book_id in enumerate(list(c_books.keys())):

        if id_counts[i] > 1:
            ins_list_temp = [xx for xx,vvv in enumerate(master_book_list) if vvv.ID == curr_book_id]
            this_title = master_book_list[ins_list_temp[0]].title #Doesn't matter which one, they're identical
            repeated_book_inst, repeated_book_indx = get_repeated_book_instances(distilled_book_list, distilled_book_IDs,
                                                                 this_title)

            continuous_consolidate_book_list(distilled_book_list, distilled_book_IDs, repeated_book_inst,
                                             repeated_book_indx)


            repet_iter += 1

        if i % update_period == 0 and i is not 0:
            # just a slot to update/report on parameters more frequently than our save period!
            print('Repition iteration counter is {0}'.format(repet_iter))



        print(str(i) + ' / ' + str(len(distilled_book_IDs)))
        # if i % 100 == 0:
        #     print(i)



    print()
    print('Finished getting all of the repeat lists')
    print()
    print()



    # save these networks
    sys.setrecursionlimit(100000)
    currTime = str( datetime.datetime.now() )
    with open('master_checkpoints/masterLists_' + currTime +'.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([distilled_book_list, master_user_list, distilled_book_IDs, master_user_IDs], f)


    # Note: Max pickle size is 155MB...



    ## BIG NOTE on searching by title:
    ## Many books (apparently) have 'twins' or aliases
    ## These are seemingly the exact same book, but with different IDs, summary, and maybe cover
    ## However, the reviews are shared and its the same book

    ## This usually happens as a result of a best-seller making another page to spice it up or something
    ## This is usually not an issue, because the 'main' page that we scraped usually has way more raters anyway,
    ## and the aliased versions usually barely have any

    ## However, when we are collecting full parameters for all of the books after scraping, we should add a field in
    ## the book node indicating 'aliases' and perhaps just combining the nodes entirely. We could also do it here later

    ## One okish solution is to 1) change what qualifies as a repitition (check ID AND name cohesion)
    ##                          2) When picking which master to choose, choose the one that has the most raters (not neccesary)
    ## TODO: implement the stuff described above~~

    # Now we have a condensed master and user list, this is distilled gold!
    # Now we can do fun things like search our master lists based on things like 'book title'

    searched_index, returned_inxstance = search_book_list(master_book_list, 'Anxious People' , search_field = 'title')
    searched_index, returned_instance = search_book_list(master_book_list, 'My Dark Vanessa', search_field='title')

    searched_index, returned_instance = search_book_list(master_book_list, 44890081, search_field='ID')

    # urlNum = [1]  # some harry potter book
    # urlNum = [20518872]  # The Three Body Problem
    # urlNum = [6266872]  # The Name of the Wind
    # # urlNum = [13569581] #Blood Song
    # urlNum = [14891]  # A Tree Grows in Brooklyn (Belindas fav)
    # urlNum = [28077464] #Night school (gma fav)
    # urlNum = [61535] #Selfish gene (sunbins fav)
    # urlNum = [13376] #The House of scorpion (Kim's fav)
    searched_index, returned_instance = search_book_list(master_book_list, 6266872, search_field='ID') # Name of the wind
    a = returned_instance.title
    searched_index, returned_instance = search_book_list(master_book_list, a,
                                                         search_field='title')

    searched_index, returned_instance = search_book_list(master_book_list, 20518872, search_field='ID')  # The Three Body Problem
    a = returned_instance.title
    searched_index, returned_instance = search_book_list(master_book_list, a,
                                                         search_field='title')

    searched_index, returned_instance = search_book_list(master_book_list, 13569581, search_field='ID')  # Blood Song
    a = returned_instance.title
    searched_index, returned_instance = search_book_list(master_book_list, a,
                                                         search_field='title')

    searched_index, returned_instance = search_book_list(master_book_list, 14891, search_field='ID')  # A Tree Grows in Brooklyn (Belindas fav)
    a = returned_instance.title
    searched_index, returned_instance = search_book_list(master_book_list, a,
                                                         search_field='title')

    # searched_index, returned_instance = search_book_list(master_book_list, 61535, search_field='ID')  # Selfish gene


