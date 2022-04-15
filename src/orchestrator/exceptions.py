class OrchestratorAuthException(Exception):
    def __init__(self, value, message):
        super().__init__(self, message)
        self.value = value

class OrchestratorFormatException(Exception):
    def __init__(self, value, message):
        super().__init__(self, message)
        self.value = value


class OrchestratorMissingParam(Exception):
    def __init__(self, value, message):
        super().__init__(self, message)
        self.value = value
