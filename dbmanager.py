import sqlite3
import random
import hashlib
import argparse
import os

conn = None
cursor = None

def open_and_create(db_path):
    """Connect to the database
    :return: no value
    :rtype: none
    """

    global conn
    global cursor

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
    # if the table does not exist create one
    except sqlite3.OperationalError:
        create_users_table(conn, cursor)

def create_users_table():
    """Create the users' table if it does not exist
    :return: no value
    :rtype: none
    """

    global conn
    global cursor
    # Create table
    cursor.execute('''CREATE TABLE users
                   (username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) NOT NULL,
                    salt SMALLINT NOT NULL,
                    PRIMARY KEY (username))''')

def save_new_username(username, password,api_key):
    """Save a new user in the users table
    :param username: the username
    :type username: string
    :param password: the password
    :type password: string
    :return: no value
    :rtype: none
    """

    global conn
    global cursor
    salt = random.randint(1, 10000)
    password = str(salt) + password
    digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # if the user already exists, replace its password and salt
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?,?,?,?)",
                   (username, digest, api_key, salt))
    conn.commit()

def remove_username(username):
    """Remove a user from the users table
    :param username: the username
    :type username: string
    :return: no value
    :rtype: none
    """
    global conn
    global cursor
    # the username is the primary key
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()

def check_for_username(username, password):
    """Check the credentials of a user
    The user provided his credentials for authentication. If the user exists
    in the db, the SHA256(salt+password) is computed. If the digest of the
    password provided by the user is the same as the digest computed as above,
    the user is authenticated and the action is allowed.
    :param username: the username provided by the user for the authentication
    :param password: the password provided by the user for the authentication
    :return: True if the user can be authenticated, False otherwise.
    :rtype: Boolean
    """

    global conn
    global cursor
    rows = cursor.execute("SELECT * FROM users WHERE username=?",
                          (username,))
    conn.commit()
    results = rows.fetchall()
    # get the salt and prepend to the password before computing the digest
    password = str(results[0][3]) + password
    digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # if the digest in the database is equal to the computed digest ALLOW
    if digest == results[0][1].lower():
        return results[0][2]
    else:
        return False

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Manage possible database actions (add/remove user)",
            prog="stock_info",
            usage="%(prog)s [options]",
            epilog="Using SQLite3")
    # command to add users
    parser.add_argument("-add", required=False, default=False,
                        help="Add username '-u' with password '-p' (Bool) and api key '-a'",
                        action="store_true")
    # command to remove users
    parser.add_argument("-rm", required=False, default=False,
                        help="Remove username '-u' with password '-p' (Bool)",
                        action="store_true")
    # user credentials
    parser.add_argument('-u', help="add a username name (requires -p)",
                        required=True, default=None)
    parser.add_argument('-p', help="the username password",
                        required=False, default=None)
    parser.add_argument('-a', help="the user api key",
                        required=False, default=None)

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s 1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    path = os.path.abspath(os.path.join(os.getcwd(),
                                        'data/database.db'))
    open_and_create(path)
    args = parse_arguments()
    # if the users wants to add and remove a user at the same time DENY
    if args.add and args.rm:
        print("You cannot add and remove a user at the same time!")
    elif args.add:
        # if there is one argument missing (username, password or both) DENY
        if args.u is None or args.p is None:
            print("Please provide a proper username and password combination!")
        else:
            save_new_username(args.u, args.p, args.a)
            print("Successfully inserted user {}".format(args.u))
    elif args.rm:
        remove_username(args.u)
        print("Successfully removed user {}".format(args.u))
    else:
        print("Please choose -add to add a user or -rm to remove a user!")






