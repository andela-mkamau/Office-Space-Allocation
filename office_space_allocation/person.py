class Person:
    id = 0  # id to uniquely identify the person

    def __init__(self, fname, lname):
        self.first_name = fname
        self.last_name = lname
        Person.id += 1
        self.unique_id = Person.id

    def get_full_name(self):
        """
        Returns the Person full name
        Combination of first name and second name
        :return: full name in title case
        """
        full_name = self.first_name.strip().title() + " " + self.last_name.strip().title()
        return full_name

    def __eq__(self, other_person):
        """
        Tests for equality between this Person and the other_person
        """
        pass