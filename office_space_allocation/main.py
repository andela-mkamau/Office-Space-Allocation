from office_space_allocation import amity, office, staff, livingspace, fellow, utilities
import os
import re

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
            if not main_amity.has_room(r):
                main_amity.add_room(r)
                print("Successfully created office room:", r.get_name())
            else:
                print("{} already exists in Amity. Cannot create duplicate room!".format(r.get_name()))
    if args['livingspace']:
        ls_rooms = [livingspace.LivingSpace(name) for name in args['<room_name>']]
        for r in ls_rooms:
            if not main_amity.has_room(r):
                main_amity.add_room(r)
                print("Successfully created livingspace room:", r.get_name())
            else:
                print("{} already exists in Amity. Cannot create duplicate room!".format(r.get_name()))


def add_person(args):
    """
    Adds a person to the system and allocates the person to a random room.

    :param args: Command line args from docopt
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
            print("Successfully added", p.get_full_name(), "to Amity.")
            if wants_accommodation == 'y':
                r = main_amity.allocate_room(p)
                print("Successfully allocated", p.get_full_name(), "to", r.get_name())
        elif args['<title>'].lower() == "fellow":
            p = fellow.Fellow(args['<first_name>'], args['<last_name>'])
            main_amity.add_person(p)
            print("Successfully added", p.get_full_name(), "to Amity.")
            if wants_accommodation == 'y':
                main_amity.allocate_room(p)
                print("Successfully allocated", p.get_full_name(), "to", r.get_name())
    except IndexError as e:
        print("Error allocating room.\n", e)


def reallocate_person(args):
    """
    Reallocates a Person to a Room with name `new_room_name`
    """
    name = args['<first_name>'].strip().title() + " " + args['<last_name>'].strip().title()
    room_name = args['<new_room_name>']
    try:
        main_amity.reallocate_person(name, room_name)
        print("Successfully reallocated", name, "to", room_name)
    except ValueError as e:
        print("Error found while reallocating room\nThe room", e)
    except utilities.InvalidRoomOccupantError as e:
        print("Error found while reallocating person!")
        print(name, "cannot be reallocated to", room_name)
    except utilities.RoomFullError as e:
        print("Error found while reallocating person!")
        print(room_name, "is already full! Please try with another room or remove some people there")
    except Exception as e:
        print("Error found while reallocating person.\n", e, "\n\n Type help to view all commands")


def _get_line_data(line_data):
    """
    Helper function to construct args when loading people from file
    """
    data = re.split("\s+", line_data)
    args = {}
    if len(data) == 4:
        args['<first_name>'] = data[0]
        args['<last_name>'] = data[1]
        args['<title>'] = data[2]
        args['<wants_accommodation>'] = data[3]
        return args
    elif len(data) == 3:
        args['<first_name>'] = data[0]
        args['<last_name>'] = data[1]
        args['<title>'] = data[2]
        args['<wants_accommodation>'] = None
        return args
    else:
        print("Error processing data!")
        print("The data file contains invalid data. Also check for incorrect formatting.")


def load_people(args):
    """
    Adds people to rooms from a txt file.
    """
    file_path = args['FILE']
    if not os.path.isfile(file_path):
        print("Error reading file...")
        print("The file path provided does not exist")
        return

    with open(file_path, encoding='utf-8') as data_file:
        line_no = 0
        for line in data_file:
            args = _get_line_data(line.strip())
            line_no += 1
            if args:
                add_person(args)
            else:
                print("Skipping line ", line_no)
                continue
