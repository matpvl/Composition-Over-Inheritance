# Problem: the subclass explosion
# ie. we want to filter a socker, then we must create a FilteredSocketLogger,
# a FilteredSyslogLogger and so on. The total number of classes will increase
# Geometrically if m and n both continue to grow.
# This is the subclass explosion the gang of four wants to avoid.

import sys
import logging
# import syslog


class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()


class SocketLogger(Logger):
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + '\n').encode('ascii'))


class SyslogLogger(Logger):
    def __init__(self, priority):
        self.priority = priority

    def log(self, message):
        logging.syslog(self.priority, message)


class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)


f = FilteredLogger('Error', sys.stdout)
f.log('Ignored: this is not important')
f.log('Error: but you want to see this')
