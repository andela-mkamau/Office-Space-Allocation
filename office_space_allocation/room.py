class Room:
    def __init__(self):
        self.occupants = []

    def get_num_occupants(self):
        """
        Fetches and returns the number of occupants in a Room
        :return: number of occupants : ```int```
        """
        return len(self.occupants)
