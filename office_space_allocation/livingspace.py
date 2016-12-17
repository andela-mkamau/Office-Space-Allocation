from office_space_allocation.room import Room
from office_space_allocation.fellow import Fellow
from office_space_allocation.staff import Staff
from office_space_allocation.utilities import InvalidRoomOccupantError
from office_space_allocation.utilities import RoomFullError


class LivingSpace(Room):
    def can_accept_occupants(self):
        return self.get_num_occupants() < 4

    def add_person(self, person):
        """
        Adds ```Person``` person to the list of occupants of the LivingRoom
        Person should only be of type Fellow

        :param : ```Person``` person
        """
        if self.can_accept_occupants():
            if isinstance(person, Fellow):
                self.occupants.append(person)
            elif isinstance(person, Staff):
                raise InvalidRoomOccupantError("Staff cannot join LivingRooms")
        else:
            raise RoomFullError("LivingSpace is full")

    def __eq__(self, other_room):
        """
        Makes equality comparison between this Room and other_room
        """
        return (isinstance(other_room, LivingSpace) and
                self.name == other_room.name and
                self.occupants == other_room.occupants)
