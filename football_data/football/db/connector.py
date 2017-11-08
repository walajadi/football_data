# -*- coding: utf-8 -*-
import psycopg2
import sys


class DBConnection(object):

    def __init__(self):

        self.conn = None

    def set_conn(self, dbname='testdb', user='user_1'):
        """
            connect to the given db, testdb if not available.

        """
        try:
            self.con = psycopg2.connect(dbname=dbname, user=user_1)
            return self.con.cursor()
        except psycopg2.DatabaseError as e:
            print('Error occured at Connection : {}'.format(e))

        return None
