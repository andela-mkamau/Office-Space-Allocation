#!/usr/bin/env python
"""
Office Space allocation

Usage:
     osa.py create_room (office | livingspace) <room_name>...
     osa.py add_person <first_name> <last_name> <title> [<wants_accommodation>]
     osa.py reallocate_person <first_name> <last_name> <new_room_name>
     osa.py load_people -i FILE
     osa.py print_allocations [-o FILE]
     osa.py print_unallocated [-o FILE]
     osa.py print_room <room_name>
     osa.py save_state [--db=SQLITE_DATABASE]
     osa.py load_state <sqlite_database>
     osa.py [-i | --interactive]

Options:

"""

import cmd
import sys
from docopt import docopt, DocoptExit
from office_space_allocation import main
from office_space_allocation import utilities

# Thanks to
# https://github.com/docopt/docopt/blob/master/examples/interactive_example.py


def docopt_cmd(sub_cmd):
    """
    Passes the results of docopt parsing to a sub_cmd
    """

    def fn(self, args):
        try:
            opts = docopt(fn.__doc__, args)
        except DocoptExit as e:
            print("Invalid Command")
            print(e)
            return
        return sub_cmd(self, opts)

    fn.__name__ = sub_cmd.__name__
    fn.__doc__ = sub_cmd.__doc__
    fn.__dict__.update(sub_cmd.__dict__)
    return fn


class InteractiveOSA(cmd.Cmd):

    intro = "Office Space Allocations\n(type help to view all commands)"
    prompt = "(amity >>> ) "
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """
        Creates rooms in Amity by specifying room type and multiple room names

        Usage:
            create_room (office | livingspace) <room_name>...

        """
        main.create_room(args)

    @docopt_cmd
    def do_add_person(self, args):
        """
        Adds a person to the system and allocates the Person to a random Room.

        Usage:
            add_person <first_name> <last_name> <title> [<wants_accommodation>]

        """
        main.add_person(args)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """
        Reallocates a Person to a Room with name `new_room_name`

        Usage:
            reallocate_person <first_name> <last_name> <new_room_name>

        """
        # TODO : Refactor to allow for a fuzzy search
        main.reallocate_person(args)

    @docopt_cmd
    def do_load_people(self, args):
        """
        Adds people to rooms from a txt file.

        Usage:
            load_people -i FILE

        """
        print(args)
        main.load_people(args)

    @docopt_cmd
    def do_print_allocations(self, args):
        """
        Prints a list of allocations onto the screen.
        Specifying the optional -o option here outputs the registered
        allocations to a txt file

        Usage:
            print_allocations [-o FILE]

        """
        main.print_allocations(args)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """
        Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file
        provided.

        Usage:
            print_unallocated [-o FILE]

        """
        main.print_unallocated(args)

    @docopt_cmd
    def do_print_room(self, args):
        """
        Prints the names of all the people in  room_name  on the screen.

        Usage:
           print_room <room_name>

        """
        main.print_room(args)

    @docopt_cmd
    def do_save_state(self, args):
        """
        Persists all the data stored in the app to a SQLite database.

        Specifying the  --db  parameter explicitly stores the data in the 
        sqlite_database  specified.

        Usage:
           save_state [--db=SQLITE_DATABASE]

        """
        main.save_state(args)

    @docopt_cmd
    def do_load_state(self, args):
        """
        Loads data from a database into the application.

        Usage:
           load_state <sqlite_database>

        """
        main.load_state(args)


opts = docopt(__doc__, sys.argv[1:])

if opts['--interactive'] or opts['-i']:
    InteractiveOSA().cmdloop()

print(opts)
