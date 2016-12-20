from office_space_allocation.person import Person


class Fellow(Person):
    def __eq__(self, other_person):
        """
        Tests for equality between this Person and the other_person
        """
        return (isinstance(other_person, Fellow) and
                self.first_name.lower() == other_person.first_name.lower() and
                self.last_name.lower() == other_person.last_name.lower() and
                self.unique_id == other_person.unique_id)
