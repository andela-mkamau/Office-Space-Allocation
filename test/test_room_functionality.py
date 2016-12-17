import unittest
from office_space_allocation import office
from office_space_allocation import livingspace
from office_space_allocation import fellow
from office_space_allocation import staff
from office_space_allocation.utilities import InvalidRoomOccupantError
from office_space_allocation.utilities import RoomFullError


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
        self.assertEqual(fel, of.occupants[0])

    def test_can_add_fellow_to_livingspace_room(self):
        """
        Should be able to add fellow to LivingRoom rooms
        """
        lroom = livingspace.LivingSpace("Kitchen")
        fel = fellow.Fellow("May", "Teresa")
        lroom.add_person(fel)
        self.assertEqual(fel, lroom.occupants[0])

    def test_can_add_staff_to_office_room(self):
        """
        Should be able to add staff to Office room
        """
        staf = staff.Staff("TT", "PP")
        of = office.Office("Main Office")
        of.add_person(staf)
        self.assertEqual(staf, of.occupants[0])

    def test_livingspace_raise_error_for_addition_of_staff(self):
        """
        LivingSpace should raise an InvalidRoomOccupantError exception when Staff tries to join it.
        """
        staf = staff.Staff("TT", "PP")
        lroom = livingspace.LivingSpace("Livingroom")
        with self.assertRaises(InvalidRoomOccupantError):
            lroom.add_person(staf)

    def test_adding_occupants_to_full_office_raises_exception(self):
        """
        A full Office (6 occupants) should raise RoomFullError when occupants are added to it.
        """
        of = office.Office("Oculus")
        with self.assertRaises(RoomFullError):
            # add 7 fellows to this room
            for i in range(8):
                of.add_person(fellow.Fellow("Fellow", str(i)))

    def test_adding_occupants_to_full_livingspace_raises_exception(self):
        """
        A full LivingSpace should raise a RoomFullError when adding more occupants
        """
        lspace = livingspace.LivingSpace('TV Room')
        with self.assertRaises(RoomFullError):
            # add 5 fellows to this room
            for i in range(6):
                lspace.add_person(fellow.Fellow("Fellow", str(i)))

    def test_livingspace_raise_error_for_addition_of_staff(self):
        """
        LivingRoom should raise an InvalidRoomOccupantError exception when Staff tries to join it.
        """
        staf = staff.Staff("TT", "PP")
        lspace = livingspace.LivingSpace("Livingroom")
        with self.assertRaises(InvalidRoomOccupantError):
            lspace.add_person(staf)

    def test_can_remove_fellow_from_office(self):
        """
        Should be able to remove a Fellow from Office room
        """
        of = office.Office("Hogwarts")
        f1 = fellow.Fellow("Nan", "Pi")
        f2 = fellow.Fellow("KK", "Brown")
        of.add_person(f1)
        of.add_person(f2)

        self.assertTupleEqual(
            (of.remove_person(f2), of.remove_person(f1)),
            (f2, f1)
        )

        self.assertEquals(0, of.get_num_occupants())

    def test_room_raises_valueerror_if_person_not_found(self):
        """
        Room should raise  a ValueError if Person is not found in it when being removed
        """
        of = office.Office("Main Office")
        with self.assertRaises(ValueError):
            of.remove_person(fellow.Fellow("IIY", "GGFD"))

    def test_can_remove_fellows_staff_from_office(self):
        """
        Should be able to remove Fellows and Staff from office
        """
        f1 = fellow.Fellow("Mark", "Mike")
        f2 = fellow.Fellow("JJ", "PP")
        s1 = staff.Staff("FF", "KK")
        s2 = staff.Staff("G", "FF")
        of = office.Office("Small Office")
        of.add_person(f1)
        of.add_person(f2)
        of.add_person(s1)
        of.add_person(s2)

        self.assertTupleEqual(
            (of.remove_person(s1), of.remove_person(s2), of.remove_person(f2),
             of.remove_person(f1),),
            (s1, s2, f2, f1)
        )

    def test_can_check_if_room_has_person(self):
        """
        Should be able to check if a Room has a Person
        """
        of1 = office.Office("oculus")
        liv = livingspace.LivingSpace("Game Room")
        f1 = fellow.Fellow("Nad", "Nate")
        s1 = staff.Staff("Luke", "John")

        self.assertFalse(of1.has_person(f1))
        self.assertFalse(liv.has_person(s1))

        of1.add_person(f1)
        self.assertTrue(of1.has_person(f1))
        of1.remove_person(f1)
        self.assertFalse(of1.has_person(f1))

        of1.add_person(s1)
        self.assertTrue(of1.has_person(s1))

        liv.add_person(f1)
        self.assertTrue(liv.has_person(f1))
