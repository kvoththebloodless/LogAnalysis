# !/usr/bin/env python3
# "Database code" for the DB Forum.

import psycopg2


def printResult(msg, query):
    '''
    Responsible for retrieving information from the database
    and sending it to be printed.
    :param msg: The description of the query results.
    :param query: The query to be executed.
    :return:
    '''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    analysis = cursor.fetchall()
    close(conn)
    printformatted(msg, analysis)


def connect():
    '''
    Responsible for establishing connection to the server.
    :return: connection instance.
    '''
    conn = psycopg2.connect(database="news")
    return conn


def close(conn):
    '''
    Closes the connection to the database.
    :param conn: Connection object to be closed.
    :return:
    '''
    conn.close()


def printformatted(msg, analysis):
    '''
    Responsible for formatting the message and the data.
    :param msg: The description of the query results.
    :param analysis: The data to be displayed in touple form.
    :return:
    '''
    print(msg)
    for row in analysis:
        print(row[0], '-', row[1])
    print()


QUERY1 = "Select title, views from view3 LIMIT 3;"

QUERY2 = "Select Authors.name, sum(view3.views) " \
         "from Authors LEFT JOIN view3 " \
         "on Authors.id=view3.author " \
         "group by Authors.name " \
         "ORDER BY sum DESC;"

QUERY3 = "Select * " \
         "from (select one.dayte,(count4 * 100/totalcount::float) as perc " \
         "from(Select dayte,count(status)as totalcount " \
         "from view4 group by dayte) as one " \
         "JOIN (Select dayte,count(status) as count4 from view4 " \
         "where status like '4%' group by dayte) " \
         "as two on one.dayte=two.dayte) as result " \
         "where perc>1;"

printResult("Most popular three articles of all time:\n", QUERY1)
printResult("Most popular article authors of all time:\n", QUERY2)
printResult("Days where more than 1% of requests lead to errors:\n", QUERY3)
