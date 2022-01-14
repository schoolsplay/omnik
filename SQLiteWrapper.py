# Copyright (c) 2011-2013 Stas Zykiewicz <stas@childsplay.mobi>
#
#               SQLiteWrapper.py


__author__ = 'stas Zytkiewicz stas@childsplay.mobi'

# Only needed if you want to test the wrapper class standalone
# import sys, os
# sys.path.insert(0, os.getcwd())

import sqlite3

import logging


class DBW:
    """Very simple wrapper around some common python sqlite commands.
    At this point you can create a dbase, connect to it, define tables, query and insert."""

    def __init__(self, dbname='db.sqlite'):
        self.logger = logging.getLogger('sp.SQLiteWrapper.DBW')
        self.logger.debug("using dbase %s" % dbname)
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname, detect_types=sqlite3.PARSE_DECLTYPES)
        self.c = self.conn.cursor()

    def get_cursor(self):
        """Returns a cursor object in case you want to do stuff"""
        return self.c

    def get_dict_cursor(self):
        """Returns a cursor object from a connection that uses the row_factory.
        This means that a fetch_all will return a list with dictionaries"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        return conn.cursor()

    def truncate(self, tname):
        """truncate by deleting all rows"""
        result = True
        try:
            self.c.execute('''DELETE FROM %s ''' % tname)
        except sqlite3.OperationalError as e:
            self.logger.warning("No table found: %s" % e)
            result = False
        try:
            self.c.execute('''DELETE FROM sqlite_sequence WHERE name = '%s';''' % tname)
        except sqlite3.OperationalError as e:
            # self.logger.info("No table found: %s" % e)
            # result = False
            pass
        self.commit()
        return result

    def define_table(self, tname, collist, uniquelist=[]):
        """define a table with 'name' and the column names and types must be in 'collist'.
        For example collist could be something like: [('id','integer',['PRIMARY KEY], ('name','text')]
        where a tuple consists of name, type pairs.
        Possible types are all supported python datatypes like 'real' 'integer' and 'text'.
        Special reminder that to use a datetime object you must use datatype 'timestamp'.
        The tuples can have additional item, which must be a list, to set restrains
         like UNIQUE, PRIMARY KEY etc.
        """
        l = []
        for items in collist:
            if len(items) == 2:
                l.append("%s %s" % items)
            else:
                s = "%s %s" % (items[0], items[1])
                for item in items[2]:
                    s += " " + item
                l.append(s)
        for item in uniquelist:
            l.append(item)
        s = '(%s)' % ",".join(l)
        #print s
        self.c.execute('''CREATE TABLE IF NOT EXISTS %s %s''' % (tname, s))

    def delete_row(self, tname, col, pattern):
        self.logger.debug("remove row: %s %s %s" % (tname, col, pattern))
        self.c.execute('''DELETE FROM %s WHERE "%s" = ?''' % (tname, col), (pattern,))
        self.commit()

    def add_row(self, tname, vallist, commit=True):
        """Insert a row with values into table 'tname'.
        vallist must be in the same sequence as the table cols"""
        s = 'INSERT INTO {0:s} values'.format(tname)
        qs = ['?'] * len(vallist)
        qs = ",".join(qs)

        try:
            self.c.execute('''%s (%s)''' % (s, qs), vallist)
        except Exception as e:
            self.logger.error("Failed to add row: %s" % e)
            # print '''%s (%s)''' % (s, qs)
            # print "vallist", vallist
            return {'mesg': "Failed to add row, rollback: %s" % e, 'id': None}
        else:
            if commit:
                self.commit()
            return {'mesg': "ok", 'id': self.c.lastrowid}

    def insert_or_replace(self, tname, vallist):
        """Insert a row with values into table 'tname'.
        When the row exists it will be replaced with the new values.
        vallist must be in the same sequence as the table cols"""
        s = 'REPLACE INTO {0:s} values'.format(tname)
        qs = ['?'] * len(vallist)
        qs = ",".join(qs)
        self.c.execute('''%s (%s)''' % (s, qs), vallist)
        self.commit()

    def update_row(self, tname, col, val, valtuple):
        """Update table tname col with val.
        valtuple must be a tuple with col, val pairs.
        For example :
        contact_update_row = ('id', row[0],
                              'name_first', row[1],
                              'name_middle', row[2],
                              .....
                              )
        The sqlite command ceated is :
        UPDATE table_name
        SET column1=value, column2=value2,...
        WHERE some_column=some_value
        UPDATE tname SET newvals where col == val
        If the col == val not found returns False
        """
        i = len(valtuple) / 2
        if i == 0:
            i = 1
        qs = ['%s = "%s"'] * i
        qs = ",".join(qs)
        s0 = 'UPDATE %s SET' % tname
        s1 = ' %s WHERE ' % qs
        s2 = '%s="%s"' % (col, val)
        s1 = s1 % valtuple
        #print s0 + s1 + s2
        self.c.execute(s0 + s1 + s2)
        self.commit()

    def select(self, tname, col, val):
        """Very, very simple select.
        It just does 'SELECT * FROM tname WHERE col = val'.
        Use get_cursor to get a cursor object if you want to do serious selects
        """
        #        try:
        #            print tname, col, val
        #        except UnicodeEncodeError:
        #            pass
        s = 'SELECT * FROM {0:s} WHERE {1:s} = ?'.format(tname, col)
        # print s, val
        self.c.execute(s, (val,))
        return self.c.fetchall()

    def select_all(self, tname):
        """Simple select.
        It just does 'SELECT * FROM tname.
        """
        s = 'SELECT * FROM {0:s}'.format(tname)
        # print s, val
        self.c.execute(s)
        return self.c.fetchall()

    def commit(self):
        """Must always be called to store stuff into dbase"""
        try:
            self.conn.commit()
        except sqlite3.Error as info:
            self.logger.error("Failed to commit dabse, rollback: %s" % info)
            self.conn.rollback()
            return {'mesg': "Failed to commit dbase, rollback: %s" % info, 'id': None}
        else:
            #self.logger.debug("commited changes to dbase")
            return {'mesg': 'ok', 'id': None}

    def close(self):
        self.commit()
        self.c.close()

    def stop(self):
        self.logger.info("Stopping dbase")
        try:
            self.close()
        except:
            pass

    def select_dbase(self, tname, col, val):
        ret = self.select(tname, col, val)
        return ret
