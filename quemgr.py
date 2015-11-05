#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading
import time


class QueMgr:

    def __init__(self, db):
        """
        The queue manager class, tends to solve the cocurrency problem,
        when writing to the sqlite database. It happens when two or more
        threads of a python application start to write to the sqlite files.
        It gives the locked error.
        here there is a thread runing that checks the database queue for items
        and commands needed to added to the database.
        """
        self.db = db
        self.queue = Queue.Queue()

    def insert(self, item, insert_type):
        """
        Insert to the database, given item with given function.
        Take a look at the database.py, there are two functions that write
        in the database. So these are chosen.

        Args:
                item (dict or list)
                insert_type string

        Kwargs:
                None

        Returns:
                None
        """
        if(insert_type == "initState"):
            self.db.update_all(item)
        if(insert_type == "finalState"):
            self.db.insert_final_state(item)


class QueMgrThread(threading.Thread):

    def __init__(self, quemgr):
        threading.Thread.__init__(self)
        self.quemgr = quemgr

    def run(self):
        while(True):
            if(self.quemgr.queue.empty()):
                print "empty"
            else:
                print "hi"
                self.quemgr.insert(item["item"], item["type"])
                q.task_done()
            time.sleep(5)
