"""pyCasJobs module.

This module provides a class for accessing the SDSS CasJobs server in
a programmatic manner.

Now discovered the method used (pretending to be a real user, storing
cookies) is unnecessary as CasJobs provides an API.
E.g., see http://casjobs.sdss.org/CasJobs/services/jobs.asmx?op=UploadData

Example usage:
>>> import pyCasJobs
>>> cas = pyCasJobs.CasJobs('username', 'password')
>>> cas.import_table('mytable.csv', 'mytable')

The current functionality is limited only to importing tables.
However, it should be straightforward to implement the additional elements of CasJobs,
such as SQL queries, in a similar manner.

Requires a non-standard library module: poster, see http://atlee.ca/software/poster/.

Created on Jul 15, 2010

@author: Steven Bamford
"""

import urllib2, urllib, cookielib

class CasJobs:
    """Programmatic access to the SDSS CasJobs server.
    
    A class which enables programmatic access to the Sloan Digital Sky Survey
    CasJobs server, by wrapping the usual browser-based web interface.

    Keyword arguments to constructor:
    username -- CasJobs username
    password -- CasJobs password

    """    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.result = None
        self.apiurl = 'http://casjobs.sdss.org/CasJobs/services/jobs.asmx/'

    def quick_query(self, query, context='MYDB', name='Quick query from pyCasJobs'):
        """Execute a synchonous quick query on CasJobs.

        Keyword arguments:
        query -- Query to run
        context -- Context of job, e.g. MYDB
        name -- Optional identifier of job
        
        """
        data = urllib.urlencode({'wsid': self.username, 'pw': self.password, 'qry': query,
                                 'context': context, 'taskname': name,
                                 'isSystem': 'false'})
        response = urllib2.urlopen(self.apiurl+'ExecuteQuickJob', data)
        self.result = response.read()
        response.close()
        
    def import_table(self, filename, tablename, tableexists=False):
        """Upload a local CSV file into CasJobs MyDB.
    
        Note that CasJobs has rather stringent limits to the size of file
        which can be uploaded.

        Keyword arguments:
        filename -- filename of the table to upload
        tablename -- name of the table to create/append to in CasJobs MyDB
        tableexists -- if 'False' create a new table, if 'True' append to existing table

        """
        table = ''.join(open(filename, 'r').readlines())
        data = urllib.urlencode({'wsid': self.username, 'pw': self.password,
                                 'tableName': tablename, 'data': table,
                                 'tableExists': tableexists})
        response = urllib2.urlopen(self.apiurl+'UploadData', data)
        self.result = response.read()
        response.close()


if __name__ == '__main__':
    pass
