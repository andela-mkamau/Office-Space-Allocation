from office_space_allocation.room import Room
from office_space_allocation.utilities import RoomFullError


class Office(Room):
    def add_person(self, person):
        """
        Adds Person ```person``` to the list of occupants of the Office room
        """
        # Check if room is full
        if self.can_accept_occupants():
            self.occupants.append(person)
        else:
            raise RoomFullError("Room is full!")

    def can_accept_occupants(self):
        """
        Office can have a maximum of 6 occupants
        """
        return self.get_num_occupants() < 6

    def __eq__(self, other_room):
        """
        Makes equality comparison between this Room and other_room
        """
        return (isinstance(other_room, Office) and
                self.name.lower() == other_room.name.lower() and
                self.occupants == other_room.occupants)
