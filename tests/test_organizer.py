# -*- coding: utf-8 -*-

import pytest

from pynteractor.interactor import Interactor
from pynteractor.organizer import Organizer

def test_interactors_missing():
    with pytest.raises(TypeError):
        class Org1(Organizer):
            pass

def test_valid():
    class Int1(Interactor):
        def run(self):
            self.context.name = 'John Doe'


    class Int2(Interactor):
        def run(self):
            self.context.age = self.context.age + 1


    class Org1(Organizer):
        interactors = [Int1, Int2]

    ctx = Org1.call(age=41)

    assert ctx.interrupted == False
    assert ctx.success == True
    assert ctx.name == 'John Doe'
    assert ctx.age == 42

def test_stopped():
    class Int1(Interactor):
        def run(self):
            self.context.name = 'John Doe'
            self.context.stop(message='Condition met')


    class Int2(Interactor):
        def run(self):
            self.context.age = self.context.age + 1


    class Org1(Organizer):
        interactors = [Int1, Int2]


    ctx = Org1.call(age=41)

    assert ctx.interrupted == True
    assert ctx.success == True
    assert ctx.name == 'John Doe'
    assert ctx.message == 'Condition met'

def test_failed():
    class Int1(Interactor):
        def run(self):
            self.context.name = 'John Doe'
            self.context.fail(message='Condition not met')


    class Int2(Interactor):
        def run(self):
            self.context.age = self.context.age + 1


    class Org1(Organizer):
        interactors = [Int1, Int2]


    ctx = Org1.call(age=41)

    assert ctx.interrupted == True
    assert ctx.success == False
    assert ctx.name == 'John Doe'
    assert ctx.message == 'Condition not met'

def test_rollback():
    class Int1(Interactor):
        def run(self):
            pass

        def rollback(self):
            self.context.rollbacked.append('Int1')


    class Int2(Interactor):
        def run(self):
            self.context.fail(message='Condition not met')

        def rollback(self):
            self.context.rollbacked.append('Int2')


    class Org1(Organizer):
        interactors = [Int1, Int2]


    ctx = Org1.call(rollbacked=[])

    assert ctx.success == False
    assert ctx.rollbacked == ['Int2', 'Int1']

def test_premature_rollback():
    class Int1(Interactor):
        def run(self):
            self.context.fail(message='Condition not met')

        def rollback(self):
            self.context.rollbacked.append('Int1')


    class Int2(Interactor):
        def run(self):
            pass

        def rollback(self):
            self.context.rollbacked.append('Int2')


    class Org1(Organizer):
        interactors = [Int1, Int2]


    ctx = Org1.call(rollbacked=[])

    assert ctx.success == False
    assert ctx.rollbacked == ['Int1']

def test_premature_no_rollback():
    class Int1(Interactor):
        def run(self):
            self.context.fail(message='Condition not met')

    class Int2(Interactor):
        def run(self):
            pass

        def rollback(self):
            self.context.rollbacked.append('Int2')


    class Org1(Organizer):
        interactors = [Int1, Int2]


    ctx = Org1.call(rollbacked=[])

    assert ctx.success == False
    assert ctx.rollbacked == []
