from interpreter import *

class RinhaError(Exception):
    def __init__(self, message):
        super().__init__(message)
