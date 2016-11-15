class Room:
    def __init__(self, name):
        self.occupants = []
        self.name = name

    def get_num_occupants(self):
        """
        Fetches and returns the number of occupants in a Room
        :return: number of occupants : ```int```
        """
        return len(self.occupants)

    def get_name(self):
        """
        Fetches and returns the name of the room, formatted in title case
        :return: ```str``` : name of room
        """
        return self.name.title()