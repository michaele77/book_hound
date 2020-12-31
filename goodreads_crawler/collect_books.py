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
from collections import Counter
import datetime

#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#



data_fields = ['Book ID', 'Book Title', 'Book Author', 'Book Link',
               'Book List Name', 'Book List Link', 'Collected', 'Date/Time Collected']

# Let's create a booklist from the most popular books:
year_list = [2010+i for i in range(1,11)]
genre_list = ['fiction-books',
              'mystery-thriller-books',
              'historical-fiction-books',
              'fantasy-books',
              'romance-books',
              'science-fiction-books',
              'horror-books',
              'humor-books',
              'nonfiction-books',
              'memoir-autobiography-books',
              'history-biography-books',
              'science-technology-books',
              # 'food-cookbooks', # Who tries to find more cookbooks...
              'graphic-novels-comics',
              'poetry-books',
              'debut-novel',
              'young-adult-fiction-books',
              'young-adult-fantasy-books',
              # all of the genres below are only for a few years...
              'debut-goodreads-author',
              'of-the-best']
choiceawards_list = []

for curr_year in reversed(year_list):
    for curr_genre in genre_list:
        choiceawards_list.append('https://www.goodreads.com/choiceawards/best-' + curr_genre + '-' + str(curr_year))

master_ID_check = []




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
        # Check that the ID has not been encountered
        if out_ids[i] not in master_ID_check:
            master_ID_check.append(out_ids[i])
            out_list.append((out_ids[i], out_title[i], out_authors[i], out_hrefs[i]))
        else:
            print('Skipping ID {0}, its already in the list!'.format(out_ids[i]))

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



def exctract_csv_to_list():
    with open('book_list.csv', 'r') as csvfile: #open in read mode
        csvreader = csv.reader(csvfile)
        out_list = []

        for row in csvreader:
            out_list.append(row)

    return out_list


def get_latest_id():
    with open('book_list.csv', 'r') as csvfile: #open in read mode
        csvreader = csv.reader(csvfile)

        # Assign vars to ERRORCODES so we know when the list is finished
        next_indx_toCollect = 'ERRORCODE'
        next_ID_toCollect = 'ERRORCODE'

        for i, row in enumerate(csvreader):
            if row[6] == '1':
                next_indx_toCollect = i
                next_ID_toCollect = row[0]
                break


    return next_indx_toCollect, next_ID_toCollect


def write_back_list( list_to_write ):
    # Overwrite the csv file
    with open('book_list.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        for curr_row in list_to_write:
            csvwriter.writerow( curr_row )



def mark_line_as_finished(index_toMark):
    with open("book_list.csv", "r+") as f:
        csvreader = csv.reader(f)

        contents = []
        # gives you a list of the lines
        for row in csvreader:
            contents.append(row)


        # delete the old line and insert the new one
        temp_list = contents.pop(index_toMark)

        # Now modify the list to change the 'collected' and 'dates' columns
        temp_list[6] = '1'
        temp_list[7] = str( datetime.datetime.now() )

        contents.insert(index_toMark, temp_list)
        # # join all lines and write it back
        # contents = "".join(contents)

        write_back_list( contents )
        pass



# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#


# Create proper main structure
if __name__ == "__main__":

    chrome_options = webdriver.chrome.options.Options()
    driver = webdriver.Chrome(options=chrome_options)


    # if True:
    create_log_file('book_list.csv')
    print(choiceawards_list)

    for curr_link in choiceawards_list:


        # currSoup = get_page('https://www.goodreads.com/choiceawards/best-young-adult-fantasy-books-2020')
        currSoup = get_page(curr_link)
        curr_tuple_list = extract_book_ids(currSoup)

        # Add to the text file the collected book info with the respective list
        add_list_to_txt(curr_link, curr_tuple_list)


    master_list = exctract_csv_to_list()



    pass




