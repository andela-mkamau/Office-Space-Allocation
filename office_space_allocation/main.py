from office_space_allocation import amity
from office_space_allocation.utilities import AmbiguityException


def create_room(room_names):
    """
    Creates Room objects with specified names.

    A Room can either be of type Office or Livingspace. The user is
    asked to specify Room type
    """
    