import pytest

from src.custom_stack_class import *

def test_push_one_elementinstack():
    element_value = 5.0
    value = 0.0

    cut = CustomStack(5)
    cut.push(element_value)
    assert cut.is_empty() == False
    assert element_value == cut.top()
    assert 1 == cut.size()

def test_new_stack_is_empty_and_has_the_given_limit():
    cut = CustomStack(3)

    assert cut.is_empty() is True
    assert cut.size() == 0
    assert cut.limit == 3


def test_push_keeps_the_order_and_top_is_the_last_pushed_element():
    cut = CustomStack(5)

    cut.push(1)
    cut.push(2)
    cut.push(3)

    assert cut.size() == 3
    assert cut.top() == 3


def test_top_does_not_remove_the_element():
    cut = CustomStack(5)
    cut.push(7)

    assert cut.top() == 7
    assert cut.top() == 7
    assert cut.size() == 1


def test_pop_returns_elements_in_lifo_order_and_removes_them():
    cut = CustomStack(5)
    for element in (1, 2, 3):
        cut.push(element)

    assert cut.pop() == 3
    assert cut.size() == 2
    assert cut.pop() == 2
    assert cut.pop() == 1
    assert cut.is_empty() is True


def test_pop_on_empty_stack_raises_stack_empty_exception():
    cut = CustomStack(5)

    with pytest.raises(StackEmptyException):
        cut.pop()


def test_pop_on_stack_emptied_by_pops_raises_stack_empty_exception():
    cut = CustomStack(5)
    cut.push(1)
    cut.pop()

    with pytest.raises(StackEmptyException):
        cut.pop()


def test_top_on_empty_stack_raises_stack_empty_exception():
    cut = CustomStack(5)

    with pytest.raises(StackEmptyException):
        cut.top()


def test_push_up_to_the_limit_is_allowed():
    cut = CustomStack(3)

    for element in (1, 2, 3):
        cut.push(element)

    assert cut.size() == 3
    assert cut.top() == 3


def test_push_on_full_stack_raises_stack_full_exception_and_keeps_the_elements():
    cut = CustomStack(2)
    cut.push(1)
    cut.push(2)

    with pytest.raises(StackFullException):
        cut.push(3)

    assert cut.size() == 2
    assert cut.top() == 2


def test_stack_with_zero_limit_is_always_full():
    cut = CustomStack(0)

    with pytest.raises(StackFullException):
        cut.push(1)

    assert cut.is_empty() is True


def test_pop_frees_space_for_a_new_push_on_a_full_stack():
    cut = CustomStack(1)
    cut.push(1)
    cut.pop()

    cut.push(2)

    assert cut.top() == 2


def test_stack_exceptions_are_exceptions():
    assert issubclass(StackEmptyException, Exception)
    assert issubclass(StackFullException, Exception)
