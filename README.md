# Office Space Allocator
[![Build Status](https://travis-ci.org/andela-mkamau/Office-Space-Allocation.svg?branch=develop)](https://travis-ci.org/andela-mkamau/Office-Space-Allocation)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2251a775f5db4c41803844d2f093f24d)](https://www.codacy.com/app/michael-kamau/Office-Space-Allocation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-mkamau/Office-Space-Allocation&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/2251a775f5db4c41803844d2f093f24d)](https://www.codacy.com/app/michael-kamau/Office-Space-Allocation?utm_source=github.com&utm_medium=referral&utm_content=andela-mkamau/Office-Space-Allocation&utm_campaign=Badge_Coverage)
## Introduction

Office Space Allocator is Python powered command line application that
is used to make room allocations in a facility called Amity.

Office Space Allocator has the following features:

* Creation of room of type `office` or `livingspace`
* Addition of persons to the system. Persons can be of type `fellow` or `staff`
* Random allocation of rooms to persons in the system. Fellows can be allocated
either type or room. Staff can only be allocated rooms of type `livingspace`
* Reallocation of persons to new rooms
* Loading of people data from text files
* Listing of existing room allocations on screen or in text file.
* Listing of unallocated persons on screen or in text file
* Listing of persons allocated a specific room on screen
* Listing of all rooms on screen
* Saving of application state to a sqlite database
* Loading of application state from a sqlite database

## Installation

Office Space Allocator is developed and tested on Python 3. The recommended
version is Python 3.5.2. Using your package manager or binaries from the
official [Python language website](https://www.python.org/downloads/),
install Python 3 first.

Follow the following steps to have the system running:

* Clone this repo:
 - Using HTTPS:
 ```
 git clone https://github.com/andela-mkamau/Office-Space-Allocation.git
 ```
 - Using SSH:
 ```
 git clone git@github.com:andela-mkamau/Office-Space-Allocation.git
 ```

* Navigate to the application directory:

```
cd Office-Space-Allocation
```

* I strongly recommend creation of a a virtual environment to install the
application in. You could install virtualenv or virtualenvwrapper.
Within your virtual environment, install the application package dependencies with:

```
pip install -r requirements.txt
```

* Run the application with:

```
python osa.py -i
```

## Using Office Space Allocator

Office Space Allocator is run in an interactive mode. Functionality is
 accessed via commands. Below is a description of all the commands
 currently supported.

*  `create_room (office | livingspace) <room_name>...`

    This create a room or a list of rooms whose type can either be `office` or
 `livingspace`.
   For instance, a session to create two office rooms would be as follows:
   
     ```
    (amity >>> ) create_room office Snow Hogwats
    Successfully created office room: Snow
    Successfully created office room: Hogwats
     ```
    To create three Livingspace rooms:

    ```
    (amity >>> ) create_room livingspace Kitchen Python Php
    Successfully created livingspace room: Kitchen
    Successfully created livingspace room: Python
    Successfully created livingspace room: Php
    ```
    
    **NOTE: You cannot create rooms with the same name**. Am sure you do want to
create confusion among your users. Neither do I.

    ```
    (amity >>> ) create_room livingspace Kitchen
    Kitchen already exists in Amity. Cannot create duplicate room!
    ```

* `add_person <first_name> <last_name> <title> [<wants_accommodation>]`

  Adds a person to the system and allocates the person to a random room. 
`wants_accommodation` is an optional argument which can be either  `Y`  or  `N`. 
The default value if it is not provided is  `N`. You could type a `yes` or `no` too.

  Below is a sample session:
  ```
  (amity >>> ) add_person joshua kimani fellow yes
  Successfully added Joshua Kimani to Amity.
  Successfully allocated Joshua Kimani to Python
  ```

* `reallocate_person <first_name> <last_name> <new_room_name>`

   This reallocates a Person to a Room with name `new_room_name`.
In the event that the operation is not successful -- new room is non-existent or
 is full -- an error message is displayed explaining the failure.
 
  Below is a sample session:
  ```
  (amity >>> ) reallocate_person Joshua Kimani snow
   Successfully reallocated Joshua Kimani to snow
  ```
  
* `load_people -i FILE`

    This adds people to rooms from a file provided. It is assumed that the file is a text
    file.
    Each line in the file must be in the form suitable for the command `add_person`.
    Any line that has an incorrect format is skipped.
    
    Below is a sample session. 
    
    The input file is called `data.txt` and contains the 
    following data:
    ```
    OLUWAFEMI SULE FELLOW Y
    DOMINIC WALTERS STAFF
    SIMON PATTERSON FELLOW Y
    MARI LAWRENCE FELLOW Y
    LEIGH RILEY STAFF
    TANA LOPEZ FELLOW Y
    ```
   Using the `load_people` command:
    ```
    (amity >>> ) load_people -i data.txt
    Successfully added Oluwafemi Sule to Amity.
    Successfully allocated Oluwafemi Sule to Python
    Successfully added Dominic Walters to Amity.
    Successfully added Simon Patterson to Amity.
    Successfully allocated Simon Patterson to Hogwats
    Successfully added Mari Lawrence to Amity.
    Successfully allocated Mari Lawrence to Snow
    Successfully added Leigh Riley to Amity.
    Successfully added Tana Lopez to Amity.
    Successfully allocated Tana Lopez to Snow
    ```
* `print_allocations [-o FILE]`

    Prints a list of current room allocations onto the screen
Specifying the optional -o option here outputs the registered allocations to a text 
file.  

    Below is a sample session where two rooms called Snoe and Oculus exist in the 
    system:
    ```
    (amity >>> ) print_allocations
    ╒═════════════════╤════════════════╕
    │ Snoe            │ Oculus         │
    ╞═════════════════╪════════════════╡
    │ Simon Patterson │ Oluwafemi Sule │
    ├─────────────────┼────────────────┤
    │ Tana Lopez      │ Mari Lawrence  │
    ╘═════════════════╧════════════════╛
    ```

* `print_unallocated [-o FILE]`

   Prints a list of unallocated people to the screen.
Specifying the optional -o option here outputs list of to a text file. 

    Below is a sample session:

    ```
    (amity >>> ) print_unallocated
    ╒══════════════════════╕
    │ Unallocated People   │
    ╞══════════════════════╡
    │ Dominic Walters      │
    ├──────────────────────┤
    │ Leigh Riley          │
    ╘══════════════════════╛
    ```
* `print_room <room_name>`

   Prints the names of all the people in a room with name `room_name` on the screen.
   
   Below is a sample session:
   ```
   (amity >>> ) print_room oculus
    ╒═════════════════════╕
    │ Oculus occupants:   │
    ╞═════════════════════╡
    │ Oluwafemi Sule      │
    ├─────────────────────┤
    │ Mari Lawrence       │ 
    ╘═════════════════════╛

   ```

* `save_state [--db=SQLITE_DATABASE]`

    Persists all the data stored in the app to a SQLite database.

    Specifying the  --db  parameter explicitly stores the data in the 
    sqlite_database specified. Otherwise, the data is stored in default database
    called `amity_db`
    
    Below is a sample session:
    ```
    (amity >>> ) save_state --db store_db
    Successfully saved Amity state to  store_db sqlite database
    ```
* `load_state <sqlite_database>`

    Loads application state from the specified database into 
    the application.
    
    The database file provided must be a valid sqlite3 database.
    
    Below is a sample session:
    
    ```
    (amity >>> ) load_state store_db
    Successfully loaded state from store_db
    ```
* `quit`

    This exits the application.

* `list_rooms`

    Prints the all rooms in the system on the screen.
    
    Below is a sample session:
    
    ```
    (amity >>> ) list_rooms
    ╒═══════════════╕
    │ Amity Rooms   │
    ╞═══════════════╡
    │ Snoe          │
    ├───────────────┤
    │ Oculus        │
    ╘═══════════════╛
    ```
    
See the video below to get a compelete picture of how to use Office
Room Allocator:


