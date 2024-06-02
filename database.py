from config import setup_supabase

supabase = setup_supabase()


def get_existing_ids():
    listings_data = supabase.table('listings').select('*').execute().data
    return [listing['listing_id'] for listing in listings_data]


def insert_new_listing(listing):
    supabase.table('listings').insert(listing).execute()
