import unittest
from office_space_allocation import staff
from office_space_allocation import person

class TestOfficeSpaceAllocationClassStructure(unittest.TestCase):
    """
    Tests the class structure model for the Office Space Allocation
    """

    def test_staff_is_subclass_of_person(self):
        """
        Staff should be a subclass of the Person class
        """
        assert issubclass(staff.Staff, person.Person), "Staff should be a subclass of Person"
