from config import session
from models import Genre, Subgenre, Dj, Venue, DjGenre, DjSubgenre, DjVenue

djs_data = [
    {"name": "Stackpackers", "produces": True, "genres": ["Drum & Bass", "Psytrance"], "subgenres": ["Jump Up", "Dancefloor", "Liquid", "Hi-Tech"], "venues": ["Max Watts", "Sub Club", "Laundry"]},
    {"name": "MELTA", "produces": False, "genres": ["Drum & Bass", "UKG"], "subgenres": ["Minimal Rollers"], "venues": ["Max Watts", "Laundry"]},
    {"name": "Rex The Bard", "produces": True, "genres": ["Drum & Bass"], "subgenres": ["Dancefloor"], "venues": ["Laundry"]}
]

genres_data = [
    {"title": "Drum & Bass"},
    {"title": "House"},
    {"title": "UKG"},
    {"title": "Psytrance"},
    {"title": "Techno"},
    {"title": "Dubstep/140"}
]

subgenres_data = [
    {"title": "Jump Up", "genre": "Drum & Bass"},
    {"title": "Dancefloor", "genre": "Drum & Bass"},
    {"title": "Minimal Rollers", "genre": "Drum & Bass"},
    {"title": "Liquid", "genre": "Drum & Bass"},
    {"title": "Hi-Tech", "genre": "Psytrance"},
    {"title": "Melodic Techno", "genre": "Techno"},
    {"title": "Bassline", "genre": "UKG"},
    {"title": "Bass House", "genre": "House"},
    {"title": "G House", "genre": "House"},
    {"title": "Tech House", "genre": "House"},
    {"title": "Tearout", "genre": "Dubstep/140"},
    {"title": "Brostep", "genre": "Dubstep/140"}
]

venues_data = [
    {"venuename": "Max Watts"},
    {"venuename": "170 Russel St"},
    {"venuename": "Sub Club"},
    {"venuename": "Laundry"}
]

def create_djs(djs):
    for dj in djs:
        new_dj = Dj(name=dj["name"], produces=dj["produces"])
        session.add(new_dj)
    session.commit()

def create_genres(genres):
    for genre in genres:
        new_genre = Genre(**genre)
        session.add(new_genre)
    session.commit()

def create_subgenres(subgenres):
    genres = {genre.title: genre for genre in session.query(Genre).all()}
    for subgenre in subgenres:
        genre = genres.get(subgenre['genre'])
        new_subgenre = Subgenre(subtitle=subgenre['title'], genre_id=genre.id)
        session.add(new_subgenre)
    session.commit()

def create_venues(venues):
    for venue in venues:
        new_venue = Venue(**venue)
        session.add(new_venue)
    session.commit()

def create_dj_genres(djs):
    djs_in_db = {dj.name: dj for dj in session.query(Dj).all()}
    genres_in_db = {genre.title: genre for genre in session.query(Genre).all()}
    
    for dj_data in djs:
        dj = djs_in_db.get(dj_data["name"])
        for genre_title in dj_data.get("genres", []):
            genre = genres_in_db.get(genre_title)
            if genre:
                dj_genre = DjGenre(dj_id=dj.id, genre_id=genre.id)
                session.add(dj_genre)
    session.commit()

def create_dj_subgenres(djs):
    djs_in_db = {dj.name: dj for dj in session.query(Dj).all()}
    subgenres_in_db = {subgenre.subtitle: subgenre for subgenre in session.query(Subgenre).all()}
    
    for dj_data in djs:
        dj = djs_in_db.get(dj_data["name"])
        for subgenre_title in dj_data.get("subgenres", []):
            subgenre = subgenres_in_db.get(subgenre_title)
            if subgenre:
                dj_subgenre = DjSubgenre(dj_id=dj.id, subgenre_id=subgenre.id)
                session.add(dj_subgenre)
    session.commit()

def create_dj_venues(djs):
    djs_in_db = {dj.name: dj for dj in session.query(Dj).all()}
    venues_in_db = {venue.venuename: venue for venue in session.query(Venue).all()}
    
    for dj_data in djs:
        dj = djs_in_db.get(dj_data["name"])
        for venue_name in dj_data.get("venues", []):
            venue = venues_in_db.get(venue_name)
            if venue:
                dj_venue = DjVenue(dj_id=dj.id, venue_id=venue.id)
                session.add(dj_venue)
    session.commit()

def delete_all():
    session.query(DjVenue).delete()
    session.query(DjSubgenre).delete()
    session.query(DjGenre).delete()
    session.query(Dj).delete()
    session.query(Subgenre).delete()
    session.query(Genre).delete()
    session.query(Venue).delete()
    session.commit()

if __name__ == "__main__":
    delete_all()

    create_genres(genres_data)
    create_subgenres(subgenres_data)
    create_venues(venues_data)
    create_djs(djs_data)
    create_dj_genres(djs_data)
    create_dj_subgenres(djs_data)
    create_dj_venues(djs_data)

    print("Seeding complete...")
