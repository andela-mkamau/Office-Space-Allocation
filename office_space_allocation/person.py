class Person:
    def __init__(self, fname, lname):
        self.first_name = fname
        self.last_name = lname

    def get_full_name(self):
        """
        Returns the Person full name
        Combination of first name and second name
        :return: full name in title case
        """
        full_name = self.first_name.strip().title() + " " + self.last_name.strip().title()
        return full_name
