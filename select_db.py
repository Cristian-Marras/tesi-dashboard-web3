from datetime import datetime
import streamlit as st
import httpx
import requests
from streamlit_searchbox import st_searchbox
import pandas as pd
import plotly.express as px
from items.api_calls import (RESAMPLING_MAP, get_collection, 
    get_collection_transactions, get_nft_transactions, 
    get_nft_from_collection, get_collection_summary, get_nft_summary, 
    get_transactions_from_wallet, get_wallet_summary,
    format_date
)

# comment multiple lines: shift + alt + a

#Caricamento iniziale dei dati
@st.cache_data
def load_collections():
    return get_collection()

# Controlla se i dati sono già stati caricati
if 'collections' not in st.session_state:
    collections = load_collections()  # Carica i dati dalla API
    st.session_state.collections = collections  # Memorizza in session_state per riutilizzarli
else:
    collections = st.session_state.collections  # Usa i dati già memorizzati

##### RICERCA COLLECTION CON AUTOCOMPLETAMENTO #####

# La lista delle collezioni è direttamente in collections["collections"]
collection_list = collections["collections"]
# Funzione per fornire suggerimenti per l'autocompletamento
def search_callback(query):
    return [collection for collection in collection_list if query.lower() in collection.lower()]
# Usa st_searchbox per l'autocompletamento
selected_collection = st_searchbox(
    search_callback,
    key="searchbox",
    label="Cerca una collezione",
    clear_on_submit=True
)

def show_summary(collection_name):
    data = get_collection_summary(collection_name)
    st.metric(label =  "Collezione selezionata", value = collection_name)
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "NFT totali", value = data['total_nfts'])
    col2.metric(label = "Transazioni totali", value = data['total_transaction'])
    col3.metric(label = "Valore", value = "$" + str(round(data['value'], 2)))
    return data

@st.fragment
def show_nft_summary(nft_name):
    data = get_nft_summary(nft_name)
    st.session_state["nft_summary"] = data
    c1, c2 = st.columns(2)
    c1.metric(label = "Wallet del creatore:", value = data['creator_wallet'])

    if c2.button(label = "Vai al wallet"):
        wallet_summary = get_wallet_summary(data['creator_wallet'].strip('"'))
        st.session_state["wallet_summary"] = wallet_summary
        st.session_state["wallet_id"] = data['creator_wallet']
        st.switch_page("items/wallet.py")
    
    co1, co2 = st.columns(2)
    co1.metric(label = "Ultimo compratore:", value = data['last_buyer'])
    if co2.button(label = "Vai al wallet", key="2"):
        wallet_summary = get_wallet_summary(data['last_buyer'].strip('"'))
        st.session_state["wallet_summary"] = wallet_summary
        st.session_state["wallet_id"] = data['last_buyer']
        st.switch_page("items/wallet.py")

    col1, col2 = st.columns(2)
    col1.metric(label = "Prima transazione", value = format_date(data['first_transaction']))
    col2.metric(label = "Ultima transazione", value = format_date(data['last_transaction']))
    st.metric(label = "Numero di transazioni", value = data['number_of_transaction'])

    return data


def get_collection_transaction_and_graph(selected_collection, min_date, max_date):
    resampling = st.selectbox(
        "Seleziona la frequenza di campionamento:",
        list(RESAMPLING_MAP.keys()),
        index=1,  # Default: "giornaliero"
        key="resampling"
    )
    if "original_df" not in st.session_state:
        data = get_collection_transactions(selected_collection, min_date, max_date, 'D')
        df = pd.DataFrame(list(data.items()), columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        st.session_state["original_df"] = df

    # AGGIUNGERE CONTROLLO PERCHé AL PRIMO RUN SESSION è VUOTO E Dà ERRORE

    df = st.session_state["original_df"].resample(RESAMPLING_MAP[resampling]).sum()
    fig = px.line(df, x=df.index, y='value', title="Transazioni")
    st.plotly_chart(fig)


def get_nft_transactions_and_graph(selected_nft, min_date, max_date):
    resampling = st.selectbox(
        "Seleziona la frequenza di campionamento:",
        list(RESAMPLING_MAP.keys()),
        index=1,  # Default: "giornaliero"
        key="resampling_select"
    )
    if "nft_df" not in st.session_state:
        data = get_nft_transactions(selected_nft, min_date, max_date, 'D')
        df = pd.DataFrame(list(data.items()), columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        st.session_state["nft_df"] = df

    df = st.session_state["nft_df"].resample(RESAMPLING_MAP[resampling]).sum()
    fig = px.line(df, x=df.index, y='value', title="Transazioni")
    st.plotly_chart(fig)


# Controlla se una collezione valida è stata selezionata
if selected_collection and selected_collection != "Seleziona una collezione":
    data = show_summary(selected_collection)
    get_collection_transaction_and_graph(selected_collection, data['min_date'], data['max_date'])

    nfts = get_nft_from_collection(selected_collection) # lista nfts

    if nfts:
        st.divider()
        selected_nft = st.selectbox("Seleziona un NFT:", nfts)
        st.session_state.pop("nft_df", None)
        st.session_state.pop("wallet_df", None)
        st.metric(label = "NFT selezionato", value = selected_nft)
        nft_data = show_nft_summary(selected_nft)
        get_nft_transactions_and_graph(selected_nft, nft_data['first_transaction'], nft_data['last_transaction'])





    
