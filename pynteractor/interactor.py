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


class Interactor:
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
        instance.before()

        try:
            instance.around()
        except (LogicError, StopExecution):
            pass

        instance.after()
        return instance.context

    def __init__(self, context=None):
        if context is None:
            context = Context

        self.context = context

    def before(self):
        """
        Hook to be called before run is called
        """

    def after(self):
        """
        Hook to be called after run is called
        """

    def around(self):
        """
        Hook to be called around run and must yield once and only once.

        Code is execute after the `before` method and before the `after` method
        """
        self.run()

    def run(self):
        """
        Implement the actual Business Logic.
        A context will alway be provided.
        """
        raise NotImplementedError()
