import pandas as pd

def add_total_fees_per_patent(results_df):
    
    year_columns = [col for col in results_df.columns if col.isdigit()]
    
    results_df[year_columns] = results_df[year_columns].apply(pd.to_numeric, errors='coerce')
    
    results_df['Total Fees'] = results_df[year_columns].fillna(0).sum(axis=1)

    return results_df



def calculate_grand_total(results_df):
    
    grand_total = results_df['Total Fees'].sum()

    grand_total_row = [''] * (results_df.shape[1] - 1) + [grand_total]

    results_df.loc[len(results_df)] = grand_total_row
    
    return results_df
