# -*- coding: utf-8 -*-

import pytest


from pynteractor.errors import LogicError, StopExecution
from pynteractor.context import Context


@pytest.fixture
def ctx():
    return Context()

def test_context_defaults():
    ctx = Context()

    assert ctx.interrupted == False
    assert ctx.success == True
    assert ctx.failure == False

def test_context_given_values():
    ctx = Context(username='John Doe', age=42)

    assert ctx.interrupted == False
    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.username == 'John Doe'
    assert ctx.age == 42

def test_value_access(ctx):
    user_values = {'name': 'John Doe', 'age': 42}

    ctx.user = user_values
    ctx['is_admin'] = False

    assert ctx['user'] == user_values
    assert ctx.is_admin == False
    assert ctx.unroll() == {
        'success': True,
        'failure': False,
        'user': user_values,
        'is_admin': False,
        'interrupted': False
    }

def test_simple_termination(ctx):
    ctx.terminate()

    assert ctx.interrupted == True
    assert ctx.success == True
    assert ctx.failure == False

def test_terminate_args(ctx):
    ctx.terminate(reason='Not working')

    assert ctx.interrupted == True
    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.reason == 'Not working'

def test_terminate_failure(ctx):
    ctx.terminate(success=False)

    assert ctx.interrupted == True
    assert ctx.success == False
    assert ctx.failure == True

def test_terminate_failure_with_args(ctx):
    ctx.terminate(success=False, reason='Not working')

    assert ctx.interrupted == True
    assert ctx.success == False
    assert ctx.failure == True
    assert ctx.reason == 'Not working'

def test_fail_no_args(ctx):
    with pytest.raises(LogicError):
        ctx.fail()

    assert ctx.interrupted == True
    assert ctx.success == False
    assert ctx.failure == True

def test_fail_with_args(ctx):
    with pytest.raises(LogicError):
        ctx.fail(reason='Not working')

    assert ctx.interrupted == True
    assert ctx.success == False
    assert ctx.failure == True
    assert ctx.reason == 'Not working'

def test_stop_no_args(ctx):
    with pytest.raises(StopExecution):
        ctx.stop()

    assert ctx.interrupted == True
    assert ctx.success == True
    assert ctx.failure == False

def test_stop_with_args(ctx):
    with pytest.raises(StopExecution):
        ctx.stop(reason='Not working')

    assert ctx.interrupted == True
    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.reason == 'Not working'
