import environs
env = environs.Env()
env.read_env()

def get_field_values():
    return {
        'message': env('MESSAGE'),
        'phone': env('PHONE'),
        'search_partners': None,
        'email': env('EMAIL'),
        'name': env('NAME'),
    }


def setup_supabase():
    from supabase import create_client

    supabase_url = env('SUPABASE_URL')
    supabase_key = env('SUPABASE_KEY')

    return create_client(supabase_url, supabase_key)