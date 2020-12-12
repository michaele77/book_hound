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




