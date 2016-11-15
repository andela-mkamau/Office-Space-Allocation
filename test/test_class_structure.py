import unittest


class TestOfficeSpaceAllocationClassStructure(unittest.TestCase):
    """
    Tests the class structure model for the Office Space Allocation
    """

    def test_staff_is_subclass_of_person(self):
        """
        Staff should be a subclass of the Person class
        """
        self.staff = staff.Staff("King", "Kong")
        assert issubclass(self.staff, person.Person), "Staff should be a subclass of Person"
