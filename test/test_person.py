import unittest
from office_space_allocation import person, fellow, staff


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

    def test_can_perfrom_equality_comparison_btn_fellows(self):
        """
        Should be able to do an equality comparison between Fellows
        """
        f1 = fellow.Fellow("Joshua", "Kimani")
        f2 = fellow.Fellow("Joshua", "Kimani")
        f1.unique_id = 344
        f2.unique_id = 45
        self.assertNotEqual(f1, f2)

        f1.unique_id = 66
        f2.unique_id = 66
        self.assertEqual(f1, f2)
