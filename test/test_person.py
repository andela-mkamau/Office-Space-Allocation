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

    def test_can_perform_equality_comparison_btn_fellows(self):
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

    def test_can_perform_equality_comparison_btn_staff(self):
        """
        Should be able to do an equality comparison between two Staff
        """
        s1 = staff.Staff("Joshua", "Kimani")
        s2 = staff.Staff("joshua", "kimani")
        s1.unique_id = 344
        s2.unique_id = 45
        self.assertNotEqual(s1, s2)

        s1.unique_id = 66
        s2.unique_id = 66
        self.assertEqual(s1, s2)

    def test_can_perform_equality_comparison_btn_staff_fellows(self):
        """
        Should be able to perform equality comparison between Staff and Fellows
        """
        s1 = staff.Staff("NN", "PP")
        f1 = fellow.Fellow("NN", "PP")
        self.assertNotEqual(s1, f1)

