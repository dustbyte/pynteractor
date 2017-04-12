# -*- coding: utf-8 -*-

"""
Library errors
"""


class LogicError(ValueError):
    """
    Used to signal the current interactor has failed and that the execution of
    the running organizer should stop.
    """
    pass


class StopExecution(ValueError):
    """
    Is used to signal the execution of the current
    organizer is to be stopped.
    """
    pass
