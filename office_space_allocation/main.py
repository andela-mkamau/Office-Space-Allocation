from office_space_allocation import amity, office, staff, livingspace, fellow, utilities, db
import os
import sqlite3
import re
import subprocess
from tabulate import tabulate

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
                try:
                    r = main_amity.allocate_room(p)
                    print("Successfully allocated", p.get_full_name(), "to", r.get_name())
                except utilities.RoomFullError as e:
                    print("Error allocating", p.get_full_name(), "room\n ", e)

        elif args['<title>'].lower() == "fellow":
            p = fellow.Fellow(args['<first_name>'], args['<last_name>'])
            main_amity.add_person(p)
            print("Successfully added", p.get_full_name(), "to Amity.")
            if wants_accommodation == 'y':
                try:
                    r = main_amity.allocate_room(p)
                    print("Successfully allocated", p.get_full_name(), "to", r.get_name())
                except utilities.RoomFullError as e:
                    print("Error allocating", p.get_full_name(), "room\n ", e)
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


def print_allocations(args):
    """
    Prints a list of allocations onto the screen
    Specifying the optional -o option here outputs the registered allocations to a txt file.
    """
    allocations = {}
    for r in main_amity.all_rooms:
        if r.get_num_occupants() > 0:
            allocations[r.get_name()] = []
            for p in r.get_occupants_tuple():
                allocations[r.get_name()].append(p.get_full_name())

    if not allocations:
        print("There exists no allocations at the moment. Please make some room allocations first.")
        return
    data = tabulate(allocations, headers='keys', tablefmt='fancy_grid')
    if args['-o'] and args['FILE']:
        with open(args['FILE'], encoding='utf-8', mode='w') as output_file:
            output_file.write(data)
            print("Successfully wrote room allocations to the file", args['FILE'])
    elif not args['-o'] and not args['FILE']:
        print(data)
    else:
        print("Invalid syntax.")
        print("""Usage:
            print_allocations [-o FILE]""")


def print_unallocated(args):
    """
    Prints a list of unallocated people to the screen
    """
    allocated_people = []
    for r in main_amity.all_rooms:
        if r.get_num_occupants() > 0:
            for p in r.get_occupants_tuple():
                allocated_people.append(p.get_full_name())
    all_people = [p.get_full_name() for p in main_amity.all_persons]
    unallocated = [p_name for p_name in all_people if p_name not in allocated_people]
    if not unallocated:
        print("There exists no unallocated people at the moment.")
        return
    data = tabulate({'Unallocated People': unallocated}, headers='keys', tablefmt='fancy_grid')

    if args['-o'] and args['FILE']:
        with open(args['FILE'], encoding='utf-8', mode='w') as output_file:
            output_file.write(data)
            print("Successfully wrote list of unallocated persons to the file", args['FILE'])
    elif not args['-o'] and not args['FILE']:
        print(data)
    else:
        print("Invalid syntax.")
        print("""Usage:
            print_unallocated [-o FILE]""")


def print_room(args):
    """
    Prints the names of all the people in a room on the screen.
    """
    try:
        room = main_amity.find_room(args['<room_name>'])
        room_occupants = [p.get_full_name() for p in room.occupants]

        if not room_occupants:
            print("{} is currently empty. Please allocate or reallocate people here.".format(room.get_name()))
            return
        data = {room.get_name() + " occupants:": room_occupants}
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
    except ValueError:
        print("The room {} doesn't exist. You could create it. Please type help to view all "
              "commands.".format(args['<room_name>']))


def save_state(args):
    """
    Persists all the data stored in the app to a SQLite database.
    """
    db_file = args['--db'] if args['--db'] else "amity_db"

    try:
        db.save_state(main_amity, db_file)
        print("Successfully saved Amity state to ", db_file, "sqlite database")
    except sqlite3.Error as e:
        print("Error found when saving state.\n ", e)
        print("Please try again.")


def load_state(args):
    db_path = args['<sqlite_database>']
    if not os.path.isfile(db_path):
        print("Error reading database file...")
        print("The file path provided does not exist")
        return
    file_type = str(subprocess.check_output(('file', db_path)), 'utf-8').strip()
    if 'sqlite' not in file_type.lower():
        print(os.path.abspath(db_path), "is not a valid Sqlite database. Please use a valid database")
        return
    else:
        state = db.load_state(db_path)
        main_amity.all_rooms, main_amity.all_persons = state
        print("Successfully loaded state from", os.path.abspath(db_path))
