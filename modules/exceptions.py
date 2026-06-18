class MaxRetryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ExpectedResultDoesNotMatchError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class AlreadyRespondedToListingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
