import os
from django.conf import settings
from .exceptions import InvalidCountryCodeError

def locate_country_code_in_fees(patent_info, fees_info):
    date_types = {}

    for patent in patent_info:
        patent_number, _, _, _, _, country, _ = patent

        if country in fees_info.columns:
            fees_for_country = fees_info[country]
            date_type = fees_for_country.iloc[0] 
            date_types[patent_number] = date_type
        else:
            date_types[patent_number] = "none"
            print(f"Warning: Country code {country} not found in fees data for patent {patent_number}. Setting date type to 'non existent'.")

    return date_types
