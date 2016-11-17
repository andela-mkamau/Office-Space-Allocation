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
