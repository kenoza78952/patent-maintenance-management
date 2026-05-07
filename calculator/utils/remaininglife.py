import datetime

def calculate_remaining_life(patent_info):
    today = datetime.date.today()

    updated_patent_info = []

    for patent in patent_info:
        patent_number, priority_date, filing_date, issued_date, expiration_date, country, numofclaims, execution_year = patent
        
        remaining_life = (expiration_date - today).days / 365.25
        rounded_remaining_life = round(remaining_life + 0.5)

        updated_patent_info.append(patent + (rounded_remaining_life,))

    return updated_patent_info
