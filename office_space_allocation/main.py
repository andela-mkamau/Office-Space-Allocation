import os
import re
import sqlite3
import subprocess
import sys
from colorama import Fore, Style

from tabulate import tabulate

from office_space_allocation import amity, office, staff, livingspace, fellow, utilities, db

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
                print(Fore.GREEN + "Successfully created office room:", r.get_name() + Style.RESET_ALL)
            else:
                print(Fore.RED + "{} already exists in Amity. Cannot create duplicate room!".format(r.get_name()) +
                      Style.RESET_ALL)
    if args['livingspace']:
        ls_rooms = [livingspace.LivingSpace(name) for name in args['<room_name>']]
        for r in ls_rooms:
            if not main_amity.has_room(r):
                main_amity.add_room(r)
                print(Fore.GREEN + "Successfully created livingspace room:", r.get_name() + Style.RESET_ALL)
            else:
                print(Fore.RED + "{} already exists in Amity. Cannot create duplicate room!".format(r.get_name()) +
                      Style.RESET_ALL)


def add_person(args):
    """
    Adds a person to the system and allocates the person to a random room.

    :param args: Command line args from docopt
    """
    if args['<title>'].lower() not in ('staff', 'fellow'):
        print(Fore.RED + "Invalid syntax!")
        print(args['<first_name>'].title(), args['<last_name>'].title(), "must either be a FELLOW or STAFF" +
              Style.RESET_ALL)
        print("""\nUsage:
            add_person <first_name> <last_name> <title> [<wants_accommodation>]""")
        return
    elif args['<wants_accommodation>'] not in (None, 'y', 'n', 'Y', 'N', 'yes', 'no', 'No', 'Yes', 'YES', 'NO'):
        print(Fore.RED + "Invalid syntax!")
        print("If", args['<first_name>'].title(), args['<last_name>'].title(), "wants accommodation, please indicate "
                                                                               "with a yes or no in the last argument"
              + Style.RESET_ALL)
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
            print(Fore.GREEN + "Successfully added", p.get_full_name(), "to Amity." + Style.RESET_ALL)
            try:
                r = main_amity.allocate_room(p)
                print(Fore.GREEN + "Successfully allocated", p.get_full_name(), "to", r.get_name() + Style.RESET_ALL)
            except utilities.RoomFullError as e:
                print(Fore.RED + "Error allocating", p.get_full_name(), "room\n ", e, Style.RESET_ALL)

        elif args['<title>'].lower() == "fellow":
            p = fellow.Fellow(args['<first_name>'], args['<last_name>'])
            main_amity.add_person(p)
            print(Fore.GREEN + "Successfully added", p.get_full_name(), "to Amity." + Style.RESET_ALL)

            try:
                r = main_amity.allocate_room(p)
                print(Fore.GREEN + "Successfully allocated", p.get_full_name(), "to",
                      r.get_name() + Style.RESET_ALL)
            except utilities.RoomFullError as e:
                    print(Fore.RED + "Error allocating", p.get_full_name(), "room\n ", e, Style.RESET_ALL)
            except IndexError as e:
                print(Fore.RED + "Error allocating room.\n", e, Style.RESET_ALL)

            if wants_accommodation == 'y':
                try:
                    lv_room = main_amity.allocate_livingspace_room(p)
                    print(Fore.GREEN + "Successfully allocated", p.get_full_name(), "to",
                          lv_room.get_name() + Style.RESET_ALL)
                except utilities.RoomFullError as e:
                    print(Fore.RED + "Error allocating", p.get_full_name(), "room\n ", e, Style.RESET_ALL)
    except IndexError as e:
        print(Fore.RED + "Error allocating room.\n", e, Style.RESET_ALL)


def reallocate_person(args):
    """
    Reallocates a Person to a Room with name `new_room_name`
    """
    name = args['<first_name>'].strip().title() + " " + args['<last_name>'].strip().title()
    room_name = args['<new_room_name>']
    try:
        main_amity.reallocate_person(name, room_name)
        print(Fore.GREEN, "Successfully reallocated", name, "to", room_name, Style.RESET_ALL)
    except ValueError as e:
        print(Fore.RED, "Error found while reallocating room\nThe room", e, Style.RESET_ALL)
    except utilities.InvalidRoomOccupantError as e:
        print(Fore.RED, "Error found while reallocating person!")
        print(name, "cannot be reallocated to", room_name, Style.RESET_ALL)
    except utilities.RoomFullError as e:
        print(Fore.RED, "Error found while reallocating person!")
        print(room_name, "is already full! Please try with another room or remove some people there", Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED, "Error found while reallocating person.\n", e, Style.RESET_ALL,
              "\nType help to view all commands")


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
        print(Fore.RED, "Error processing data!")
        print("The data file contains invalid data. Also check for incorrect formatting.", Style.RESET_ALL)


def load_people(args):
    """
    Adds people to rooms from a txt file.
    """
    file_path = args['FILE']
    if not os.path.isfile(file_path):
        print(Fore.RED, "Error reading file...")
        print("The file path provided does not exist", Style.RESET_ALL)
        return

    with open(file_path, encoding='utf-8') as data_file:
        line_no = 0
        for line in data_file:
            args = _get_line_data(line.strip())
            line_no += 1
            if args:
                add_person(args)
            else:
                print(Fore.MAGENTA, "Skipping line ", line_no, Style.RESET_ALL)
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
        print(Fore.RED, "There exists no allocations at the moment. Please make some room allocations first.",
              Style.RESET_ALL)
        return
    data = tabulate(allocations, headers='keys', tablefmt='fancy_grid')
    if args['-o'] and args['FILE']:
        with open(args['FILE'], encoding='utf-8', mode='w') as output_file:
            output_file.write(data)
            print(Fore.GREEN, "Successfully wrote room allocations to the file", args['FILE'], Style.RESET_ALL)
    elif not args['-o'] and not args['FILE']:
        print(data)
    else:
        print(Fore.RED, "Invalid syntax.", Style.RESET_ALL)
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
        print(Fore.RED, "There exists no unallocated people at the moment.", Style.RESET_ALL)
        return
    data = tabulate({'Unallocated People': unallocated}, headers='keys', tablefmt='fancy_grid')

    if args['-o'] and args['FILE']:
        with open(args['FILE'], encoding='utf-8', mode='w') as output_file:
            output_file.write(data)
            print(Fore.GREEN, "Successfully wrote list of unallocated persons to the file", args['FILE'],
                  Style.RESET_ALL)
    elif not args['-o'] and not args['FILE']:
        print(data)
    else:
        print(Fore.RED, "Invalid syntax.", Style.RESET_ALL)
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
            print(Fore.RED, "{} is currently empty. Please allocate or reallocate people here.".format(room.get_name()),
                  Style.RESET_ALL)
            return
        data = {room.get_name() + " occupants:": room_occupants}
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
    except ValueError:
        print(Fore.RED, "The room {} doesn't exist. You could create it. Please type help to view all "
              "commands.".format(args['<room_name>']), Style.RESET_ALL)


def save_state(args):
    """
    Persists all the data stored in the app to a SQLite database.
    """
    db_file = args['--db'] if args['--db'] else "amity_db"

    try:
        db.save_state(main_amity, db_file)
        print(Fore.GREEN, "Successfully saved Amity state to ", db_file, "sqlite database", Style.RESET_ALL)
    except sqlite3.Error as e:
        print(Fore.RED, "Error found when saving state.\n ", e)
        print("Please try again.", Style.RESET_ALL)


def load_state(args):
    db_path = args['<sqlite_database>']
    if not os.path.isfile(db_path):
        print(Fore.RED, "Error reading database file...")
        print("The file path provided does not exist", Style.RESET_ALL)
        return
    file_type = str(subprocess.check_output(('file', db_path)), 'utf-8').strip()
    if 'sqlite' not in file_type.lower():
        print(Fore.RED, os.path.abspath(db_path), "is not a valid Sqlite database. Please use a valid database",
              Style.RESET_ALL)
        return
    else:
        state = db.load_state(db_path)
        main_amity.all_rooms, main_amity.all_persons = state
        print(Fore.GREEN, "Successfully loaded state from", os.path.abspath(db_path), Style.RESET_ALL)


def list_rooms(args):
    """
    Prints to screen all rooms in Amity
    """
    all_rooms = [r.get_name() for r in main_amity.all_rooms]
    if not all_rooms:
        print(Fore.RED, "There exists no room at Amity. You could create some. Type help to view all commands.",
              Style.RESET_ALL)
        return
    data = tabulate({'Amity Rooms': all_rooms}, headers='keys',
                    tablefmt='fancy_grid')
    print(data)


def quit(args):
    """
    Exits the application
    """
    print(Fore.RED, Style.BRIGHT, "\nExiting Amity application", Style.RESET_ALL)
    sys.exit()
