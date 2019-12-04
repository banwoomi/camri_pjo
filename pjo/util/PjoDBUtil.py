import logging
logger = logging.getLogger("devLog")


class DBUtil(object):

    # ==============================================================================
    #  Constructor
    # ==============================================================================
    def __init__(self):
        # do nothing
        pass

    # ==============================================================================
    #  Make list to dictionary
    # ==============================================================================
    @staticmethod
    def f_dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
