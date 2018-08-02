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

def test_rollback_not_called():
    class Impl(Interactor):
        def run(self):
            self.context.rollbacked = False

        def rollback(self):
            self.context.rollbacked = True

    ctx = Impl.call()

    assert ctx.success == True
    assert ctx.rollbacked == False

def test_rollback_called():
    class Impl(Interactor):
        def run(self):
            self.context.fail(message="I want to rollback")

        def rollback(self):
            self.context.rollbacked = True

    ctx = Impl.call()

    assert ctx.success == False
    assert ctx.rollbacked == True


def test_ctx_alias():
    class Impl(Interactor):
        def run(self):
            self.ctx.my_val = 42
            self.ctx.my_other_val = 21

    ctx = Impl.call()

    assert ctx.my_val == 42
    assert ctx.my_other_val == 21
