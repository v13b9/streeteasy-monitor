class Database:
    def __init__(self, config):
        self.supabase = config.setup_supabase()

    def get_existing_ids(self):
        listings_data = self.supabase.table('listings').select('*').execute().data
        return set([listing['listing_id'] for listing in listings_data])

    def get_listings_sorted(self):
        response = (
            self.supabase.table('listings')
            .select('*')
            .order('created_at', desc=True)
            .execute()
        )
        return response.data

    def insert_new_listing(self, listing):
        self.supabase.table('listings').insert(listing).execute()
