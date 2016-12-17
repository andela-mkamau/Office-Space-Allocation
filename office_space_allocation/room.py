from abc import ABCMeta, abstractmethod
from office_space_allocation.person import Person


class Room(metaclass=ABCMeta):
    def __init__(self, name):
        self.occupants = []
        self.name = name

    def get_num_occupants(self):
        """
        Fetches and returns the number of occupants in a Room
        :return: number of occupants : ```int```
        """
        return len(self.occupants)

    def get_occupants_tuple(self):
        return tuple(self.occupants)

    def get_name(self):
        """
        Fetches and returns the name of the room, formatted in title case
        :return: ```str``` : name of room
        """
        return self.name.title()

    @abstractmethod
    def add_person(self, person):
        pass

    @abstractmethod
    def can_accept_occupants(self):
        pass

    def has_person(self, person):
        """
        Checks if this Room has Person person

        :param person: `Person` to check for
        :return: `True` if Room has this Person, else `False`
        """
        for p in self.occupants:
            if person == p:
                return True
        return False

    def remove_person(self, person):
        """
        Fetches, removes and returns a Person from the list of occupants in the Room
        :param person:
        :return: ```Person``` person
        """
        if not isinstance(person, Person):
            raise TypeError("Argument must be of type Person")
        elif self.get_num_occupants() == 0:
            raise ValueError("Room is empty!")
        elif person in self.occupants:
            self.occupants.remove(person)
            return person
        else:
            raise ValueError("Person not found iin this Room")

    def __eq__(self, other_room):
        """
        Makes equality comparison between this Room and other_room
        """
        pass
