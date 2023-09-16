# country_codes
from pygal.maps.world import COUNTRIES

def get_country_code(country_name):
    # return a 2 digit code for the given country

    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
        # if not found
        return None