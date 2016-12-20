class RoomFullError(Exception):
    pass


class InvalidRoomOccupantError(Exception):
    pass


class MultiplePeopleFoundException(Exception):
    pass


class AmbiguityException(Exception):
    """
    This exception is raised to indicate a case of ambiguity when interacting
    with input from the user.

    Raise it and catch it to seek clarity for the user,
    """
    pass
