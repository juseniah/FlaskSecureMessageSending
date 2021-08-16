"""
Name: Jussi Doherty
Date: March 19, 2021
Assignment: Module 11 - Using Threads
Due Date: March 21, 2021
About this project: Notify if any new messages about X are sent
Assumptions: N/A
All work below was performed by Jussi Doherty
"""

from multiprocessing import Process
import sqlite3 as sql
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time


# Function to count number of messages containing x
def FindX(x: str):
    count = 0
    # connects to special agent database and runs sql query
    with sql.connect("sagent.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        sql_select_query = """select count(*) as NumMsgs from Messages where Message like ? """
        cur.execute(sql_select_query, ("%" + x + "%",))
        row = cur.fetchone();
        CurrNum = int(row[0])
    con.close()
    return CurrNum


def main():
    # get current number of messages with cat and dog
    numCatMsgs = FindX("cat")
    numDogMsgs = FindX("dog")

    # Use ThreadPoolExecutor to manage threads
    while True:
        # Submit 2 tasks to the executor
        with ThreadPoolExecutor(max_workers=2) as executor:
            taskNumCatMsgs = executor.submit(FindX, ("cat"))
            taskNumDogMsgs = executor.submit(FindX, ("dog"))

        # Update numCatMsgs if it's changed
        if taskNumCatMsgs.result() != numCatMsgs:
            numCatMsgs = taskNumCatMsgs.result()
            print("Now there are " + str(numCatMsgs) + " messages with cat")

        # Update numDogMsgs if it's changed
        if taskNumDogMsgs.result() != numDogMsgs:
            numDogMsgs = taskNumDogMsgs.result()
            print("Now there are " + str(numDogMsgs) + " messages with dog")

        # Run every 4 seconds instead of constantly
        time.sleep(4)

if __name__ == '__main__':
    main()
