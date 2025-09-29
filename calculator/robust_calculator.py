import re

class RobustCalculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None

        tokens = self.tokenize(expression)
        return self._evaluate_infix(tokens)

    def tokenize(self, expression):
        # Use regex to handle expressions without spaces
        return re.findall(r"(\d+(?:\.\d+)?|[\+\-\*/])", expression)


    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:

                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"Not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        try:
            values.append(self.operators[operator](a, b))
        except ZeroDivisionError:
            raise ValueError("Division by zero")
