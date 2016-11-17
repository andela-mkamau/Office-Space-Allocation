import unittest
from office_space_allocation import amity
from office_space_allocation import fellow
from office_space_allocation import staff


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
