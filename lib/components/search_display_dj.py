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
        choice = input("Please select an option")

        if choice == "1":
            clear()
            heading(f"{dj.name}'s Full Details")
            print(f"Producer: {'Y' if dj.produces else 'N'}\n")

            print("Genres and Subgenres:")
            genres = dj.genres
            for genre in genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).filter_by(genre_id=genre.id).all()
                for subgenre in subgenres:
                    print(f"  - {subgenre.subtitle}")

            print("\nVenues:")
            venues = [venue.venuename for venue in dj.venues]
            for venue in venues:
                print(f"- {venue}")

            input("\nPress Enter to return to the previous menu. ")  

        elif choice == "2":
            clear()
            heading(f"{dj.name}'s Genres and Subgenres")
            genres = dj.genres
            for genre in genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).filter_by(genre_id=genre.id).all()
                for subgenre in subgenres:
                    print(f" - {subgenre.subtitle}")
            input("\nPress Enter to return to the previous menu. ")      

        elif choice == "3":
            clear()
            heading(f"Venue's that {dj.name} has played at")
            venues = [venue.venuename for venue in dj.venues]
            for venue in venues:
                print(f"- {venue}")

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
        print(f"No Dj found with the name {dj_name}")
        while True:
            choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").lower()
            if choice in ["yes", "y", "ys"]:
                break
            elif choice in ["no", "n"]:
                return
            else:
                print("Invalid input, please enter Yes/Y or No/N")
