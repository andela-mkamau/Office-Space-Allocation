# Office Space Allocator

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

 * `create_room (office | livingspace) <room_name>...`

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



