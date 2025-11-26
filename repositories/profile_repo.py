from db.mongodb import get_profiles_collection


def get_profiles_collection_ref():
    return get_profiles_collection()
