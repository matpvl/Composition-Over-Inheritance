# Say we want more flexibility, to support multiple filters and
# multiple outputs for a single stream of log messages.

# 1. The Logger class that callers interact with doesn't itself implement
# either filtering or output. Instead, it maintains a list of filters
# and a list of handlers.

# 2. For each log message, the logger calls each of its filters.
# The message is discarded if any filter rejects it.

# 3. For each log message that's accepted by all the filters, the logger
# loops over its output handlers and asks every one of them to
# emit() the message.

import logging
import sys


# We now have only one logger.

class Logger:
    def __init__(self, filters, handlers):
        self.filters = filters
        self.handlers = handlers

    def log(self, message):
        if all(f.match(message) for f in self.filters):
            for h in self.handlers:
                h.emit(message)


# Filters now know only about strings.

class TextFilter:
    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, text):
        return self.pattern in text


# Handlers

class FileHandler:
    def __init__(self, file):
        self.file = file

    def emit(self, message):
        self.file.write(message + "\n")
        self.file.flush()


class SocketHandler:
    def __init__(self, sock):
        self.sock = sock

    def emit(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


class SyslogHandler:
    def __init__(self, priority):
        self.priority = priority

    def emit(self, message):
        logging.syslog(self.priority, message)


f = TextFilter("Error")
h = FileHandler(sys.stdout)
logger = Logger([f], [h])

logger.log("Ignored: this will not be logged.")
logger.log("Error: this is mui importante.")
