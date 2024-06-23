import fire
from env import session, clear
from models import Dj
from styling import error_message, success_message, subheading_two

def delete_dj():
    clear()
    subheading_two("Current DJs:")
    djs = session.query(Dj).all()
    for dj in djs:
        print(dj.name)

    dj_name = input("Enter the name of the DJ you want to delete: ").strip().lower()
    dj = session.query(Dj).filter(Dj.name.ilike(dj_name)).first()
    if dj:
        session.delete(dj)
        session.commit()
        success_message(f"DJ {dj.name} has been successfully deleted.")
    else:
        error_message(f"DJ with name '{dj_name}' not found.")

def main():
    fire.Fire(delete_dj)

if __name__ == "__main__":
    main()
