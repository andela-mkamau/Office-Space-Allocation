import unittest
from office_space_allocation import main


class TestMainFunctionality(unittest.TestCase):
    """
    Tests the main functionalities of the Office Space Allocation system
    """

    def test_can_add_room_to_amity(self):
        """
        Given arbitrary command line args as room names, the create_room 
        command should be able to add rooms to Amity
        """
        

