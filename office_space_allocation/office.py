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
        return self.get_num_occupants() < 7
