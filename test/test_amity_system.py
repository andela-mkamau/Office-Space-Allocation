import unittest
from office_space_allocation import amity
from office_space_allocation import fellow
from office_space_allocation import staff
from office_space_allocation import office
from office_space_allocation import livingspace


class TestAmitySystem(unittest.TestCase):
    """
    Tests for the functionality the major components of the system
    """

    def setUp(self):
        self.amity = amity.Amity()

    def test_can_add_person_to_list(self):
        """
        Should be able to add Person to list of person
        """
        p1 = fellow.Fellow("New", "Guy")
        p2 = staff.Staff("New", 'Staff')
        self.amity.add_person(p1)
        self.amity.add_person(p2)
        self.assertTupleEqual(
            (self.amity.all_persons[0], self.amity.all_persons[1]),
            (p1, p2)
        )

    def test_can_add_new_room_to_list_rooms(self):
        """
        Should be able to add rooms to list of rooms
        """
        rm1 = office.Office("New Office")
        rm2 = livingspace.LivingSpace("Chillout Room")
        self.amity.add_room(rm1)
        self.amity.add_room(rm2)
        self.assertTupleEqual(
            (self.amity.all_rooms[1], self.amity.all_rooms[0]),
            (rm2, rm1)
        )

    def test_can_find_room_by_name(self):
        """
        Should be able to find Room using name
        """
        rm1 = office.Office("office 1")
        rm2 = livingspace.LivingSpace("Livingroom 1")
        self.amity.add_room(rm1)
        self.amity.add_room(rm2)

        self.assertTupleEqual(
            (self.amity.find_room("livingroom 1"),
             self.amity.find_room("office 1")),
            (rm2, rm1)
        )

    def test_raises_valueerror_room_not_found(self):
        """
        Should raise a ValueError when room is not found
        """
        with self.assertRaises(ValueError):
            self.amity.find_room("No Room Here")

    def test_can_allocate_room_to_person(self):
        """
        Should be able to allocate room to a Person
        """
        rm1 = office.Office("Room 1")
        rm2 = livingspace.LivingSpace("Room 2")
        rm3 = livingspace.LivingSpace("Room 3")
        self.amity.add_room(rm1)
        self.amity.add_room(rm2)
        self.amity.add_room(rm3)

        fel = fellow.Fellow("Tat", "Pap")

        fel_room = self.amity.allocate_room(fel)

        self.assertEqual(fel, fel_room.get_occupants_tuple()[0])
