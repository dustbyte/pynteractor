# -*- coding: utf-8 -*-

"""
Implement the context helper to help share variables with the outside of the
organizer, but also within the organizer itself.
"""

from pynteractor.errors import LogicError, StopExecution


class Context:
    """
    Organizer data bank and termination decider.
    """

    def __init__(self, **kwargs):
        super(Context, self).__setattr__('_inner', kwargs)
        self.set_success(True)

    def set_success(self, value):
        """
        Set the outcoming results
        """
        self._inner['success'] = value
        self._inner['failure'] = not value

    def __getattr__(self, attr):
        return self._inner.get(attr, None)

    def __setattr__(self, attr, value):
        self._inner[attr] = value

    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        return setattr(self, attr, value)

    def unroll(self):
        """
        Expose the whole set of context-related attributes
        """
        return self._inner

    def terminate(self, success=True, **kwargs):
        """
        Stop running the current interactor and organizer and populate the
        current context with passed arguments.
        """
        for arg, value in kwargs.items():
            self._inner[arg] = value

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
