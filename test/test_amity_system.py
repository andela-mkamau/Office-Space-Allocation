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
