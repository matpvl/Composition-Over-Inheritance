# In The Decorator design pattern all of our loggers perform real output.
import logging
import sys
import re


class FileLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + "\n")
        self.file.flush()


class SocketLogger:
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


class SysLogger:
    def __init__(self, priority):
        self.priority = priority

    def log(self, message):
        logging.syslog(self.priority, message)


# The filtering code has been moved outside of any particular logger class.
# It's not a stand-alone feature that can be wrapper around any logger we want.


class LogFilter:
    def __init__(self, pattern, logger):
        self.pattern = pattern
        self.logger = logger

    def log(self, message):
        if re.search(self.pattern, message, re.IGNORECASE):
            self.logger.log(message)


log1 = FileLogger(sys.stdout)
log2 = LogFilter('Error', log1)

log1.log('Noisy: this logger always produces output')

log2.log('Ignored: this will be filtered out')
log2.log('Error: this is important and gets printed')

# We can now stack several different filters atop the same log.

log3 = LogFilter("Severe", log2)
log3.log("Error: this is ignored")
log3.log("Error: this is severe and cannot be ignored")
