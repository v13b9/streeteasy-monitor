from .config import setup_supabase

supabase = setup_supabase()


def get_existing_ids():
    listings_data = supabase.table('listings').select('*').execute().data
    return [listing['listing_id'] for listing in listings_data]


def get_listings_sorted():
    response = supabase.table('listings').select('*').order('created_at', desc=True).execute()
    return response.data


def insert_new_listing(listing):
    supabase.table('listings').insert(listing).execute()
