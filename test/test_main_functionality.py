import unittest
from office_space_allocation import main


class TestMainFunctionality(unittest.TestCase):
    """
    Tests the main functionalities of the Office Space Allocation system
    """

    def test_can_add_office_rooms_to_amity(self):
        """
        Given arbitrary command line args as room type and room names, the create_room
        command should be able to add Office rooms to Amity
        """
        args = {
            '<room_name>' : ['Hogwats', 'Oculus'],
            'office': True,
            'livingspace': False,
        }
        main.create_room(args)
        self.assertListEqual(
            args['<room_name>'],
            [r.get_name() for r in main.main_amity.all_rooms]
        )


        

