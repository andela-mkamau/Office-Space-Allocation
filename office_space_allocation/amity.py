from office_space_allocation.person import Person
from office_space_allocation.fellow import Fellow
from office_space_allocation.staff import Staff
from office_space_allocation.office import Office
from office_space_allocation.utilities import InvalidRoomOccupantError
from office_space_allocation.utilities import RoomFullError
from office_space_allocation.utilities import MultiplePeopleFoundException
import random


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

    def allocate_room(self, person):
        """
        Allocates a room to ```Person``` person.

        This is done randomly.
        :param person: ```Person``` to allocate room
        :return: room : ```Room``` allocated , if possible
        """
        if isinstance(person, Staff):
            # allocate only offices
            offices = [of for of in self.all_rooms if isinstance(of, Office)]
            if len(offices) < 1:
                raise IndexError("There are no more Office rooms to allocate. Please create some rooms before making "
                                 "allocations")
            else:
                rm = random.choice(offices)

                rm.add_person(person)
                self.allocated_rooms.append(rm)
                return rm
        elif isinstance(person, Fellow):
            # raise exception if there are no rooms
            if len(self.all_rooms) < 1:
                raise IndexError("There are no available rooms. Please create some rooms before making allocations.")
            else:
                office_rm = random.choice(self.all_rooms)
                office_rm.add_person(person)
                self.allocated_rooms.append(office_rm)
                return office_rm
        else:
            raise TypeError("Person argument must be of type Staff or Fellow")

    def find_person(self, name):
        """
        Finds a Person using name.
        Name can be the full name, first name, last name or part of either
        :param name:
        :return: a tuple with Person(s) objects found in the list if persons
        """
        name = name.strip()
        res = [p for p in self.all_persons if name.title() in p.get_full_name()]
        if not res:
            raise Exception("Person was not found in the system")
        else:
            return tuple(res)

    def reallocate_person(self, person_name, room_name):
        """
        Reallocates `Person` to another `Room` if possible

        :param: person_name: Name of the `Person`
        :param: room_name: Name of the `Room`
        :return: a tuple with (`Person`, `Room`) if reallocation is successful
        """
        person_name = person_name.strip()
        room_name = room_name.strip()

        try:
            # only one person should be found
            people_found = self.find_person(person_name)
            if len(people_found) > 1:
                raise MultiplePeopleFoundException
            else:
                person = people_found[0]
        except Exception:
            raise

        try:
            room = self.find_room(room_name)
        except ValueError:
            raise

        if person in room.get_occupants_tuple():
            raise Exception("Cannot reallocate person to same room.\n {} is already in {}".format(person_name,
                                                                                                  room_name))

        # remove person in current room
        # TODO: Add error checking if person is not in any room
        for r in self.all_rooms:
            if person in r.get_occupants_tuple():
                r.remove_person(person)
                break

        # add person to room
        try:
            room.add_person(person)
        except InvalidRoomOccupantError:
            raise
        except RoomFullError:
            raise
        return person, room
