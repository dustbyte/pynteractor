# -*- coding: utf-8 -*-

"""
Small brick of Business Logic.  An interactor usually never goes over a simple
action.

Examples:
- Checks
- PersistData
- MarkAsDone
- Notify
"""

from pynteractor.errors import LogicError, StopExecution
from pynteractor.context import Context


class Interactor(object):
    """
    Smallest brick of Business Logic
    """

    @classmethod
    def call(klass, **kwargs):
        """
        Call the interactor with keywords arguments.

        Example:

        def MyInteractor(Interactor):
            pass

        MyInteractor.call(firstname='John', lastname='Doe')
        """
        return klass.call_with_context(Context(**kwargs))

    @classmethod
    def call_with_context(klass, context):
        """
        Call the current interactor with a given context of type
        pynteractor.Context.

        Mostly used internally to chain interactor calls.
        """
        instance = klass(context)

        try:
            instance.run()
        except StopExecution:
            pass
        except LogicError:
            klass.call_rollback(context)

        return context

    @classmethod
    def call_rollback(klass, context):
        instance = klass(context)
        try:
            instance.rollback()
        except AttributeError:
            pass
        return instance.context

    def __init__(self, context=None):
        if context is None:
            context = Context

        self.context = context

    def run(self):
        """
        Implement the actual Business Logic.
        A context will alway be provided.
        """
        raise NotImplementedError()
