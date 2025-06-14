import streamlit as st
import pandas as pd
import plotly.express as px
from items.api_calls import (RESAMPLING_MAP, get_wallet_summary, get_transactions_from_wallet,
    get_wallet_purchase, get_wallet_purchase_transactions,
    get_wallet_sales, get_wallet_sales_transactions,
    format_date, get_wallet_owned_nfts, get_wallet_nfts_gain,
    get_nft_summary
)
# Creazione delle tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dettagli del wallet", "Acquisti", "Vendite", "NFT Posseduti & Guadagni"])

wallet_id = st.session_state["wallet_id"]
#st.write(st.session_state['wallet_summary'])
wallet_summary = st.session_state["wallet_summary"]
#nft_summary = st.session_state["nft_summary"]


def show_wallet_transaction():
    resampling = st.selectbox(
        "Seleziona la frequenza di campionamento:",
        list(RESAMPLING_MAP.keys()),
        index=1,  # Default: "giornaliero"
        key="resampling_wallet"
    )
    if "wallet_df" not in st.session_state:
        wallet_data = get_transactions_from_wallet(wallet_id, wallet_summary['first_buy_date'], wallet_summary['last_sell_date'], "D")
        #st.write(wallet_data)
        df = pd.DataFrame(list(wallet_data.items()), columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        st.session_state["wallet_df"] = df
    df = st.session_state["wallet_df"].resample(RESAMPLING_MAP[resampling]).sum()
    fig = px.line(df, x=df.index, y='value', title="Transazioni del wallet")
    st.plotly_chart(fig)

@st.fragment
def show_purchase_transaction():
    resampling = st.selectbox(
        "Seleziona la frequenza di campionamento:",
        list(RESAMPLING_MAP.keys()),
        index=1,  # Default: "giornaliero"
        key="resampling_purchase"
    )
    if "wallet_purchase_df" not in st.session_state:
        wallet_purchase_data = get_wallet_purchase_transactions(wallet_id, wallet_summary['first_buy_date'], wallet_summary['last_sell_date'], "D")        
        all_purchases = wallet_purchase_data["numero NFT acquistati"]
        #st.write("Ecco i dati grezzi:", all_purchases)
        df = pd.DataFrame(all_purchases)
        # Converte 'date' e imposta come indice
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').sort_index()
        # Salva nello stato della sessione
        st.session_state["wallet_purchase_df"] = df
        #st.write("DataFrame finale:", df)
    df = st.session_state["wallet_purchase_df"].resample(RESAMPLING_MAP[resampling]).sum()
    fig = px.line(df, x=df.index, y='nft_count', title="Transazioni di acquisto")
    st.plotly_chart(fig)

@st.fragment
def show_sales_transaction():
    resampling = st.selectbox(
        "Seleziona la frequenza di campionamento:",
        list(RESAMPLING_MAP.keys()),
        index=1,  # Default: "giornaliero"
        key="resampling_sales"
    )
    if "wallet_sales_df" not in st.session_state:
        wallet_sales_data = get_wallet_sales_transactions(wallet_id, wallet_summary['first_buy_date'], wallet_summary['last_sell_date'], "D")
        all_sales = wallet_sales_data["numero NFT venduti"]
        df = pd.DataFrame(all_sales)
        # Converte 'date' e imposta come indice
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').sort_index()
        # Salva nello stato della sessione
        st.session_state["wallet_sales_df"] = df
        #st.write("DataFrame finale:", df)
    df = st.session_state["wallet_sales_df"].resample(RESAMPLING_MAP[resampling]).sum()
    fig = px.line(df, x=df.index, y='nft_count', title="Transazioni di vendita")
    st.plotly_chart(fig)

# mostra lista degli acquisti
def show_purchase_list():
    wallet_purchase_list = get_wallet_purchase(wallet_id, wallet_summary['first_buy_date'], wallet_summary['last_sell_date'])
    selected_nft = st.selectbox("NFT acquistati:", wallet_purchase_list['NFT acquistati'])
    return selected_nft

# mostra lista delle vendite
def show_sales_list():
    wallet_sales_list = get_wallet_sales(wallet_id, wallet_summary['first_buy_date'], wallet_summary['last_sell_date'])
    selected_nft = st.selectbox("NFT venduti:", wallet_sales_list['NFT venduti'])
    return selected_nft

#@st.fragment
def show_owned_nfts():
    wallet_owned_nfts = get_wallet_owned_nfts(wallet_id, wallet_summary['last_sell_date'])
    selected_nft = st.selectbox("NFT attualmente posseduti:", wallet_owned_nfts['NFT posseduti'])
    return selected_nft

@st.cache_data
def show_wallet_nfts_gain():
    wallet_gain = get_wallet_nfts_gain(wallet_id, wallet_summary['last_sell_date'])
    #st.write(wallet_gain)
    dati = []
    for value in wallet_gain["NFT - Prezzo d'acquisto - Prezzo di vendita - Guadagno"]:
        valori = value.split(",")  # Separiamo gli elementi
        nft, prezzo_acquisto, prezzo_vendita, guadagno = valori
        prezzo_acquisto = f"${round(float(prezzo_acquisto), 2):.2f}"
        prezzo_vendita = f"${round(float(prezzo_vendita), 2):.2f}"
        guadagno = f"${round(float(guadagno), 2):.2f}"
        dati.append([nft.strip(), prezzo_acquisto, prezzo_vendita, guadagno])
    df = pd.DataFrame(dati, columns=["NFT", "Prezzo Acquisto", "Prezzo Vendita", "Guadagno"])
    st.dataframe(df)

def show_nft_summary(nft_name, key1, key2):
    data = get_nft_summary(nft_name)
    st.session_state["nft_summary"] = data
    c1, c2 = st.columns(2)
    c1.metric(label = "Wallet del creatore:", value = data['creator_wallet'])
    if c2.button(label = "Vai al wallet", key=key1):
        wallet_summary = get_wallet_summary(data['creator_wallet'].strip('"'))
        st.session_state["wallet_summary"] = wallet_summary
        st.session_state["wallet_id"] = data['creator_wallet']
        st.switch_page("items/wallet.py")
    co1, co2 = st.columns(2)
    co1.metric(label = "Ultimo compratore:", value = data['last_buyer'])
    if co2.button(label = "Vai al wallet", key=key2):
        wallet_summary = get_wallet_summary(data['last_buyer'].strip('"'))
        st.session_state["wallet_summary"] = wallet_summary
        st.session_state["wallet_id"] = data['last_buyer']
        st.switch_page("items/wallet.py")
    col1, col2 = st.columns(2)
    col1.metric(label = "Prima transazione", value = format_date(data['first_transaction']))
    col2.metric(label = "Ultima transazione", value = format_date(data['last_transaction']))
    st.metric(label = "Numero di transazioni", value = data['number_of_transaction'])
    return data

#
# === Fragment che ricarica solo la selezione NFT ===
@st.fragment
def nft_selection_and_summary():
    st.header("📌 Lista degli NFT attualmente posseduti") 
    selected_owned_nft = show_owned_nfts()
    show_nft_summary(selected_owned_nft, 5, 6)
#
#

if wallet_summary['first_buy_date'] != "":
    with tab1: 
        st.title("👛 Dettagli del wallet")
        st.metric(label ="Wallet ID:", value = st.session_state["wallet_id"])
        co1, co2 = st.columns(2)
        co1.metric(label = "Primo acquisto", value = format_date(wallet_summary['first_buy_date']))
        co2.metric(label = "Ultima vendita", value = format_date(wallet_summary['last_sell_date']))
        c1, c2 = st.columns(2)
        c1.metric(label = "Transazioni d'acquisto totali", value = wallet_summary['total_buy_transactions'])
        c2.metric(label = "Acquisti totali", value = "$" + str(round(wallet_summary['total_buy'], 2)))
        col1, col2 = st.columns(2)
        col1.metric(label = "Transazioni di vendita totali", value = wallet_summary['total_sell_transactions'])
        col2.metric(label = "Vendite totali", value = "$" + str(round(wallet_summary['total_sell'], 2)))
        show_wallet_transaction()

    with tab2:
        st.header("📌 Acquisti")
        st.subheader("NFT acquistati")
        selected_purchase_nft = show_purchase_list()
        show_nft_summary(selected_purchase_nft, 1,2)
        st.subheader("Transazioni di acquisto")
        show_purchase_transaction()

    with tab3:
        st.header("📌 Vendite")
        st.subheader("NFT venduti")
        selected_sell_nft = show_sales_list()
        show_nft_summary(selected_sell_nft, 3,4)
        st.subheader("Transazioni di vendita")
        show_sales_transaction()

    with tab4:
        """ st.header("📌 Lista degli NFT attualmente posseduti")
        selected_owned_nft = show_owned_nfts()
        show_nft_summary(selected_owned_nft, 5,6)
        st.header("📌 Guadagni")
        show_wallet_nfts_gain() """

        # Questo è il blocco che si aggiorna se cambia la selectbox
        nft_selection_and_summary()

        st.header("📌 Guadagni")
        show_wallet_nfts_gain()

    #st.header("📌 Dettagli NFT selezionato")
    #show_nft_summary(selected_owned_nft, 5, 6)

else:
    st.markdown(f"<h3>Il wallet</h3><h3>{st.session_state['wallet_id']}</h3><h3>non ha transazioni</h3>", unsafe_allow_html=True)
