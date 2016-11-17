import unittest
from office_space_allocation import office
from office_space_allocation import livingspace
from office_space_allocation import staff
from office_space_allocation import fellow
from office_space_allocation import amity


class TestDatabaseOperations(unittest.TestCase):
    """
    Tests operations performed when saving or retrieving application state in a 
    sqlite database
    """

    def setUp(self):
        self.amity = amity.Amity()

    @unittest.skip("Test not complete")
    def test_can_save_retrieve_application_state_to_sqlite_database(self):
        """
        Should be able to save and retrieve all application state to sqlite database
        """
        # add rooms
        rm1 = office.Office("Main Office")
        rm2 = livingspace.LivingSpace("Living Space")
        self.amity.add_room(rm1)
        self.amity.add_room(rm2)
        # add persons
        p1 = staff.Staff("Mary", "mary")
        p2 = fellow.Fellow("Jack", "Bauer")
        self.amity.add_person(p1)
        self.amity.add_person(p2)
        # allocate rooms
        self.amity.allocate_room(p2)
        self.amity.allocate_room(p1)

        # save state
        db.save_state(self.amity, 'test_db')

        # make another system
        self.another_amity = amity.Amity()

        # retrieve stored state
        state = db.load_state(self.another_amity, 'test_db')

        self.assertTupleEqual(
            (self.amity.all_rooms, self.amity.all_persons),
            self.state
        )
