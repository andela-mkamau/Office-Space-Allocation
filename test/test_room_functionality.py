import unittest
from office_space_allocation import office
from office_space_allocation import livingspace
from office_space_allocation import fellow


class TestRoomFunctionality(unittest.TestCase):
    """
    Tests the functionality of Room class, and its subclasses LivingRoom and Office
    """

    def test_office_room_has_zero_occupants_by_default(self):
        """
        By default, a Office room created should have zero occupants
        """
        rm = office.Office("Main office")
        self.assertEqual(rm.get_num_occupants(), 0, msg='By default, an Office room created should have zero occupants')

    def test_get_name_office_room(self):
        """
        Should return the name of the office room, formatted in title case
        """
        self.rm = office.Office("Quiet room")
        self.assertEqual(self.rm.get_name(), "Quiet Room")

    def test_get_name_livingspace(self):
        """
        Should be able to get name of LivingSpace room, formatted in title case
        """
        self.lvroom = livingspace.LivingSpace("Chillout place")
        self.assertEqual(self.lvroom.get_name(), "Chillout Place")

    def test_can_add_fellow_to_office_room(self):
        """
        Should be able to add fellows to Office room
        """
        of = office.Office("New Office")
        fel = fellow.Fellow("Mary", "Jane")
        of.add_person(fel)
        self.assertEqual(fel, self.of.occupants[0])
