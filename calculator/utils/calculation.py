import datetime
import pandas as pd
import numpy as np

def check_year_inclusion(date, date_type):

    today = pd.Timestamp.today().date()
    current_month_day = (today.month, today.day)

    if date_type == 'file date':
        comparison_month_day = (date.month, date.day)
    elif date_type == 'publication date':
        comparison_month_day = (date.month, date.day)
    else:
        raise ValueError(f"Invalid date type: {date_type}. Expected 'file' or 'publication'.")

    include_current_year = comparison_month_day > current_month_day

    return include_current_year

def post_process_fees(results_df):
    today = pd.Timestamp.today().date()
    current_year = today.year

    for index, row in results_df.iterrows():
        filing_date = row['File Date']
        issued_date = row['Publication Date']
        date_type = row['Date Type'] 

        if date_type == "none":
            continue

        date_to_check = issued_date if date_type == 'publication date' else filing_date

        include_current_year = check_year_inclusion(date_to_check, date_type)
        if not include_current_year:
            column_name = str(current_year)
            if column_name in results_df.columns:
                results_df.at[index, column_name] = np.nan

    return results_df

def date_check(patent, date_types, fees_info, results_df, index):
    patent_number, type, filing_date, issued_date, expiration_date, country, numofclaims = patent
    date_type = date_types.get(patent_number, '').lower()

    if type.lower() != "grant":
        date_type = "none"
    if date_type == "none":
        for year in range(datetime.date.today().year, expiration_date.year + 1):
            results_df.at[index, str(year)] = 0
        results_df.at[index, 'Date Type'] = "none"
        return results_df
    if date_type == 'publication date':
        fees_by_year = calculate_fees_issued_date(patent, fees_info)
    elif date_type == 'file date':
        fees_by_year = calculate_fees_filing_date(patent, fees_info)
    else:
        return results_df 

    for year, fee in fees_by_year:
        if year >= datetime.date.today().year:
            results_df.at[index, str(year)] = fee

    results_df.at[index, 'Date Type'] = date_type

    return results_df



######################## FOR PATENTS WHICH CALCULATE FROM FILING DATE ########################

def calculate_fees_issued_date(patent_info, fees_info):

    patent_number, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info

    print(f"Calculating issued date fees for patent {patent_number} in country {country}")

    if country not in fees_info.columns or (country == 'JP' and 'JPPC' not in fees_info.columns):
        print(f"Warning: Fees data for country code {country} or JPPC not found. Skipping this patent.")
        return []

    country_fees = fees_info[country].dropna().values 
    print(f"Country fees for {country}: {country_fees}")

    if country == 'US':
        return calculate_fees_us(patent_info, country_fees)
    elif country == 'JP':
        fees_per_claim = fees_info['JPPC'].dropna().values
        print(f"Fees per claim for JP: {fees_per_claim}")
        return calculate_fees_jp(patent_info, country_fees, fees_per_claim)
    elif country == 'KR':
        fees_per_claim = fees_info['KRPC'].dropna().values
        print(f"Fees per claim for KR: {fees_per_claim}")
        return calculate_fees_kr(patent_info, country_fees, fees_per_claim)
    elif country == 'ID':
        fees_per_claim = fees_info['IDPC'].dropna().values
        print(f"Fees per claim for ID: {fees_per_claim}")
        return calculate_fees_id(patent_info, country_fees, fees_per_claim)
    elif country == 'TW':
        return calculate_fees_tw(patent_info, country_fees)
    elif country == 'RU':
        return calculate_fees_ru(patent_info, country_fees)
    elif country == 'MY':
        return calculate_fees_my(patent_info, country_fees)
    elif country == 'SK':
        return calculate_fees_sk(patent_info, country_fees)
    else:
        print(f"Warning: Unsupported country code for issued date calculation: {country}. Skipping this patent.")
        return []
    
def calculate_fees_us(patent_info, country_fees):

    _, _, _, issued_date, expiration_date, _, _ = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year)
    end_year = expiration_date.year

    fees_by_year = []

    country_fees = country_fees[2:]

    for year in range(start_year, end_year):
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] if not pd.isna(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year
    

def calculate_fees_filing_date(patent_info, fees_info):

    patent_number, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info

    today = datetime.date.today()
    start_year = max(today.year, filing_date.year)
    remaining_years = expiration_date.year - start_year
    
    if country not in fees_info.columns:
        print(f"Warning: Fees data for country code {country} not found. Skipping this patent.")
        return []

    country_fees = fees_info[country].fillna(0).values
    
    if remaining_years > len(country_fees):
        print(f"Warning: Not enough fee data available for country code {country}. Skipping this patent.")
        return []

    selected_fees = country_fees[-remaining_years:]
    
    fees_by_year = [(start_year + i, fee) for i, fee in enumerate(selected_fees)]

    return fees_by_year

 ################### FOR PATENTS CALCULATING FROM PUBLICATION/ISSUED DATE ###################
def calculate_fees_jp(patent_info, country_fees, fees_per_claim):

    _, _, _, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year)
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)
    fees_per_claim = np.nan_to_num(np.array(fees_per_claim[2:], dtype=float), nan=0.0)

    fees_by_year = []
    
    initial_fees = sum(country_fees[:3]) + numofclaims * sum(fees_per_claim[:3])
    fees_by_year.append((issued_date.year, initial_fees))

    for year in range(start_year, end_year):
        if year == issued_date.year:
            continue 
        if year < issued_date.year + 3:
            fees_by_year.append((year, '0'))
            continue
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] + numofclaims * fees_per_claim[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year

def calculate_fees_kr(patent_info, country_fees, fees_per_claim):

    _, _, _, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year)
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)
    fees_per_claim = np.nan_to_num(np.array(fees_per_claim[2:], dtype=float), nan=0.0)

    fees_by_year = []

    initial_fees = sum(country_fees[:3]) + numofclaims * sum(fees_per_claim[:3])
    fees_by_year.append((issued_date.year, initial_fees))

    for year in range(start_year, end_year):
        if year == issued_date.year:
            continue 
        if year < issued_date.year + 3:
            fees_by_year.append((year, '0'))
            continue
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] + numofclaims * fees_per_claim[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year

def calculate_fees_id(patent_info, country_fees, fees_per_claim):
   
    _, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year + 1)
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)
    fees_per_claim = np.nan_to_num(np.array(fees_per_claim[2:], dtype=float), nan=0.0)

    fees_by_year = []

    initial_fees = sum(country_fees[:issued_date.year - filing_date.year]) + numofclaims * sum(fees_per_claim[:issued_date.year - filing_date.year])
    fees_by_year.append((issued_date.year, initial_fees))
    
    for year in range(start_year, end_year):
        year_index = year - (filing_date.year)
        if 0 <= year_index < len(country_fees):
            fee = country_fees[year_index] + numofclaims * fees_per_claim[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year

def calculate_fees_tw(patent_info, country_fees):
 
    _, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year)
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)

    fees_by_year = []
    
    for year in range(start_year, end_year):
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year


def calculate_fees_ru(patent_info, country_fees):
   
    _, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year)
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)

    fees_by_year = []

    for year in range(start_year, end_year):
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year

def calculate_fees_my(patent_info, country_fees):
   
    _, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year) 
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)

    fees_by_year = []

    for year in range(start_year, end_year):
        year_index = year - issued_date.year
        if year_index < len(country_fees):
            fee = country_fees[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year


def calculate_fees_sk(patent_info, country_fees, fees_per_claim):
 
    _, priority_date, filing_date, issued_date, expiration_date, country, numofclaims = patent_info
    today = datetime.date.today()
    start_year = max(today.year, issued_date.year + 1) 
    end_year = expiration_date.year

    country_fees = np.nan_to_num(np.array(country_fees[2:], dtype=float), nan=0.0)
    fees_per_claim = np.nan_to_num(np.array(fees_per_claim[2:], dtype=float), nan=0.0)

    fees_by_year = []

    initial_fees = sum(country_fees[:issued_date.year - filing_date.year])
    fees_by_year.append((issued_date.year, initial_fees))
    
    for year in range(start_year, end_year):
        year_index = year - (filing_date.year)
        if 0 <= year_index < len(country_fees):
            fee = country_fees[year_index] if not np.isnan(country_fees[year_index]) else 0
        else:
            fee = 0
        fees_by_year.append((year, fee))

    return fees_by_year
