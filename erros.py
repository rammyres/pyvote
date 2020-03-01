class Erros(Exception):

    pass

class hashAnteriorInvalido(Erros):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, message):
        self.message = message