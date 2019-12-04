import logging

import linecache
import sys
import traceback
from pjo.models import ExceptionLog

logger = logging.getLogger("devLog")
errLogger = logging.getLogger("errLog")


class PjoException(Exception):

    #  Constructor
    def __init__(self, **kwargs):

        # Exception origin info -> Exception Message Setting
        exc_type, exc_obj, exc_tb = sys.exc_info()
        self.tb = traceback.format_exception(exc_type, exc_obj, exc_tb)

        # Set Exception Values
        f = exc_tb.tb_frame
        self.lineno = exc_tb.tb_lineno
        self.filename = f.f_code.co_filename
        self.exception_class = exc_obj.__class__.__name__
        self.exception_msg = exc_obj
        linecache.checkcache(self.filename)
        line = linecache.getline(self.filename, self.lineno, f.f_globals)
        self.line = line.strip()

        # Custom Exception Message
        self.user_msg = kwargs.get('user_msg')
        if not self.user_msg:
            self.user_msg = ""

        # User Session Info
        self.user_id = kwargs.get('user_id')
        if not self.user_id:
            self.user_id = ""

        # Exception Message for User
        self.message = "[" + self.exception_class + "] " + self.user_msg

    def process(self):
        # Logging
        self.logging()
        # DB
        self.db_insert()

    def logging(self):
        errLogger.error('[{}] {}'.format(self.exception_class, self.exception_msg))
        str_log = ""
        for line in self.tb:
            str_log = str_log + line
        errLogger.error(str_log)

    def db_insert(self):

        try:
            # INSERT
            exception_log = ExceptionLog(exc_name=self.exception_class, exc_msg=self.exception_msg,
                                         filename=self.filename, line_no=self.lineno,
                                         line_string=self.line, reg_id=self.user_id)
            exception_log.save()

        except Exception as e:
            errLogger.error("[[[PjoException]]] ExceptionLog DB INSERT ERROR")
            errLogger.error(e)
            pass
