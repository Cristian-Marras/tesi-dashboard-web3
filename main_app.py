import streamlit as st
import pandas as pd
import asyncio
import httpx

pg = st.navigation(
    {
        '' : [
            st.Page("items/select_db.py", title = "Home", icon = ":material/contacts:"),
        ],
        '-' : [
            st.Page("items/wallet.py", title = "Wallet", icon = ":material/cards:"),
        ],
    }
)
pg.run()