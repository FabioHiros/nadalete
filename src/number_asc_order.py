from src.custom_stack_class import CustomStack


class NumberAscOrder:
    """Collects the numbers drawn in a Mega Sena contest from a CustomStack and sorts them."""

    DRAWN_NUMBERS = 6
    MIN_NUMBER = 1
    MAX_NUMBER = 60

    def sort(self, stack):
        """Returns the drawn numbers as a list in ascending order.

        The stack is read only through its public methods and is left as it was.

        Raises:
            TypeError: if `stack` is not a CustomStack.
            ValueError: if the stack is empty or does not hold exactly 6 distinct
                integers between 1 and 60.
        """
        if not isinstance(stack, CustomStack):
            raise TypeError("sort() espera uma CustomStack")

        numbers = self._collect(stack)
        self._validate(numbers)
        return sorted(numbers)

    @staticmethod
    def _collect(stack):
        popped = []
        try:
            while not stack.is_empty():
                popped.append(stack.pop())
        finally:
            # put the numbers back in the original order, even if a pop failed midway
            for number in reversed(popped):
                stack.push(number)
        return popped

    def _validate(self, numbers):
        if not numbers:
            raise ValueError("A pilha de números sorteados está vazia")
        if len(numbers) != self.DRAWN_NUMBERS:
            raise ValueError(
                f"A pilha deve conter exatamente {self.DRAWN_NUMBERS} números sorteados"
            )
        if any(type(number) is not int for number in numbers):
            raise ValueError("Os números sorteados devem ser inteiros")
        if any(not self.MIN_NUMBER <= number <= self.MAX_NUMBER for number in numbers):
            raise ValueError(
                f"Os números sorteados devem estar entre {self.MIN_NUMBER} e {self.MAX_NUMBER}"
            )
        if len(set(numbers)) != len(numbers):
            raise ValueError("Os números sorteados não podem ser repetidos")
