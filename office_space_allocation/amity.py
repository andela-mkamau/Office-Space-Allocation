from office_space_allocation.person import Person
from office_space_allocation.fellow import Fellow
from office_space_allocation.staff import Staff


class Amity:
    # TODO : Complete definition
    def __init__(self):
        self.all_persons = []
        self.all_rooms = []
        self.allocated_rooms = []

    def add_person(self, person):
        """
        Adds a new Person to list of persons
        :param: ```Person``` person
        """
        if not isinstance(person, Person):
            raise TypeError("Argument should be of type Person")
        else:
            self.all_persons.append(person)

    def add_room(self, new_room):
        """
        Adds ```Room``` new_room to list of all_rooms
        :param ```Room``` new_room
        """
        self.all_rooms.append(new_room)

    def find_room(self, name):
        """
        Find a ```Room``` object using name
        :param name: ```str``` name of the Room to look for
        :return: ```Room``` object if found
        """
        name = name.lower()
        for r in self.all_rooms:
            if name == r.get_name().lower():
                return r
        raise ValueError(name + " not found!")
