import unittest

from office_space_allocation import main, office, staff


class TestMainFunctionality(unittest.TestCase):
    """
    Tests the main functionalities of the Office Space Allocation system
    """

    def test_can_add_office_rooms_to_amity(self):
        """
        Given  command line args as room type and room names, the create_room
        command should be able to add Office rooms to Amity
        """
        main.main_amity.all_rooms = []
        args = {
            '<room_name>': ['Hogwats', 'Oculus'],
            'office': True,
            'livingspace': False,
        }
        main.create_room(args)
        self.assertListEqual(
            args['<room_name>'],
            [r.get_name() for r in main.main_amity.all_rooms]
        )

    def test_can_add_livingspace_rooms_to_amity(self):
        """
        Given  command line args as room type and room names, the create_room
        command should be able to add LivingSpace rooms to Amity
        """
        main.main_amity.all_rooms = []
        args = {
            '<room_name>': ['Shell', 'Php'],
            'office': False,
            'livingspace': True,
        }
        main.create_room(args)
        self.assertListEqual(
            args['<room_name>'],
            [r.get_name() for r in main.main_amity.all_rooms]
        )

    def test_can_add_and_allocate_person_room(self):
        """
        Given correct command line args, add_person should be able to add Person to amity and allocate random room
        """
        main.main_amity.all_rooms = []
        main.main_amity.add_room(office.Office("Oculus"))
        args = {'<first_name>': 'john',
                '<last_name>': 'king',
                '<title>': 'STAFF',
                '<wants_accommodation>': 'Y'}
        main.add_person(args)
        self.assertEquals(main.main_amity.find_room("Oculus").get_num_occupants(), 1)

    def test_can_reallocate_person_to_another_room(self):
        """
        Given correct command line args, reallocate_person should be able to reallocate Person to new Room
        """
        main.main_amity.all_rooms = []
        main.main_amity.all_persons = []
        args = {'<first_name>': 'mike',
                '<last_name>': 'sam',
                '<new_room_name>': 'mordor'}

        p = staff.Staff("Mike", "Sam")
        main.main_amity.add_person(p)
        rm1 = office.Office("oculus")
        main.main_amity.add_room(rm1)
        main.main_amity.allocate_room(p)

        rm2 = office.Office("mordor")
        main.main_amity.add_room(rm2)
        self.assertFalse(rm2.has_person(p))

        main.reallocate_person(args)
        self.assertTrue(rm2.has_person(p))
