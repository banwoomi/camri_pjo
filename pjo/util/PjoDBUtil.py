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
    def f_dict_fetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # ==============================================================================
    #  Make list to dictionary
    # ==============================================================================
    @staticmethod
    def f_dict_fetchone(cursor):

        columns = [col[0] for col in cursor.description]
        tuple_result = cursor.fetchone()

        if tuple_result:
            return dict(zip(columns, tuple_result))
        else:
            return None


