import random

import pytest

from src.custom_stack_class import CustomStack, StackEmptyException
from src.number_asc_order import NumberAscOrder


def drawn_numbers(seed):
    """Six distinct Mega Sena numbers, in draw order."""
    return random.Random(seed).sample(range(1, 61), 6)


def mock_stack(mocker, elements):
    """CustomStack mock that behaves like a stack holding `elements` (last one on top)."""
    remaining = list(elements)
    stack = mocker.Mock(spec=CustomStack)
    stack.is_empty.side_effect = lambda: not remaining
    stack.pop.side_effect = lambda: remaining.pop()
    stack.push.side_effect = remaining.append
    stack.remaining = remaining
    return stack


def real_stack(elements, limit=6):
    stack = CustomStack(limit)
    for element in elements:
        stack.push(element)
    return stack


@pytest.fixture
def cut():
    return NumberAscOrder()


# Scenario 1: stack of 6 positions with the 6 drawn numbers


@pytest.mark.parametrize("seed", range(10))
def test_sort_returns_the_six_random_numbers_in_ascending_order(cut, mocker, seed):
    drawn = drawn_numbers(seed)
    stack = mock_stack(mocker, drawn)

    result = cut.sort(stack)

    assert result == sorted(drawn)
    assert isinstance(result, list)


def test_sort_reads_the_stack_only_through_its_public_methods(cut, mocker):
    stack = mock_stack(mocker, [33, 5, 60, 1, 17, 42])

    cut.sort(stack)

    assert stack.pop.call_count == 6


def test_sort_leaves_the_stack_as_it_was_before_the_call(cut, mocker):
    drawn = [33, 5, 60, 1, 17, 42]
    stack = mock_stack(mocker, drawn)

    cut.sort(stack)

    assert stack.remaining == drawn
    assert stack.push.call_args_list == [mocker.call(n) for n in drawn]


@pytest.mark.parametrize("seed", range(10))
def test_sort_with_a_real_stack_returns_ascending_numbers_and_keeps_the_stack(cut, seed):
    drawn = drawn_numbers(seed)
    stack = real_stack(drawn)

    result = cut.sort(stack)

    assert result == sorted(drawn)
    assert stack.size() == 6
    assert stack.top() == drawn[-1]
    assert [stack.pop() for _ in range(6)] == drawn[::-1]


@pytest.mark.parametrize(
    "drawn",
    [[1, 2, 3, 4, 5, 6], [60, 59, 58, 57, 56, 55], [1, 60, 2, 59, 3, 58]],
    ids=["already ascending", "descending", "alternating"],
)
def test_sort_handles_any_initial_order(cut, mocker, drawn):
    assert cut.sort(mock_stack(mocker, drawn)) == sorted(drawn)


def test_sort_returns_a_new_list_that_is_not_tied_to_the_stack(cut):
    stack = real_stack([6, 5, 4, 3, 2, 1])

    result = cut.sort(stack)
    result.append(99)

    assert stack.size() == 6


# Scenario 2: empty stack of 6 positions


def test_sort_of_an_empty_mock_stack_raises_value_error_without_popping(cut, mocker):
    stack = mock_stack(mocker, [])

    with pytest.raises(ValueError, match="vazia"):
        cut.sort(stack)

    stack.pop.assert_not_called()
    stack.push.assert_not_called()


def test_sort_of_an_empty_real_stack_raises_value_error(cut):
    with pytest.raises(ValueError, match="vazia"):
        cut.sort(CustomStack(6))


# Checks on the argument and on the drawn numbers


@pytest.mark.parametrize("not_a_stack", [None, [1, 2, 3, 4, 5, 6], "123456", 7, {1, 2}])
def test_sort_rejects_an_argument_that_is_not_a_custom_stack(cut, not_a_stack):
    with pytest.raises(TypeError):
        cut.sort(not_a_stack)


@pytest.mark.parametrize("quantity", [1, 5, 7])
def test_sort_rejects_a_stack_without_exactly_six_numbers(cut, mocker, quantity):
    drawn = list(range(1, quantity + 1))
    stack = mock_stack(mocker, drawn)

    with pytest.raises(ValueError, match="6 números"):
        cut.sort(stack)

    assert stack.remaining == drawn


@pytest.mark.parametrize("out_of_range", [0, -1, 61, 100])
def test_sort_rejects_numbers_outside_1_to_60(cut, mocker, out_of_range):
    drawn = [1, 2, 3, 4, 5, out_of_range]
    stack = mock_stack(mocker, drawn)

    with pytest.raises(ValueError, match="entre 1 e 60"):
        cut.sort(stack)

    assert stack.remaining == drawn


@pytest.mark.parametrize("not_an_int", [5.0, "7", None, True])
def test_sort_rejects_numbers_that_are_not_integers(cut, mocker, not_an_int):
    drawn = [1, 2, 3, 4, 8, not_an_int]
    stack = mock_stack(mocker, drawn)

    with pytest.raises(ValueError, match="inteiros"):
        cut.sort(stack)

    assert stack.remaining == drawn


def test_sort_rejects_repeated_numbers(cut, mocker):
    drawn = [10, 20, 30, 40, 50, 10]
    stack = mock_stack(mocker, drawn)

    with pytest.raises(ValueError, match="repetidos"):
        cut.sort(stack)

    assert stack.remaining == drawn


def test_sort_puts_the_numbers_back_even_if_the_stack_fails_midway(cut, mocker):
    stack = mock_stack(mocker, [10, 20, 30, 40, 50, 60])
    original_pop = stack.pop.side_effect
    calls = {"count": 0}

    def failing_pop():
        calls["count"] += 1
        if calls["count"] == 4:
            raise StackEmptyException
        return original_pop()

    stack.pop.side_effect = failing_pop

    with pytest.raises(StackEmptyException):
        cut.sort(stack)

    assert stack.remaining == [10, 20, 30, 40, 50, 60]
