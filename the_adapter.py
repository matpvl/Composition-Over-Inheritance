# Solution #1, The Adapter.

# We keep the original Logger and FilteredLogger
# But instead of creating destination specific subclasses,
# we adapt each destination to the behavior of a file and then pass the adapter
# to a Logger as its output file.

# Python encourages duck-typing, If we need a duck to quack there is no reason
# for it to walk as well.

import sys
import logging
import socket
# import syslog

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)


class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()


class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)


class FileLikeSocket:
    def __init__(self, sock):
        self.sock = sock

    def write(self, message_and_newline):
        self.sock.sendall(message_and_newline.encode('ascii'))

    def flush(self):
        pass


class FileLikeSyslog:
    def __init__(self, priority):
        self.priority = priority

    def write(self, message_and_newline):
        message = message_and_newline.rstrip('\n')
        logging.syslog(self.priority, message)

    def flush(self):
        pass


sock1, sock2 = socket.socketpair()

fs = FileLikeSocket(sock1)
logger = FilteredLogger('Error', fs)
logger.log('Warning: message number one')
logger.log('Error: message number two')

print('The socket received: %r' % sock2.recv(512))

