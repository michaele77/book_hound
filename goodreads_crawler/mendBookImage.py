## This file takes a completed mongoDB graph, then searches through the graph for non-full parameter books
## If a non-full parameter book is found, it will go and scrape goodreads for the rest of that parameters of that book
## We have 500,000 books, so this is expected to take about 500,000/60/60 = 139 hours, so let's run this when we can!


## IGNORE BELOW. We will just re-scrape all of the books
## Side node...the originally scraped books do not contain correct genres (they omit the top genre)
## So keep a pointer to the originally scraped books somehow and if we encounter one of them, re-scrape their genres




#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import sys
import pickle
import time
import os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import requests
import pymongo

#-----------------------------------------------------------------------------#
#                             GLOBAL DEFINES                                  #
#-----------------------------------------------------------------------------#


url_location = 'https://www.goodreads.com/book/show/'
# book_reference_number = 186074 #Name of the Wind
# book_reference_number = 61535  #Selfish gene (sunbins fav)
# book_reference_number = 14891  #A Tree Grows in Brooklyn (Belindas fav)
# book_reference_number = 35342928 # Age of War

chrome_options = webdriver.chrome.options.Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


#-----------------------------------------------------------------------------#
#                                Functions                                    #
#-----------------------------------------------------------------------------#

## Stole a lot of these from thread_spinney.py
## No sense in doing extra work right?
def save_img_file(book_dict, inBits):
    try:
        file = open('mend_DB_imgs/' + book_dict['title'] + '_' + str(book_dict['ID']) + '.jpg', 'wb')
    except:
        # We're here if the title contains a '/', which confuses the directory os...lol
        # Replace it with a dash
        new_str = book_dict['title'].replace('/', '-')
        file = open('mend_DB_imgs/' + new_str + '_' + str(book_dict['ID']) + '.jpg', 'wb')

    file.write(inBits)
    file.close()


def get_page(fnc_url_link):

    ##Below is the old code that WORKED
    driver.get(fnc_url_link)
    soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')

    time.sleep(1)

    return soup_toreturn


def extract_img(img_src_str):
    response = requests.get(img_src_str)
    out = response.content
    return out


def get_genre_list(book_info):
    # This function will unpack the "genre" list and will structure the data in a list
    # Each item in the list will be a tuple: (plain string, href, user count)
    # Note that plain string should be used as a reference
    # Note that string and href could be lists in case of super genres

    element_list = soup.select('.elementList')
    element_list.pop(0) # Clear out the first garbage entree

    try:
        temp_x = element_list[0].contents[3].contents[1].contents[0]
    except:
        print('First element is garbage (again)')
        element_list.pop(0)


    output_list = []
    for trackerI, curr_element in enumerate(element_list):
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

        genre_tuple = [plain_string_list, user_count]

        output_list.append( genre_tuple )

    return output_list



# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#

if __name__ == "__main__":
    ## First, we should check if we have made a pickle of the already full-paramed books

    directory_list = os.listdir('mend_DB_imgs/')
    try:
        print('Removed DS_Store')
        directory_list.remove('.DS_Store')
    except:
        print('No DS_store to pop (thankfully)')

    checkList_location = 'mend_DB_imgs'


    ## Let's load in our mongoDB and convert stuff to lists

    dbName = "bookhound_mongodb_toMend"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbName]
    print("Got it")

    bookCol = mydb["books"]
    userCol = mydb["users"]

    DB_books = [*bookCol.find()]
    DB_users = [*userCol.find()]

    ## Now we can loop through every book ID
    for curBook in DB_books:

        if curBook['fullParameter'] == 0 or curBook['fullParameter'] == 1 or curBook['fullParameter'] == False:
            print('scraping book {0}'.format(curBook['title']))
            ID_toScrape = curBook["_id"]
            book_reference_number = int(ID_toScrape)
            soup = get_page(url_location + str(book_reference_number))

            # Get general book info
            book_info = {}

            book_info['ID'] = book_reference_number
            book_info['title'] = soup.select('#bookTitle')[0].text.strip()  # book title
            book_info['author'] = soup.select('.authorName')[0].text.strip()  # author
            book_info['meta'] = soup.select('#bookMeta')[0].text.strip()  # book meta
            book_info['details'] = soup.select('#details')[0].text.strip()  # book details (stats)

            # Extra info added:
            book_info['series'] = soup.select('#bookSeries')[0].text.strip()  # book series
            book_info['summary'] = soup.select('#descriptionContainer')[0].text.strip()  # summary
            book_info['imageSource'] = soup.select('#coverImage')[0].attrs['src']  # jpg asset link of book cover

            image_bits = extract_img(book_info['imageSource'])
            save_img_file(book_info, image_bits)

            book_info['imageBinary'] = image_bits  # Actual image bitds
            book_info['genres'] = get_genre_list(book_info)  # Genre list
            book_info['href'] = 'https://www.goodreads.com/book/show/' + str(book_info['ID'])


        else:
            print('Skipped book {0}, since fullParam was {1}'.format(curBook['title'], curBook['fullParameter']))



    print('We are finished!')



