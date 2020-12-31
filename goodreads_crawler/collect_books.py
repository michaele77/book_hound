## This file will scrape goodreads popular book lists to fill out a list of ~5,000 books to scrape
## This will be recorded in a .txt file named "book_list.txt"
## The structure of the file will be:

##    BOOK ID  |  BOOK TITLE  |  BOOK AUTHOR  |   BOOK HREF LINK |  BOOK LIST NAME |  LIST HREF LINK | COLLECTED | DATE/TIME COLLECTED



#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import csv
import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver


#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#


chrome_options = webdriver.chrome.options.Options()
driver = webdriver.Chrome(options=chrome_options)


data_fields = ['Book ID', 'Book Title', 'Book Author', 'Book Link',
               'Book List Name', 'Book List Link', 'Collected', 'Date/Time Collected']

# Let's create a booklist from the most popular books:
year_list = [2010+i for i in range(1,11)]
genre_list = ['fiction',
              'mystery-thriller',
              'historical-fiction',
              'fantasy',
              'romance',
              'science-fiction',
              'horror',
              'humor',
              'nonfiction',
              'memoir-autobiography',
              'history-biography',
              'science-technology',
              'food-cookbooks',
              'graphics-novels-comics',
              'poetry',
              'debut-novel',
              'young-adult-fiction',
              'young-adult-fantasy']
choiceawards_list = []

for curr_year in reversed(year_list):
    for curr_genre in genre_list:
        choiceawards_list.append('https://www.goodreads.com/choiceawards/best-' + curr_genre + '-books-' + str(curr_year))





#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#

# From thread_spinner.py
def get_page(fnc_url_link):
    ##Below is the old code that WORKED
    driver.get(fnc_url_link)

    soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')

    time.sleep(1)

    return soup_toreturn


def extract_book_ids(in_soup):
    awarded_books = in_soup.select('.js-tooltipTrigger.tooltipTrigger')
    out_ids = [i.attrs['data-resource-id'] for i in awarded_books]

    out_hrefs = []
    out_title = []
    out_authors = []
    for cur_content in awarded_books:
        temp_content = cur_content.contents[1]

        out_hrefs.append( 'https://www.goodreads.com' + temp_content.attrs['href'].split('?')[0] )
        shared_str = temp_content.contents[0].attrs['alt'].split(' by ')
        out_title.append( shared_str[0] )
        out_authors.append(shared_str[1])
    out_list = []

    for i in range(len(out_ids)):
        out_list.append((out_ids[i], out_title[i], out_authors[i], out_hrefs[i]))

    return out_list


def create_log_file(fileName):
    # writing to csv file
    with open(fileName, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(data_fields)


def add_list_to_txt(list_link, tuple_list):
    list_name = list_link.split('/')[-1]

    with open('book_list.csv', 'a') as csvfile: #open in append mode
        csvwriter = csv.writer(csvfile)
        for curr_tuple in tuple_list:
            row_to_write = [curr_tuple[0], curr_tuple[1], curr_tuple[2], curr_tuple[3],
                            list_name, list_link, '0', 'N/A']
            csvwriter.writerow( row_to_write )






# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#


# Create proper main structure
if __name__ == "__main__":
    create_log_file('book_list.csv')
    print(choiceawards_list)

    for curr_link in choiceawards_list:


        # currSoup = get_page('https://www.goodreads.com/choiceawards/best-young-adult-fantasy-books-2020')
        currSoup = get_page(curr_link)
        curr_tuple_list = extract_book_ids(currSoup)

        # Add to the text file the collected book info with the respective list
        add_list_to_txt(curr_link, curr_tuple_list)



    pass




