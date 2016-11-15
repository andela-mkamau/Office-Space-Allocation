import unittest
from office_space_allocation import staff
from office_space_allocation import person
from office_space_allocation import fellow

class TestOfficeSpaceAllocationClassStructure(unittest.TestCase):
    """
    Tests the class structure model for the Office Space Allocation
    """

    def test_staff_is_subclass_of_person(self):
        """
        Staff should be a subclass of the Person class
        """
        self.staff = staff.Staff()
        self.assertIsInstance(self.staff, person.Person, msg="Staff should be a subclass of Person")

    def test_fellow_is_subclass_of_person(self):
        """
        Fellow should be a subclass of the Person class
        """
        self.f1 = fellow.Fellow()
        self.assertIsInstance(self.f1, person.Person, msg="Fellow should be a subclass of Person")