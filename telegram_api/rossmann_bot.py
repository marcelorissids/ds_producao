import requests
import json
import pandas as pd


def load_dataset(store_id):
    # Test dataset
    df10 = pd.read_csv('/home/marcelo/repos_cds/ds_producao/data/raw/test.csv')
    df_store_raw = pd.read_csv('/home/marcelo/repos_cds/ds_producao/data/raw/store.csv')

    # Merging test + store dataset
    df_test = pd.merge(df10, df_store_raw, how='left', on='Store')

    # Choosing only one store for prediction test
    df_test = df_test[df_test['Store'] == store_id]

    # Removing closed days
    df_test = df_test[df_test['Open'] != 0]
    df_test = df_test[~df_test['Open'].isnull()]
    df_test = df_test.drop('Id', axis=1)

    # Converting dataframe to json
    data = json.dumps(df_test.to_dict(orient='records'))

    return data

def predict(data):

    # API Call
    url = 'https://webapp-rossmann-8290.onrender.com/rossmann/predict'
    header = {'Content-type': 'application/json'}
    data = data

    r = requests.post(url, data=data, headers=header)
    print('Status Code {}'.format(r.status_code))

    d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())

    return d1

# d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()

# for x in range(len(d2)):
#    print('Store number {} will sell ${:,.2f} in the next 6 weeks'.format(
#           d2.loc[x, 'store'],
#           d2.loc[x, 'prediction']))
    
