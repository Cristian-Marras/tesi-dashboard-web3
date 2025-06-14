# Dashboard di Analytics a supporto di applicazioni basate su Web3

Progetto di tesi triennale in Informatica per la Comunicazione Digitale (Università degli Studi di Milano), focalizzato sulla creazione di una dashboard di analytics per marketplace di NFT.

---

## 🎯 Obiettivo del Progetto

Lo scopo del progetto è lo sviluppo di una Dashboard a supporto dell'analisi delle transazioni e dello scambio di NFT in diversi marketplace.
Come caso d'uso, la dashboard analizza un dataset pubblico le cui transazioni sono state pre-elaborate e modellate attraverso una rappresentazione a grafo dalla collega tesista che si è occupata del backend.
A partire da essa è stata realizzata una dashboard pensata per analizzare i pattern di utilizzo dei principali elementi del sistema, come wallet, collezioni e bilancio degli account.

## 🏗️ Architettura del Progetto e Mio Contributo

Il sistema è suddiviso in due componenti principali:

1.  **Backend & Data Layer (sviluppato da un'altra tesista):** Un sistema responsabile della raccolta dati, della loro elaborazione e dell'esposizione tramite un'API dedicata (realizzata con **FastAPI**).

2.  **Frontend - Dashboard di Analytics (il mio contributo):** Un'applicazione web sviluppata interamente da me in **Python** e **Streamlit**. 
    * Durante lo sviluppo, la connessione al backend avveniva in modo sicuro tramite un **tunnel SSH** stabilito su una rete privata virtuale (**OpenVPN Connect**).
    * L'applicazione consuma i dati forniti dall'API e li presenta attraverso un'interfaccia grafica interattiva e user-friendly.

Il mio lavoro ha quindi riguardato la **progettazione della UI/UX**, lo **sviluppo di tutte le componenti interattive** (grafici, tabelle, filtri, navigazione), e l'**ottimizzazione delle performance** del frontend.

## 🛠️ Strumenti e Tecnologie

* **Linguaggio:** Python
* **Framework Web App:** Streamlit
* **Manipolazione Dati:** Pandas, NumPy
* **Data Visualization:** Plotly (per grafici interattivi)

## 🚀 Galleria di funzionalità

Questa sezione illustra le principali feature implementate nella dashboard.

### 1. Ricerca Intelligente e Panoramica Collezione

Per facilitare l'esplorazione, è stata implementata una barra di ricerca con funzione di autocompletamento. Una volta selezionata una collezione, la dashboard presenta una scheda riassuntiva con le sue informazioni principali.

![Ricerca collezione e informazioni principali](https://github.com/user-attachments/assets/cd2e15ea-c8bf-44a8-aac1-b1b3829d05f4)

![image](https://github.com/user-attachments/assets/c8672c6a-5682-412f-93e2-2bcea6358a58)

### 2. Analisi Temporale Dinamica

La dashboard offre grafici interattivi (realizzati con Plotly) per analizzare l'andamento delle transazioni nel tempo. Una feature chiave è il **ricampionamento dinamico** della frequenza temporale (giornaliera, settimanale, mensile), ottimizzato grazie alla **cache interna di Streamlit (`@st.cache`)** per garantire performance elevate senza ricaricare i dati.

![transazioni collezione](https://github.com/user-attachments/assets/66f825cb-5049-4f93-b38b-8f02d48683a9)

![transazioni collezione ricampionate](https://github.com/user-attachments/assets/5cf0e1eb-887a-4c01-944a-d59ec7f9baf5)

### 3. Esplorazione del singolo NFT

Per consentire un'analisi granulare, un menù a tendina interattivo (`st.selectbox`) permette di selezionare un singolo NFT all'interno della collezione. Da qui, l'utente può navigare direttamente alle pagine di analisi dei **wallet del creatore o dell'ultimo proprietario**, creando un percorso di esplorazione dei dati fluido e interconnesso.

![NFt selezionato](https://github.com/user-attachments/assets/8c972acc-2c0a-4fdd-8f07-26d239589c83)

### 4. Esplorazione dei Wallet e delle Transazioni

Una volta navigato a una pagina Wallet, l'interfaccia utilizza le **Streamlit Tabs** (`st.tabs`) per organizzare l'enorme quantità di informazioni in sezioni navigabili: Profilo, Acquisti, Vendite, e NFT Posseduti & Guadagni. Questo garantisce un'esperienza utente pulita e permette di analizzare nel dettaglio la storia finanziaria e operativa di ogni attore del sistema.

![Barra di navigazione](https://github.com/user-attachments/assets/bc6cf317-d9cc-4aa9-a962-3f00737455d6)

### 5. Riepilogo Finanziario e Asset del Wallet

Le schede finali forniscono un riepilogo finanziario cruciale. Vengono presentate in tabelle chiare e ordinate le transazioni di acquisto e vendita, gli NFT attualmente posseduti e, soprattutto, i **guadagni netti** realizzati dal wallet, sintetizzando la performance economica dell'account.

![NFT acquistati](https://github.com/user-attachments/assets/950cbae4-a492-4394-bcae-33fd90462fb9)

![transazioni di acquisto](https://github.com/user-attachments/assets/051c5379-8016-47b7-96be-449957caae47)

![guadagni](https://github.com/user-attachments/assets/2e9f991c-7a39-43e5-8fe0-142e7a70c093)

## ⚠️ Nota sulla Eseguibilità

Per motivi di privacy e dipendenza da API private dell'ambiente di ricerca universitario, il codice in questo repository non è direttamente eseguibile. Il progetto viene qui presentato attraverso la documentazione e gli screenshot a scopo di portfolio.

## 📄 Documentazione Completa

Per un'analisi approfondita della metodologia e dei risultati, sono disponibili la tesi completa e le slide di presentazione.

* **[Scarica la Tesi di Laurea (PDF)](./Tesi.pdf)**
* **[Scarica le Slide della Presentazione (PDF)](./Presentazione_tesi.pdf)**

## 📧 Contatti

* **LinkedIn:** [Cristian Marras](https://www.linkedin.com/in/cristian-marras-151932186)
* **Email:** cristianmarrasj@gmail.com








