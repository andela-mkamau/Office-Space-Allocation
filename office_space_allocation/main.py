from office_space_allocation import amity, office, staff, livingspace, fellow

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


def add_person(args):
    """
    Adds a person to the system and allocates the person to a random room.

    :param args: Command line args from docopt
    '<first_name>': 'john',
                '<last_name>': 'king',
                '<title>': 'STAFF',
                '<wants_accommodation>': 'Y'}
    """
    if args['<title>'].lower() not in ('staff', 'fellow'):
        print("Invalid syntax!")
        print(args['<first_name>'].title(), args['<last_name>'].title(), "must either be a FELLOW or STAFF")
        print("""\nUsage:
            add_person <first_name> <last_name> <title> [<wants_accommodation>]""")
        return
    elif args['<wants_accommodation>'] not in (None, 'y', 'n', 'Y', 'N', 'yes', 'no', 'No', 'Yes', 'YES', 'NO'):
        print("Invalid syntax!")
        print("If", args['<first_name>'].title(), args['<last_name>'].title(), "wants accommodation, please indicate "
                                                                               "with a yes or no in the last argument")
        print("""\nUsage:
                    add_person <first_name> <last_name> <title> [<wants_accommodation>]""")
        return

    if args['<wants_accommodation>']:
        if args['<wants_accommodation>'].lower().startswith('y'):
            wants_accommodation = 'y'
        elif args['<wants_accommodation>'].lower().startswith('n'):
            wants_accommodation = 'n'
    else:
        wants_accommodation = 'n'

    try:
        if args['<title>'].lower() == "staff":
            p = staff.Staff(args['<first_name>'], args['<last_name>'])
            main_amity.add_person(p)
            if wants_accommodation == 'y':
                main_amity.allocate_room(p)
        elif args['<title>'].lower() == "fellow":
            p = fellow.Fellow(args['<first_name>'], args['<last_name>'])
            main_amity.add_person(p)
            if wants_accommodation == 'y':
                main_amity.allocate_room(p)
    except IndexError as e:
        print("Error allocating room.\n", e)
