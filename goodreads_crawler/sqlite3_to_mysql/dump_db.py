## NOTE: Instead of using this, use pure command line syntax:
## sqlite3 xxx.db .dump > yyy.sql
##      Where xxx = original file name, yyy = desired destination filename

## Super simple script to dump a sqlite3 file into a .sql file
## Used to import into AWS hosted server through mySQL workbench

# import sqlite3
# con = sqlite3.connect('bookhound_test1_index.db')
#
# f = open('bookhound_dump2.sql', 'w')
# for i,line in enumerate(con.iterdump()):
#     print(i)
#     f.write('%s\n' % line)
# f.close()


## Following script is from here:
## https://stackoverflow.com/questions/29012586/migrating-sqlite3-from-django-to-mysql-in-aws-rds-always-reporting-syntax-error

## In order to make this work, use the following command line syntax:
## sqlite3 bookhound_database_golden_copy.db .dump | python dump_db.py > dump.sql

import re
import fileinput

def this_line_is_useless(line):
    useless_es = [
        'BEGIN TRANSACTION',
        'COMMIT',
        'sqlite_sequence',
        'CREATE UNIQUE INDEX',
        'PRAGMA foreign_keys=OFF'
        ]
    for useless in useless_es:
        if re.search(useless, line):
                return True

def has_primary_key(line):
    return bool(re.search(r'PRIMARY KEY', line))

searching_for_end = False
for line in fileinput.input():
    if this_line_is_useless(line): continue

    # this line was necessary because ''); was getting
    # converted (inappropriately) to \');
    if re.match(r".*, ''\);", line):
        line = re.sub(r"''\);", r'``);', line)

    if re.match(r'^CREATE TABLE.*', line):
        searching_for_end = True

    m = re.search('CREATE TABLE "?([A-Za-z_]*)"?(.*)', line)
    if m:
        name, sub = m.groups()
        line = "DROP TABLE IF EXISTS %(name)s;\nCREATE TABLE IF NOT EXISTS `%(name)s`%(sub)s\n"
        line = line % dict(name=name, sub=sub)
    else:
        m = re.search('INSERT INTO "([A-Za-z_]*)"(.*)', line)
        if m:
                line = 'INSERT INTO %s%s\n' % m.groups()
                line = line.replace('"', r'\"')
                line = line.replace('"', "'")
    line = line.replace('AUTOINCREMENT','AUTO_INCREMENT')
    #line = line.replace('UNIQUE ','')
    line = line.replace('"','')
    line = re.sub(r"(?<!')'t'(?=.)", r"1", line)
    line = re.sub(r"(?<!')'f'(?=.)", r"0", line)

    # Add auto_increment if it's not there since sqlite auto_increments ALL
    # primary keys
    if searching_for_end:
        if re.search(r"integer(?:\s+\w+)*\s*PRIMARY KEY(?:\s+\w+)*\s*,", line):
            line = line.replace("PRIMARY KEY", "PRIMARY KEY AUTO_INCREMENT")
        # replace " and ' with ` because mysql doesn't like quotes in CREATE com                                                                             mands

    # And now we convert it back (see above)
    if re.match(r".*, ``\);", line):
        line = re.sub(r'``\);', r"'');", line)

    if searching_for_end and re.match(r'.*\);', line):
        searching_for_end = False

    if re.match(r"CREATE INDEX", line):
        line = re.sub('"', '`', line)

    print(line)