# Import the necessary functions
from excel_utils import read_patent_data, extract_patent_info
from fees_reader import read_fees_data
from locate import locate_country_code_in_fees
from remaininglife import calculate_remaining_life
from total import add_total_fees_per_patent, calculate_grand_total
from overview import create_overview_sheet, format_dates_and_currency
from calculation import calculate_fees_filing_date, calculate_fees_issued_date, post_process_fees
import datetime as datetime
import pandas as pd

def main():
    input_file_path = 'C:/Users/Eric/Desktop/input.xlsx'
    fees_file_path = 'C:/Users/Eric/Desktop/FeesDollars.xlsx'
    output_file_path = 'C:/Users/Eric/Desktop/outputASDASDASDASD.xlsx'

    full_patent_df, patent_df = read_patent_data(input_file_path)

    print("Full Patent DataFrame (Unaltered):")
    print(full_patent_df)
    print()

    print("Processed Patent DataFrame:")
    print(patent_df)
    print()

    patent_info = extract_patent_info(patent_df)

    fees_info = read_fees_data(fees_file_path)
    print("Extracted Fees Information:")
    print(fees_info)
    print()
    date_types = locate_country_code_in_fees(patent_info, fees_info)

    results_df = patent_df.copy()
    results_df['Date Type'] = None

    for i, patent in enumerate(patent_info):
        try:
            patent_number = patent[0]
            date_type = date_types[patent_number].lower()
            
            if date_type == 'issued date':
                fees_by_year = calculate_fees_issued_date(patent, fees_info)
            elif date_type == 'filing date':
                fees_by_year = calculate_fees_filing_date(patent, fees_info)
            else:
                raise ValueError(f"Unsupported date type: {date_type}")

            for year, fee in fees_by_year:
                if year >= datetime.date.today().year:
                    results_df.at[i, str(year)] = fee

            results_df.at[i, 'Date Type'] = date_type

        except ValueError as e:
            print(f"Error calculating fees for Patent {patent[0]}: {e}")
            print("----------------------------------------------------------------")

    results_df = post_process_fees(results_df)

    results_df = add_total_fees_per_patent(results_df)
    
    results_df = calculate_grand_total(results_df)

    results_df = results_df.drop(columns=['Date Type'])
    
    output_columns = [
        'Patent / Publication Number', 
        'Country Code', 
        'Priority Date', 
        'Filing Date', 
        'Issued Date', 
        'Expiration Date', 
        'Number of Claims'
    ] + [col for col in results_df.columns if col.isdigit() or col in ['Total Fees', 'Grand Total']]
    
    output_df = results_df[output_columns]

    output_df.to_excel(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")

    create_overview_sheet(output_file_path)

    format_dates_and_currency(output_file_path)
    
    print("Full Input DataFrame after Calculations:")
    print(full_patent_df)

if __name__ == "__main__":
    main()
