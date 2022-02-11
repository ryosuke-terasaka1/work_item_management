import streamlit as st
import datetime 
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['create_users', 'update_users', 'create_items', 'update_items'])

if page == 'create_users':
    st.title('ユーザー登録画面')
    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        username: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            # 'user_id': user_id,
            'username': username
        }
        submit_button = st.form_submit_button(label='ユーザー登録')

    if submit_button:
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('ユーザー登録完了')
        st.json(res.json())

elif page == 'update_items':
    url_items = 'http://127.0.0.1:8000/items'
    # url_items = 'https://ghuuab.deta.dev/items'
    res = requests.get(url_items)
    items = res.json()
    items_name = {}
    for item in items:
        items_name[item['item_name']] = {
            'item_id': item['item_id'],
            'capacity': item['capacity']
        }
    
    st.write('### 商品一覧')
    df_items = pd.DataFrame(items)
    df_items.columns = ['商品名', '定員', '商品ID']
    df_items['アップデート'] = st.button('update')
    st.table(df_items)

elif page == 'create_items':
    st.title('商品登録画面')

    with st.form(key='item'):
        # item_id: int = random.randint(0, 10)
        item_name: str = st.text_input('商品名', max_chars=12)
        created_date: datetime.datetime = st.number_input('作成日', step=1)
        data = {
            # 'item_id': item_id,
            'item_name': item_name,
            'created_date': created_date
        }
        submit_button = st.form_submit_button(label='商品登録')

    if submit_button:
        url = 'http://127.0.0.1:8000/items'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('商品登録完了')
        st.json(res.json())
