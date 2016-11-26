from office_space_allocation.person import Person


class Fellow(Person):
    def __eq__(self, other_person):
        """
        Tests for equality between this Person and the other_person
        """
        return (isinstance(other_person, Fellow) and
                self.first_name == other_person.first_name and
                self.last_name == other_person.last_name and
                self.unique_id == other_person.unique_id)
