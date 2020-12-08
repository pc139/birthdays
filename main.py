#! /usr/bin/env python3

import argparse
import dbmanager as db
from weather_fun import def_min_max_day

# PAY ATTENTION WHEN CHANGING PATHS!
db_path = 'data/database.db'


def parse_arguments(currencies, companies):
    parser = argparse.ArgumentParser(
            description="Process ticker symbol and currency",
            prog="stock_info",
            usage="%(prog)s [options]",
            epilog="Using financialmodelingprep API")
    parser.add_argument("-v", help="Be more verbose", action="store_true")

    # check username and password
    parser.add_argument('-u', help="add a username name (requires -p)",
                        required=True)
    parser.add_argument('-p', help="the username password",
                        required=True)
    parser.add_argument('-a', help="the user api",
                        required=True)
    parser.add_argument('-c1', help="the city",
                        required=True)
    parser.add_argument('-c2', help="the country",
                        required=True)
    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s 1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # open the connection and (IF NECESSARY) create the users table
    db.open_and_create(db_path)
    # If the user is authenticated proceed:
    if db.check_for_username(args.u, args.p):

        def_min_max_day(args.c1, args.c2)
    else:
        print("Username does not exist or password is incorrect!")