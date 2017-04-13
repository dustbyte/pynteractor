# -*- coding: utf-8 -*-

import pytest

from pynteractor.context import Context
from pynteractor.interactor import Interactor


def test_not_implemented():
    with pytest.raises(NotImplementedError):
        Interactor().call()

def test_call_with_context():
    class Impl(Interactor):
        def run(self):
            self.context.age = 42

    ctx = Impl.call_with_context(Context(name='John Doe'))

    assert ctx.success == True
    assert ctx.age == 42
    assert ctx.name == 'John Doe'

def test_call_without_context():
    class Impl(Interactor):
        def run(self):
            self.context.age = 42

    ctx = Impl.call(name='John Doe')

    assert ctx.success == True
    assert ctx.age == 42
    assert ctx.name == 'John Doe'

def test_before_hook():
    class Impl(Interactor):
        def before(self):
            self.context.age = 41

        def run(self):
            self.context.age = self.context.age + 1

    ctx = Impl.call()

    assert ctx.success == True
    assert ctx.age == 42

def test_after_hook():
    class Impl(Interactor):
        def run(self):
            self.context.age = 41

        def after(self):
            self.context.age = self.context.age + 1


    ctx = Impl.call()

    assert ctx.success == True
    assert ctx.age == 42

def test_around_hook():
    class Impl(Interactor):
        def around(self):
            self.context.age = 40
            self.run()
            self.context.age = self.context.age + 1

        def run(self):
            self.context.age = self.context.age + 1

    ctx = Impl.call()

    assert ctx.success == True
    assert ctx.age == 42
