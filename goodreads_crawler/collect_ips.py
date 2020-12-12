"""
Filename: collect_ips.py
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


Function: Srape a free ip website and collect a given number of ips.
          Store these IPs for future use in a pkl and txt file.
          This functionality should be wrapped in a function so it can be imported and called in thread_spinner.py.

Inputs:  -Number of IPs to scrape and website (store programmtically).

Outputs: -List of IPs in ip_list.pkl.
         -A list of IPs in ip_list.txt.

Author: Michael Ershov
Date: 12/12/20
"""



#############################
######    Imports     #######
#############################
import os


#############################
######    Defines     #######
#############################
proxy_site_str = 'http://www.freeproxylists.net/'


#############################
######   Functions    #######
#############################

