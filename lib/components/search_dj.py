from sqlalchemy import func
from env import session, os
from lib import styling
from models import Dj
from styling import heading
from components import display_dj_details, clear

# search for a DJ via name function
def search_dj():
    clear()
    heading("SEARCH FOR A DJ")
    dj_name = input("Enter DJ name: ")
    dj = session.query(Dj).filter(func.lower(Dj.name) == dj_name.lower()).first()

    if dj:
        display_dj_details(dj)
    else:
        print(f"No Dj found with the name {dj_name}")
        while True:
            choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").lower()
            if choice in ["yes", "y", "ys"]:
                break
            elif choice in ["no", "n"]:
                return
            else:
                print("Invalid input, please enter Yes/Y or No/N")
