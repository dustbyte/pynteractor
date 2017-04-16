# -*- coding: utf-8 -*-

"""
Master interactor that keeps a list of other interactors in order and loops
through them.

This is generally the global action, called by views/controllers.

Examples:
- CreateEntity
- LoginUser
- UpdatePassword
"""

from six import with_metaclass
from collections import Iterable

from pynteractor import Interactor


class OrganizerMeta(type):
    """
    Metaclass around organizers, ensures that the static attribute
    `interactors` of a class inheritting from Organizer is present.
    """

    def __init__(cls, name, bases, attrs):
        if name != 'Organizer' and 'interactors' not in attrs:
                raise TypeError('Organizer requires a list of interactors.')

        super(OrganizerMeta, cls).__init__(name, bases, attrs)


class Organizer(with_metaclass(OrganizerMeta, Interactor)):
    """
    Organize interactors.

    Works like an Interactor with two differences:
    - An `interactors` static attribute must be provided with a list of
      interactors in the desired execution order.
    - The `run` method is already implemented to answer the Organizer logic and
      should not be overridden.

    Example usage

    class UpdateUser(Organizer):
        interactors = [
            EnsureUserIsActive,
            UpdateUserAttributes,
            RegisterEvent,
        ]

        def before():
            self.context.user = User.objects.get(pk=self.context.user_id)
    [...]
    result = UpdateUser.call(user_id=form['user_id'])
    """

    def run(self):
        called = []
        for interactor in self.interactors:
            self.context = interactor.call_with_context(self.context)
            if self.context.interrupted:
                break
            called.append(interactor)

        if not self.context.success:
            for interactor in reversed(called):
                interactor.call_rollback(self.context)
