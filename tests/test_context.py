# -*- coding: utf-8 -*-

import pytest

from pynteractor.context import Context, LogicError, StopExecution


def test_context_defaults():
    ctx = Context()
    assert ctx.success == True
    assert ctx.failure == False

def test_context_given_values():
    ctx = Context(username='John Doe', age=42)

    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.username == 'John Doe'
    assert ctx.age == 42

def test_value_access():
    user_values = {'name': 'John Doe', 'age': 42}

    ctx = Context()
    ctx.user = user_values
    ctx['is_admin'] = False

    assert ctx['user'] == user_values
    assert ctx.is_admin == False
    assert ctx.unroll() == {
        'success': True,
        'failure': False,
        'user': user_values,
        'is_admin': False
    }

def test_simple_termination():
    ctx = Context()

    ctx.terminate()

    assert ctx.success == True
    assert ctx.failure == False

def test_terminate_args():
    ctx = Context()

    ctx.terminate(reason='Not working')

    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.reason == 'Not working'

def test_terminate_failure():
    ctx = Context()

    ctx.terminate(success=False)

    assert ctx.success == False
    assert ctx.failure == True

def test_terminate_failure_with_args():
    ctx = Context()

    ctx.terminate(success=False, reason='Not working')

    assert ctx.success == False
    assert ctx.failure == True
    assert ctx.reason == 'Not working'

def test_fail_no_args():
    ctx = Context()

    with pytest.raises(LogicError):
        ctx.fail()

    assert ctx.success == False
    assert ctx.failure == True

def test_fail_with_args():
    ctx = Context()

    with pytest.raises(LogicError):
        ctx.fail(reason='Not working')

    assert ctx.success == False
    assert ctx.failure == True
    assert ctx.reason == 'Not working'

def test_stop_no_args():
    ctx = Context()

    with pytest.raises(StopExecution):
        ctx.stop()

    assert ctx.success == True
    assert ctx.failure == False

def test_stop_with_args():
    ctx = Context()

    with pytest.raises(StopExecution):
        ctx.stop(reason='Not working')

    assert ctx.success == True
    assert ctx.failure == False
    assert ctx.reason == 'Not working'
