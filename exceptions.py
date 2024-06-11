class GrizzlySmsError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message="An error occurred with Grizzly SMS"):
        self.message = message
        super().__init__(self.message)

class NoIdActivationError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: The activation ID does not exist.")

class BadActionError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: Incorrect action. (maybe it has already been completed?)")

class SqlError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: SQL server error.")

class BadServiceError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: Incorrect service name.")

class BadStatusError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: Incorrect status.")

class InvalidServiceCodeError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: Invalid service code.")

class InvalidCountryCodeError(GrizzlySmsError):
    def __init__(self):
        super().__init__("Grizzly sms: Invalid country code.")