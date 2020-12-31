"""
Filename: thread_spinner.py
Connection Graph:

+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+----+
+                                                                                                                      +
+                                +-----------------+                                                                   +
+                                +  collect_ips.py +  ---->  * ip_list.txt *                                           +
+                                +-----------------+                                                                   +
+                                        |                                                                             +
+    +------------------+                V                                                                             +
+    + collect_books.py +          * ip_list.pkl *                                                                     +
+    +------------------+                |                                                                             +
+           |                            V                                                                             +
+           V                  +---------------------+                                                                 +
+  * book_list.txt *  <---->   +  thread_spinner.py  +   ---->    * scraped_data/book_data_x.pkl *                     +
+                              +---------------------+                        |                                        +
+                                                                             V                                        +
+                                                                   +--------------------+                             +
+                                                                   +   build_network.py +  ---->  full_network.pkl    +
+                                                                   +--------------------+                             +
+                                                                            |                                         +
+                                                                            V                                         +
+                                                                       SQL DATABASE                                   +
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+----+


Function: Create threads that will be spun off to work on scraping users from a specified book.
          These threads will collect data about users and the books they rated, creating book/user nodes.
          At the end of each book, the data from these threads will be collected and appended.
          After each book, the currently constructed net will be saved with pickle to free up RAM.
          If the program is interrupted, only the progress on the current book will be interrupted

Inputs:  -A list of books to scrape stored in book_list.txt (save as text so it's readable).
         -A list of ips to use for scraping in ip_list.pkl.
         -How many threads to spin up (this could be done programmatically too).

Outputs: -Stored book/user network after each book in scraped_data/book_data_x.pkl.
         -Write back to book_list.txt to indicate that the book is stored.
         -Calling collect_ips.py programmatically if the collected IPs are no longer valid.


Author: Michael Ershov
Date: 12/12/20
"""

#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

from scraper_api import ScraperAPIClient

import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import numpy as np
import pickle
import sys
import copy
import concurrent.futures
import threading

# Do custom function imports
from config import get_scraper_API_KEY
from node_structure import BookNode
from node_structure import UserNode



#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#

API_KEY = get_scraper_API_KEY()
client = ScraperAPIClient(API_KEY)

API_KEY = '445b0c65f0d18958ea2a4cd0356bfdcb'

url_location = 'https://www.goodreads.com/book/show/'
book_reference_number = 186074 #Name of the Wind
# book_reference_number = 61535  #Selfish gene (sunbins fav)
# book_reference_number = 14891  #A Tree Grows in Brooklyn (Belindas fav)
book_reference_number = 35342928 # Age of War

chrome_options = webdriver.chrome.options.Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

#--------------------------------#
#  Goodreads Star Assignment     #
#--------------------------------#
#  Stars   |  field rating value #
#--------------------------------#
#   5      |  'it was amazing'   #
#   4      |  'really liked it'  #
#   3      |      'liked it'     #
#   2      |     'it was ok'     #
#   1      |  'did not like it'  #
#   N/A    |       No key        #
#--------------------------------#

star_assignment = {}

star_assignment['it was amazing']   = 5
star_assignment['really liked it']  = 4
star_assignment['liked it']         = 3
star_assignment['it was ok']        = 2
star_assignment['did not like it']  = 1


searchParam_max_rating_pages = 4
searchParam_max_users = 4




#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#


def get_page(fnc_url_link):
    # ####### REQUEST GET METHOD for URL
    # r = requests.get(fnc_url_link)
    #
    # ####### DATA FROM REQUESTS.GET
    # data = r.text
    # soup_toreturn = BeautifulSoup(data, 'lxml')

    ##Below is the old code that WORKED
    driver.get(fnc_url_link)

    soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')

    time.sleep(1)

    return soup_toreturn



def get_page_inf_scroll(fnc_url_link, curr_thread, scroll_num=20):
    ##Below is the new code for infinite scrolling

    print('Infinite page, thread {0}'.format(curr_thread))

    continueFlag = True
    pageIter = 1
    ratingsListFnc = []
    ratingsList = None
    ratingsScore_AVG = None
    ratingsScore_OWN_temp = None

    page_limit = searchParam_max_rating_pages ##Automatically stops if more than 5 pages
    star_limit = 3 ##Automatically stops once 3 or less stars encountered TODO: what if NONE is encountered?

    while continueFlag:
        print('Infinite page LOOPTIME, thread {0}'.format(curr_thread))
        append_string = '&page=' + str(pageIter)
        # driver.get(fnc_url_link+append_string)
        #
        # temp_soup = BeautifulSoup(driver.page_source, 'lxml')
        temp_soup = get_payload(fnc_url_link+append_string)

        small_ratingsList = temp_soup.select('.field.title')
        try:
            small_ratingsList.pop(0)
        except:
            print('Encountered private user')
            return -1, -1, -1 # error code

        small_ratingsScore_AVG = temp_soup.select('.field.avg_rating')  # This simply gets AVERAGE RATING OF THE BOOK
        small_ratingsScore_AVG.pop(0)
        small_ratingsScore_OWN = temp_soup.select('.staticStars.notranslate')
        # No need to pop from the notranslate selection

        ############################
        #####EXCTRACTION TIME#######
        ############################

        #Extract title string
        small_ratingsList = [ currRating.contents[1].contents[1].attrs for currRating in small_ratingsList ]

        #Extract the book's average rating from info string
        small_ratingsScore_AVG = [ float(currAVG.text.split('\n')[0].split(' ')[-1]) for currAVG in small_ratingsScore_AVG ]

        #Extract the actual score from the per-book rating
        for curri, currPers in enumerate(small_ratingsScore_OWN):
            try:
                small_ratingsScore_OWN[curri] = star_assignment[currPers.attrs['title']]
            except:
                small_ratingsScore_OWN[curri] = None


        ############################
        ####END EXCTRACTION TIME####
        ############################


        if not ratingsList:
            ratingsList = small_ratingsList.copy()
            ratingsScore_AVG =  small_ratingsScore_AVG.copy()
            ratingsScore_OWN = small_ratingsScore_OWN.copy()
        else:
            ratingsList = ratingsList + small_ratingsList.copy()
            ratingsScore_AVG = ratingsScore_AVG + small_ratingsScore_AVG.copy()
            ratingsScore_OWN = ratingsScore_OWN + small_ratingsScore_OWN.copy()

        # To solve any bugs that arise when the ratings are None (not rated)
        for temp_iter in range(len(small_ratingsScore_OWN)):
            if small_ratingsScore_OWN[temp_iter] is None:
                small_ratingsScore_OWN[temp_iter] = 0

        # ratingsList_to_add = temp_soup.select('.field.title')[1:]
        if not small_ratingsList:
            print('We have hit the final page! final page count: {}'.format(pageIter))
            continueFlag = False
            #Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages

        elif pageIter >= page_limit:
            print('We have hit the set page limit! final page count: {}'.format(pageIter))
            continueFlag = False
            # Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages



        elif any(temp_comp <= star_limit for temp_comp in small_ratingsScore_OWN):
            print('We have hit the "moderately bad" rated books! final page count: {}'.format(pageIter))
            #Remove any indices that are beyond the first 'setStar' rating
            try:
                first_index_beyond = ratingsScore_OWN.index(star_limit)
            except:
                try:
                    first_index_beyond = ratingsScore_OWN.index(2)
                except:
                    try:
                        first_index_beyond = ratingsScore_OWN.index(1)
                    except:
                        try:
                            first_index_beyond = ratingsScore_OWN.index(None)
                        except:
                            first_index_beyond = 1 #final recourse...this should never happen



            ratingsList = ratingsList[0:first_index_beyond]
            ratingsScore_AVG = ratingsScore_AVG[0:first_index_beyond]
            ratingsScore_OWN = ratingsScore_OWN[0:first_index_beyond]

            continueFlag = False
            # Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages


        else:
            print('currently at {}'.format(len(ratingsList)))
            pageIter += 1



    return ratingsList, ratingsScore_AVG, ratingsScore_OWN




def get_payload(link_to_visit):
    payload = {'api_key': API_KEY, 'url': link_to_visit}
    r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)

    if r.status_code == 200:
        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
    else:
        print('STATUS CODE: {0}'.format(r.status_code))

    return soup


def get_concurrent_requests():
    usage = client.account()
    return usage['concurrentRequests']


def get_next_availability(list_to_parse):
    for i, trav_bool in enumerate(list_to_parse):
        if not trav_bool:
            return i


def extract_img(img_src_str):
    response = requests.get(img_src_str)
    out = response.content
    return out

def save_img_file(book_dict, inBits):
    file = open('cover_photos/' + book_dict['title'] + '_' + str(book_dict['ID']) + '.jpg', 'wb')
    file.write(inBits)
    file.close()

def get_genre_list(book_info):
    # This function will unpack the "genre" list and will structure the data in a list
    # Each item in the list will be a tuple: (plain string, href, user count)
    # Note that plain string should be used as a reference
    # Note that string and href could be lists in case of super genres

    element_list = soup.select('.elementList')
    element_list.pop(0) # Clear out the first garbage entree

    output_list = []
    for curr_element in element_list:
        temp_content = curr_element.contents

        # Do the user count first, it's easiest
        user_count = temp_content[3].contents[1].contents[0] # outputs a string of form 'XXXX users'
        temp_split = user_count.split(' ') # Split at the space between number and 'users'
        user_count = int(temp_split[0].replace(',', '')) # Replace any commas with nothing to make it parseable

        # Now do the plain string + href lists
        plain_string_list = []
        href_list = []

        temp_combo_list = temp_content[1].contents
        for curr_combo in temp_combo_list:
            try:
                plain_string_list.append( str(curr_combo.contents[0]) )
                href_list.append( str(curr_combo.attrs['href']) )
            except:
                # If we hit here, it's some sort of newline or something
                continue

        genre_tuple = (plain_string_list, href_list, user_count)

        output_list.append( genre_tuple )

    return output_list



def hit_ratings_button(page_soup, i):
    # fish out the ratings link on the top left hand corner of the user's page
    # add it to the dictionary once we have it
    try:
        reviewer_info[i]['ratings link'] = page_soup.select('.profilePageUserStatsInfo')[0].contents[1].attrs['href']
    except:
        try:
            # Author's page has a different layout type...
            reviewer_info[i]['ratings link'] = page_soup.select('.smallText')[0].contents[1].attrs['href']
            print('On an authors page!')
        except:
            # Some people make their profiles private...
            user_text = page_soup.select('#privateProfile')[0].text
            usertextList = []
            usertextList.append(user_text.split('This')[1][1:20])
            usertextList.append(user_text.split('Sign in to ')[1].split('\n')[0])

            print('On a private page, so no content available')
            print('From users page: {0}, {1}'.format(usertextList[0], usertextList[1]))
            print('skipping to next reviewer')

            return 77 #error code, i guess

def add_userRating_link(i):
    pre_string = 'https://www.goodreads.com/review/list/'
    post_string = '?sort=rating&view=reviews'
    mid_string_list = reviewer_info[i]['link'].split('/')
    mid_string = mid_string_list[-1]

    ratinglist_link = pre_string + mid_string + post_string
    reviewer_info[i]['ratings link'] = ratinglist_link


def add_to_reviewerInfo(curr_user, i, curr_thread):
    reviewer_info[i] = {}
    reviewer_info[i]['name'] = curr_user.attrs['name']
    reviewer_info[i]['link'] = curr_user.attrs['href']

    # extract the user ID from the first part of the href
    reviewer_info[i]['ID'] = int(reviewer_info[i]['link'].split('/')[-1].split('-')[0])

    # Add the link to the reviewer_info structure
    add_userRating_link(i)

    print('Thread {0} on index {1}'.format(curr_thread, i))


    ratingsList, ratingsScore_AVG, ratingsScore_OWN = get_page_inf_scroll(reviewer_info[i]['ratings link'], curr_thread)

    # Check if we hit a dead user
    if ratingsList == -1:
        print('Thread {0} hit a private user, aborting this user'.format(curr_thread))
        return

    print('Thread {0} after infinite scroll!'.format(curr_thread))

    reviewer_info[i]['ratings'] = []
    for j in range(len(ratingsList)):
        reviewer_info[i]['ratings'].append(ratingsList[j])
        book_AVG_score = ratingsScore_AVG[j]  # currently not used...include in the book node in the future
        reviewer_info[i]['ratings'][j]['score'] = ratingsScore_OWN[j]

        # Also include the unique ID for each book for easy identification later on
        try:
            reviewer_info[i]['ratings'][j]['ID'] = int(reviewer_info[i]['ratings'][j]['href'].split('/')[-1].split('-')[0])
        except:
            reviewer_info[i]['ratings'][j]['ID'] = int(reviewer_info[i]['ratings'][j]['href'].split('/')[-1].split('.')[0])




def review_collection_thread_function(thread_num):
    print('At thread number ' + str(thread_num))
    while not all(threading_taken): #continue while not all of threading_taken is true
        # if get_concurrent_requests() < 5:
        with threading.Lock():
            link_indx = get_next_availability(threading_taken)
            threading_taken[link_indx] = True
        print(threading_taken)

        print('Thread {0} has link {1}'.format(thread_num, link_indx))
        add_to_reviewerInfo(book_info['reviewers'][link_indx], link_indx, thread_num)
        # get_payload(example_list[link_indx])


    print('Finished with thread {0}'.format(thread_num))







#-----------------------------------------------------------------------------#
#                                   MAIN                                      #
#-----------------------------------------------------------------------------#

if True:
    soup = get_page(url_location+str(book_reference_number))

    #Get general book info
    book_info = {}

    book_info['ID'] = book_reference_number
    book_info['title'] = soup.select('#bookTitle')[0].text.strip()              # book title
    book_info['author'] = soup.select('.authorName')[0].text.strip()            # author
    book_info['meta'] = soup.select('#bookMeta')[0].text.strip()                # book meta
    book_info['details'] = soup.select('#details')[0].text.strip()              # book details (stats)

    #Extra info added:
    book_info['series'] = soup.select('#bookSeries')[0].text.strip()            # book series
    book_info['summary'] = soup.select('#descriptionContainer')[0].text.strip() # summary
    book_info['imageSource'] = soup.select('#coverImage')[0].attrs['src']       # jpg asset link of book cover

    image_bits = extract_img(book_info['imageSource'])
    save_img_file(book_info, image_bits)

    book_info['imageBinary'] = image_bits                                       # Actual image bitds
    book_info['genres'] = get_genre_list(book_info)                             # Genre list
    book_info['href'] = 'https://www.goodreads.com/book/show/' + str(book_info['ID'])



    for i,v in enumerate(book_info):
        print('Book {0}: {1}'.format(i,v))

    #Now, step into the 30 reviewers on the first page
    # book_info['reviewers'] = list(soup.select('.user')) #Raw format (not text) of all reviewers, CONVERT TO LIST FOR EASY CONCATENATION
    book_info['reviewers'] = []

    #Now we need to close the popup that happens if we're not logged in...Find the close button by xpath:
    time.sleep(.5)
    close_XPATH = '/html/body/div[3]/div/div/div[1]/button/img'
    element = driver.find_element_by_xpath(close_XPATH)
    element.click()
    time.sleep(2)

    #Append however many user pages we want to go through!
    user_page_num = searchParam_max_users
    for cnt_i in range(user_page_num):
        #instead of grabbing href link from the parsed XML, use a selenium click
        #won't work otherwise (since it uses a JSON request to get the next page)
        time.sleep(2)  # to avoid the random-length HTML garbage anti-attack mechanism

        # The first click when cnt_i == 0 just brings us down to the bottom page, and doesn't bring new info...
        element = driver.find_element_by_class_name('next_page')
        element.click()

        curr_page_soup = BeautifulSoup(driver.page_source, 'lxml')
        curr_page_reviews = list(curr_page_soup.select('.user'))

        # Now, if the user's review is 3 or less stars, kick them off the list
        # reviewer_stars = list(curr_page_soup.select('.staticStars.notranslate'))
        # reviewer_stars = reviewer_stars[2:]  # Now this list corresponds to the reviewer list
        # reviewer_stars = [curri.attrs['title'] for curri in reviewer_stars]  # Now should be the pure string

        # Fixing a bug! This would offset users and stars if no stars were given...
        # By default, include these no stars as 4
        info_list = list(curr_page_soup.select('.reviewHeader.uitext.stacked'))
        reviewer_stars = []
        for iii, curr_user_info in enumerate(info_list):
            try:
                temp_str = curr_user_info.contents[5]['title']
            except:
                print('Found a no-star reviewer! Lets add them (index {0})'.format(iii))
                temp_str = 'really liked it' # fake a 4 star rating!
            reviewer_stars.append(temp_str)


        kickoff_list = []
        for iterI, curr_stars in enumerate(reviewer_stars):
            star_num = star_assignment[curr_stars]
            if star_num <= 3:
                # If the review was not good, skip this person
                # Add to a "kick off" list first so that a pop error doesnt occur
                print('POP off person {0}'.format(iterI))
                kickoff_list.append(iterI)

        # Now proceed to actually pop these people
        for index in sorted(kickoff_list, reverse=True):
            del curr_page_reviews[index] # del is same as pop, but doesnt return a value (so its probably faster...)


        book_info['reviewers'] = book_info['reviewers'] + curr_page_reviews



    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Threading time!
    ## Spin off however many threads is allowed, make each run the function that extracts reviewers' info
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~


    reviewer_info = [0]*len(book_info['reviewers'])
    threading_taken = [False]*len(book_info['reviewers'])


    ## Spin up the threads!
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(review_collection_thread_function, range(5))





## ~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Done with scraping!
## Save to file
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ogRecLimit = sys.getrecursionlimit()
    sys.setrecursionlimit(100000)
    with open('temp_data_0.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([book_info, reviewer_info], f)


# Getting back the objects:
with open('temp_data_0.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    book_info, reviewer_info = pickle.load(f)

sys.setrecursionlimit(100)





## ~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Add info to nodes
## leverage the node_structure.py file imported
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Create the network with the correct class assignments
#For each book (in this case, 1) iterate through all of the users
#Create a user node for each user, and a book node for each of their corresponding rated books
#For each user's books, search that this book is not in the network before adding it

covered_books = [] #list to keep track of books that have been added to the net
covered_users = [] #list to keep track of users that have been added to the net
book_idx = 0
for idx_user in range(len(reviewer_info)):
    #Create the user node and add it to the tracker list
    currUser_dict = reviewer_info[idx_user]
    try:
        user_instance = UserNode(currUser_dict)
    except:
        print('DEAD USER~~~~')
        print('PASSING...')
        continue

    covered_users.append(user_instance)
    user_idx = covered_users.index(user_instance)

    #Now, iterate through the user's books
    for idx_book in range(len(currUser_dict['ratings'])):
        currBook_dict = currUser_dict['ratings'][idx_book]

        #Check that the book is not in the net already
        #Track by full object pointer in the list
        book_instance = BookNode(currBook_dict)
        covered_book_hrefs = [i.href for i in covered_books]

        if book_instance.href not in covered_book_hrefs: #use hrefs for consistent string comprehension
            covered_books.append( book_instance )
            book_idx = len(covered_books) - 1
        else:
            #find the existing object in the list by searching through the hrefs
            book_idx = covered_book_hrefs.index(book_instance.href)

        #Now that we have the correct book object, let's add to both the book and user reference lists
        #first is book instance --> rater
        inRater = covered_users[user_idx]
        inScore = currBook_dict['score']
        covered_books[book_idx].add_rater(inRater, inScore)


        #second is user instance --> book
        inBook = covered_books[book_idx]
        inScore = currBook_dict['score']
        covered_users[user_idx].add_book(inBook, inScore)



# Finally...let's save the original book that gave us these users to begin with
# First check that the book isn't already in the covered_books list (it probably is lol)
master_book_id = book_info['ID']
id_list = [icc.ID for icc in covered_books]
if master_book_id in id_list:
    master_idx = id_list.index(master_book_id)

else:
    try:
        master_book_instance = BookNode(book_info)
    except:
        print('Using old book_info structure...creating href')
        book_info['href'] = 'https://www.goodreads.com/book/show/' + str(book_info['ID'])
        master_book_instance = BookNode(book_info)

    covered_books.append(master_book_instance)
    master_idx = id_list.index(master_book_instance.ID)

covered_books[master_idx].add_full_book_info(book_info)

# Now, add to each user that reviewed the book (which is all covered users) to the reviewed user list
covered_books[master_idx].add_reviewers(covered_users)

# Finally, add this master book as an item in the book list for each user
# To perserve structure and give identification, add as a 4.5 score
for each_user in covered_users:
    each_user.add_book(covered_books[master_idx], 4.5)




# Save the newly created covered_users and covered_books lists to test the file size!

sys.setrecursionlimit(100000)
with open('temp_data_0_nodalStructure.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([covered_users, covered_books], f)



## STATS:
## Took 13 minutes with 4 threads (didn't seem like thread 0 was up...) for 150 users...
## Took 810-395 = 415 requests

x = 7 # BREAKLOOP...stop here

