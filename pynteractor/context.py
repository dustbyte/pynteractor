# -*- coding: utf-8 -*-

"""
Implement the context helper to help share variables with the outside of the
organizer, but also within the organizer itself.
"""

from pynteractor.errors import LogicError, StopExecution


class Context(object):
    """
    Organizer data bank and termination decider.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

        self.interrupted = False
        self.set_success(True)

    def set_success(self, value):
        """
        Set the outcoming results
        """
        self.success = value
        self.failure = not value

    def __getattr__(self, attr):
        return self.__dict__.get(attr, None)

    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        return setattr(self, attr, value)

    def unroll(self):
        """
        Expose the whole set of context-related attributes
        """
        return self.__dict__

    def terminate(self, success=True, **kwargs):
        """
        Stop running the current interactor and organizer and populate the
        current context with passed arguments.
        """
        for arg, value in kwargs.items():
            self[arg] = value

        self.interrupted = True
        self.set_success(success)

    def fail(self, **kwargs):
        """
        Stop running the current organizer but raise an error to signal
        something went wrong.
        """
        self.terminate(success=False, **kwargs)
        raise LogicError()

    def stop(self, **kwargs):
        """
        Stop running the current organizer but raise an error to signal the
        user just wants to terminate the current organizer/interactor execution.
        """
        self.terminate(success=True, **kwargs)
        raise StopExecution()
