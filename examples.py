from time import sleep
from random import randint

from timers import time_taken

# Adding this decorator will allow you to see how long this function takes to compute
@time_taken
def foo():
    """
    This function simulates a process which takes an unknown amount of time to compute
    like a function that saves some data about a game, for example.
    """
    seconds = randint(5, 10)
    sleep(seconds)


foo()





