## NOTE: Instead of using this, use pure command line syntax:
## sqlite3 xxx.db .dump > yyy.sql
##      Where xxx = original file name, yyy = desired destination filename

## Super simple script to dump a sqlite3 file into a .sql file
## Used to import into AWS hosted server through mySQL workbench

import sqlite3
con = sqlite3.connect('bookhound_test1_index.db')

f = open('bookhound_dump2.sql', 'w')
for i,line in enumerate(con.iterdump()):
    print(i)
    f.write('%s\n' % line)
f.close()