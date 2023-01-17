import os
import pandas as pd
from data_config import Colconfig

def get_data(target=None):
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dls_els_share.parquet')
    raw_data = pd.read_parquet(data_path)

    if target == 'DLS':
        dls_data = raw_data.loc[:, Colconfig.date_cols + \
            [Colconfig.company_col, Colconfig.bal_col] + Colconfig.dls_bal + Colconfig.dls_cnt]
        return dls_data
    elif target == 'ELS':
        els_data = raw_data.loc[:, Colconfig.date_cols + \
            [Colconfig.company_col, Colconfig.bal_col] + Colconfig.els_bal + Colconfig.els_cnt]
        return els_data
    
    return raw_data

if __name__ == '__main__':
    print('start processing')
    # col_catalist = pd.read_csv('발행잔액_catal.csv', delimiter='!')
    col_catalist = pd.read_parquet('scrap_data_col_korean_name.parquet')
    print(col_catalist)
    # col_catalist.to_parquet('scrap_data_col_korean_name.parquet', index=False)