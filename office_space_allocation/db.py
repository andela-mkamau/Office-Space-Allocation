import sqlite3
import pickle


def save_state(amity, sqlite_db):
    """
    Saves the current state of Amity to the sqlite_db

    :param: amity: Amity system
    :param: sqlite_db: A sqlite3 database to persist state to
    """
    state = (amity.all_rooms, amity.all_persons)
    state_bytes = pickle.dumps(state)
    state_bin = sqlite3.Binary(state_bytes)

    conn = sqlite3.connect(sqlite_db)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS State")
        cur.execute("CREATE TABLE State(Data BLOB)")
        cur.execute("INSERT INTO TABLE State(Data) VALUES (?)", (state_bin,))
