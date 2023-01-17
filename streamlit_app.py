import os
import pandas as pd

import market_share_data
import streamlit as st

st.set_page_config(page_title='Market Share'
                        , page_icon=":shark:"
                        , layout='wide')

@st.experimental_memo
def get_data_cache(target):
    data = market_share_data.get_data(target)
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '발행잔액_catal.csv')
    col_catalist = pd.read_csv(data_path, delimiter='!')

    return data, col_catalist

@st.experimental_memo
def get_company_data(tmp_data, company_name = '한국투자증권'):
    com_data = tmp_data[tmp_data.loc[:, 'repSecnNm'] == company_name]
    com_data.reset_index(drop=True, inplace=True)
    com_data.loc[:, 'date_month_key'] = com_data.date.dt.strftime('%Y%m').astype('float')
    com_month_stat = com_data.groupby('date_month_key').sum().applymap(int)
    com_month_stat.index = com_month_stat.index.astype('str')
    
    return com_data, com_month_stat

def set_colname_to_korean(data, col_catalist):
    tmp_data = pd.merge(pd.DataFrame(data.columns, columns=['항목명(영문)_tmp']), col_catalist
         , how='left', left_on='항목명(영문)_tmp', right_on='항목명(영문)')
    tmp_idx = tmp_data[tmp_data.loc[:, '항목명(국문)'].isnull()].index
    tmp_data.loc[tmp_idx, '항목명(국문)'] = tmp_data.loc[tmp_idx, '항목명(영문)_tmp']
    data.columns = tmp_data.loc[:, '항목명(국문)'].tolist()
    
    return data

if __name__ == '__main__':

    st.sidebar.header('Menu')
    genrre = st.sidebar.radio('DLS or ELS', ('DLS', 'ELS'))
    show_company = st.sidebar.selectbox(
    "증권사:", (['한국투자증권', 'NH투자증권', '현대차증권', '한화투자증권', '하이투자증권', '하나증권'
                    , '키움증권', '유진투자증권', '유안타증권', '아이비케이투자증권', '신한투자증권', '케이비증권'
                    , '삼성증권', '신영증권', '교보증권', '노무라금융투자', '다올투자증권', '대신증권', 'SK증권', '메리츠증권'
                    , '미래에셋증권', '비엔케이투자증권', '디비금융투자'])
    )

    dls_data, col_catalist = get_data_cache(genrre)
    kis_data, kis_month_stat = get_company_data(dls_data, company_name = show_company)

    # stroke_width = st.sidebar.slider("시작 월: ", 1, 12, 1)

    st.subheader('{} {} 월별 발행잔량'.format(show_company, genrre))
    
    if genrre == 'DLS':
        # st.area_chart(kis_month_stat.balanceSumDls)
        st.bar_chart(kis_month_stat.balanceSumDls)
    else:
        # st.area_chart(kis_month_stat.balanceSumEls)
        st.bar_chart(kis_month_stat.balanceSumEls)

    st.table(set_colname_to_korean(kis_month_stat, col_catalist).style.highlight_max(axis=0).format("{:,.0f}"))
    st.write(' (*) 발행잔량합계 = DLS 발행잔량 + ELS 발행잔량')
    