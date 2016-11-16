import unittest
from office_space_allocation import person


class TestPersonClass(unittest.TestCase):
    """
    Tests functionality of the Person class
    """

    def test_can_get_person_full_name(self):
        """
        Should be able to get the Person full name
        """
        p1 = person.Person("mike", "kamau")
        self.assertEqual("Mike Kamau", p1.get_full_name())
