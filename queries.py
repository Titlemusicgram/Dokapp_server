from database import session_factory


def add_object_to_db(obj):
    with session_factory() as session:
        session.add(obj)
        session.commit()
