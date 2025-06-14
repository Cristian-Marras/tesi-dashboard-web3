import logging
import requests
import httpx
import streamlit as st
from datetime import datetime

BASE_URL = "http://localhost:10010/api"

RESAMPLING_MAP = {
    "orario": "h",
    "giornaliero": "D",
    "settimanale": "W",
    "mensile": "ME"
}

def format_date(iso_date):
    dt = datetime.fromisoformat(iso_date)
    return dt.strftime("%d/%m/%Y %H:%M:%S")

def handle_request_error(response):
    #Gestione degli errori HTTP per le chiamate API
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        logging.error(f"Errore HTTP {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        logging.error(f"Errore di connessione: {e}")
    except Exception as e:
        logging.error(f"Errore generico: {e}")
    return None

def get_collection():
    url = f"{BASE_URL}/nft/collections"
    headers = {"accept": "application/json"}
    response = httpx.get(url, headers=headers, timeout=10)
    return handle_request_error(response) or response.json()

def get_collection_transactions(collection_name, start_date, end_date, frequency):
    url = f"{BASE_URL}/collection/transaction_ts"
    params = {
        'collection': collection_name,
        'start_date': start_date,
        'end_date': end_date,
        'sampling_frequency': frequency
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    return handle_request_error(response) or response.json()


def get_collection_summary(collection_name):
    url = f"{BASE_URL}/collection/summary"
    params = {'collection': collection_name}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_nft_transactions(nft_id, start_date, end_date, frequency):
    url = f"{BASE_URL}/nft/transactions_ts"
    params = {
        'nft_id': nft_id,
        'start_date': start_date,
        'end_date': end_date,
        'sampling_frequency': frequency
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    return handle_request_error(response) or response.json()

def get_nft_summary(nft_name):
    url = f"{BASE_URL}/nft/summary"
    params = {'nft': nft_name}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()    

def get_nft_from_collection(collection_name):
    url = f"{BASE_URL}/collection/nfts"
    params = {'collection': collection_name}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_transactions_from_wallet(wallet, start_date, end_date, sampling_frequency):
    url = f"{BASE_URL}/wallet/transactions_ts"
    params = {
        'wallet_id': wallet,
        'start_date': start_date,
        'end_date': end_date,
        'sampling_frequency': sampling_frequency
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_summary(wallet):
    url = f"{BASE_URL}/wallet/summary"
    params = {'wallet_id': wallet}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_purchase(wallet, start_date, end_date):
    url = f"{BASE_URL}/wallet/purchase"
    params = {'wallet_id': wallet,
              'start_date': start_date,
              'end_date': end_date}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()


def get_wallet_purchase_transactions(wallet, start_date, end_date, sampling_frequency):
    url = f"{BASE_URL}/wallet/purchase_ts"
    params = {'wallet_id': wallet,
              'start_date': start_date,
              'end_date': end_date,
              'sampling_frequency': sampling_frequency}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_sales(wallet, start_date, end_date):
    url = f"{BASE_URL}/wallet/sales"
    params = {'wallet_id': wallet,
              'start_date': start_date,
              'end_date': end_date}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_sales_transactions(wallet, start_date, end_date, sampling_frequency):
    url = f"{BASE_URL}/wallet/sales_ts"
    params = {'wallet_id': wallet,
              'start_date': start_date,
              'end_date': end_date,
              'sampling_frequency': sampling_frequency}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_owned_nfts(wallet, end_date):
    url = f"{BASE_URL}/wallet/own"
    params = {'wallet_id': wallet,
              'end_date': end_date}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

def get_wallet_nfts_gain(wallet, end_date):
    url = f"{BASE_URL}/wallet/gain"
    params = {'wallet_id': wallet,
              'end_date': end_date}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    return handle_request_error(response) or response.json()

