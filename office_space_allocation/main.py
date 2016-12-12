from office_space_allocation import amity, office, livingspace

main_amity = None


def init_amity():
    """
    Initialises the Amity class
    """
    global main_amity
    main_amity = amity.Amity()


init_amity()


def create_room(args):
    """
    Creates Room objects with specified names and adds them to Amity.

    A Room can either be of type Office or Livingspace. The user specifies the room type
    """
    if args['office']:
        office_rooms = [office.Office(name) for name in args['<room_name>']]
        for r in office_rooms:
            main_amity.add_room(r)
    if args['livingspace']:
        ls_rooms = [livingspace.LivingSpace(name) for name in args['<room_name>']]
        for r in ls_rooms:
            main_amity.add_room(r)
