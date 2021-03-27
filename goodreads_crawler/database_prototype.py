## Using SQLite to prototype the intended table structure in the final AWS RDS DB

#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import os
import sqlite3

#-----------------------------------------------------------------------------#
#                               PRE-DEFINES                                   #
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
#                            MODULE FUNCTIONS                                 #
#-----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#

if __name__ == "__main__":

    ## Load in pickled data
    



    ## Stop here to look at it lol
    pass


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
