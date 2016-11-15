import unittest
from office_space_allocation import office


class TestRoomFunctionality(unittest.TestCase):
    """
    Tests the functionality of Room class, and its subclasses LivingRoom and Office
    """
    def test_office_room_has_zero_occupants_by_default(self):
        """
        By default, a Office room created should have zero occupants
        """
        rm = office.Office()
        self.assertEqual(rm.get_num_occupants(), 0, msg='By default, an Office room created should have zero occupants')
