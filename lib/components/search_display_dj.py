from sqlalchemy import func
from env import session, os
from models import Dj, Genre, Subgenre, Venue, DjGenre, DjSubgenre, DjVenue
from styling import heading, clear

# display dj for search function
def display_dj_details(dj):
    while True:
        clear()
        heading(f"{dj.name}:")
        print(f"1. View all of {dj.name}'s details")
        print(f"2. View genres and subgenres that {dj.name} plays")
        print(f"3. View venues {dj.name} has played at")
        print(f"4. View {dj.name}'s Production Status")
        print(f"5. Update {dj.name}'s details")
        print("6. Return to Main Menu")
        choice = input("Please select an option: ")

        if choice == "1":
            clear()
            heading(f"{dj.name}'s Full Details")
            print(f"Producer: {'Yes' if dj.produces else 'No'}\n")

            print("Genres and Subgenres:")
            for genre in dj.genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).join(DjSubgenre).filter(
                    DjSubgenre.dj_id == dj.id,
                    Subgenre.genre_id == genre.id
                ).all()
                for subgenre in subgenres:
                    print(f"  - {subgenre.subtitle}")

            print("\nVenues:")
            for venue in dj.venues:
                print(f"- {venue.venuename}")

            input("\nPress Enter to return to the previous menu. ")  

        elif choice == "2":
            clear()
            heading(f"{dj.name}'s Genres and Subgenres")
            for genre in dj.genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).join(DjSubgenre).filter(
                    DjSubgenre.dj_id == dj.id,
                    Subgenre.genre_id == genre.id
                ).all()
                for subgenre in subgenres:
                    print(f"  - {subgenre.subtitle}")
            input("\nPress Enter to return to the previous menu. ")      

        elif choice == "3":
            clear()
            heading(f"Venues that {dj.name} has played at")
            for venue in dj.venues:
                print(f"- {venue.venuename}")

            input("\nPress Enter to return to the previous menu. ")  

        elif choice == "4":
            clear()
            heading(f"{dj.name}'s producer status")
            print(f"Producer: {'Y' if dj.produces else 'N'}\n")
            input("\nPress Enter to return to the previous menu. ")

        elif choice == "5":
            pass

        elif choice == "6":
            return
        
        else:
            print("Invalid input, please enter an option from the menu.")

# search for a DJ via name function
def search_dj():
    clear()
    heading("SEARCH FOR A DJ")
    dj_name = input("Enter DJ name: ")
    dj = session.query(Dj).filter(func.lower(Dj.name) == dj_name.lower()).first()

    if dj:
        display_dj_details(dj)
    else:
        print(f"No DJ found with the name {dj_name}")
        while True:
            choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").lower()
            if choice in ["yes", "y", "ys"]:
                search_dj()
                return
            elif choice in ["no", "n"]:
                return
            else:
                print("Invalid input, please enter Yes/Y or No/N")
