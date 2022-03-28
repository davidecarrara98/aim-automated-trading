import sys
import os
sys.path.append(os.getcwd())

import warnings
warnings.filterwarnings('ignore')

f = open("output/logs.txt","w+")
f.close()
f = open("output/logs.txt", "a") # salveremo tutto l'output stampato a schermo in un file .txt

############################################################################
### Introduzione
############################################################################

# Yahoo Finance consente di avere accesso a dati di mercato rispetto ad un "Ticker", 
# ovvero un codice in grado di identificare un particolare strumento finanziario
# scambiato sui mercati (Stocks, Fixed income, FX, Commodities). 

# Nel nostro caso faremo riferimento ai seguenti 10 tickers, scambiati su 
tickers = ["ENEL.MI", "STLA.MI", "ENI.MI", "ISP.MI", "RACE.MI", "STM.MI", "G.MI", "UCG.MI", "CNHI.MI", "SRG.MI"]

# Per importare in Python questi dati si fa riferimento all'API chiamata yfinance
# Per una guida approfondita (non necessaria per questa challenge), consultare:
# https://pypi.org/project/yfinance/
# https://algotrading101.com/learn/yfinance-guide/

# In particolare attraverso un'istanza di 
# yftk = yfinance.Ticker("ENEL.MI") 
# si possono scaricare i dati storici giornalieri tramite il metodo
# yftk.history(start="2021-01-01", end="2021-12-31", interval="1d")


############################################################################
### Punto 1
############################################################################

# Classes to develop: DataLoader and DataLoaderDict
from auto_trading_aim.data_loader_dict import DataLoaderDict
# from auto_trading_aim.data_loader import DataLoader

# Definizione ed inizializzazione di historical_data, dict-like object di tipo DataLoaderDict
# contenente oggetti di tipo DataLoader, che scarica i dati di mercato relativi ai prezzi di 
# chiusura ("Close") e i volumi ("Volume") per ogni giorno (lavorativo) del 2021 
historical_data = DataLoaderDict(tickers, start="2021-01-01", end="2021-12-31", interval="1d") # scarica i dati
historical_data.save(path = "data/") # salva i dati

# Descrizione testuale dei dati di prezzi e di volumi, con:
# - codice del ticker selezionato, periodo e intervallo
# - minimo, media e massimo raggiunto nel periodo
# - valori al primo e all'ultimo giorno dell'anno
print(historical_data["ENEL.MI"], file=f)

# Descrizione grafica dei dati
historical_data["STLA.MI"].plot("Prices") # esegue un plot dei Prezzi nel tempo
historical_data["ENI.MI"].plot("Volumes") # esegue un plot dei Volumi nel tempo


############################################################################
### Punto 2
############################################################################

# Classes to develop: Asset and Portfolio
from auto_trading_aim.asset import Asset
# from auto_trading_aim.portfolio import Portfolio

# Viene inizializzato portfolio1, un dict-like object di tipo Portfolio di oggetti Asset
# Esempio: portfolio1["ENEL.MI"] sarà un oggetto di tipo Asset
# Asset ha come attributi
# - ticker_name: stringa del nome del ticker
# - prices: pandas dataframe con lo storico del valore
# - mkt_returns: pandas dataframe con i rendimenti semplici
# - volume_owned: numero di azioni possedute di quell'asset

# Il metodo build_portfolio() di DataLoaderDict crea e ritorna un'istanza di oggetto Portfolio
# In questo caso il portafoglio è composto da 4 stock di "ENEL.MI" e 3 di "STLA.MI"
portfolio1 = historical_data.build_portfolio({"ENEL.MI" : 4, "STLA.MI" : 3})

# Si aggiungono al portfolio 2 azioni di "ENI.MI"
portfolio1["ENI.MI"] = Asset(ticker_name = "ENI.MI", prices = historical_data["ENI.MI"].prices, 
                             volume_owned = 2)

# Per il calcolo dei rendimenti semplici giornalieri sui prezzi, in pandas si può usare:
# df.pct_change(1)

# Stampa a schermo: 
# - nome del ticker
# - la quantità di azioni possedute
# - la media e la varianza dei rendimenti del ticker nel periodo
print(portfolio1["ENEL.MI"], file=f)

# Stampa a schermo le informazioni precedenti per ogni asset del portafoglio 
print(portfolio1, file=f)

# Esegue un istogramma dei rendimenti
portfolio1["ENEL.MI"].hist()
    
# NOTA: il valore di un portafoglio deve essere calcolato come la somma delle sue componenti
#       (quindi portfolio1 avrà come valore 4*ENEL+3*STLA+2*ENI ogni giorno)
#       a partire dal valore si calcola nuovamente il rendimento dell'intero portafoglio

# Esegue un istogramma dei rendimenti dell'intero portafoglio e un plot del valore nel tempo
portfolio1.hist()
portfolio1.plot()

# Si costruisce un nuovo portafoglio e lo si somma al portafoglio precedente
# tramite Operator Overloading
# portfolio2 conterrà 2 azioni di ENEL.MI e 9 di ISP.MI
portfolio2 = portfolio1["ENEL.MI"] / 2 + Asset(ticker_name = "ISP.MI", prices = historical_data["ISP.MI"].prices, volume_owned = 9)
portfolio3 = portfolio1 + portfolio2
portfolio3.plot()


############################################################################
### Punto 3
############################################################################

# Class to develop: PortfolioBuilder
from auto_trading_aim.portfolio_builder import PortfolioBuilder

# Implementare un metodo di Portfolio che ritorni un Pandas DataFrame dell'allocazione del 
# portafoglio (1 riga e massimo 10 colonne, una per ogni ticker con le quantità possedute)
allocation1 = portfolio1.to_df()
print(allocation1, file=f)

# Si immagini di avere il seguente capitale iniziale (in €) e lo si impieghi almeno per il 90% 
# per costruire dei portafogli composti dai 10 ticker selezionati
capital = 1000000
min_invest = 0.90

port_build = PortfolioBuilder(capital = capital, data = historical_data, min_invest = min_invest)

# NOTA: per l'esecuzione dei seguenti esercizi si consigliano due approcci
#       - Attraverso la Frontiera del Portafogli https://it.wikipedia.org/wiki/Frontiera_dei_portafogli
#       - Con simulazione casuale di portafogli, prendendo quello che massimizza le informazioni richieste 

# Caso 1: portafoglio a varianza minima dei rendimenti
port_min_var = port_build.min_var()

# Caso 2: portafoglio con rapporto maggiore tra media e deviazione standard dei rendimenti 
port_rate_mean_std = port_build.rate_mean_std()

# Salvare le allocazioni
port_min_var.to_df().to_csv("output/port_min_var.csv")
port_rate_mean_std.to_df().to_csv("output/port_rate_mean_std.csv")


############################################################################
### Punto 4
############################################################################

# Class to develop: DailyPortfolioBuilder
from auto_trading_aim.daily_portfolio_builder import DailyPortfolioBuilder

# Introdurre un oggetto DailyPortfolioBuilder che, per ogni giorno dal 01/07/2021 in poi, 
# costruisca il miglior portafoglio in base alle precedenti metriche
# L'allocazione si dovrà basare solo sulle informazioni precedenti alla data analizzata

daily_port_build = DailyPortfolioBuilder(capital = capital, data = historical_data, 
                                         min_invest = min_invest, start="2021-07-01")

# Salvare in un csv la composizione di portafoglio in modo che:
# - le colonne rappresentino i singoli asset
# - le righe i giorni dell'anno dal 01/07/2021 in poi

# Caso 1: portafoglio a varianza minima dei rendimenti
daily_port_min_var = daily_port_build.min_var(save_path = "output/daily_port_min_var.csv")

# Caso 2: portafoglio con rapporto maggiore tra media e deviazione standard dei rendimenti 
daily_port_rate_mean_std = daily_port_build.rate_mean_std(save_path = "output/daily_port_rate_mean_std.csv")


############################################################################
### Punto 5 - Bonus
############################################################################

# Class to develop: DailyPortfolioBuilderBonus
from auto_trading_aim.daily_portfolio_builder_bonus import DailyPortfolioBuilderBonus

# Ripetere il punto precedente eseguendo una previsione dei rendimenti e basando la composizione
# su quella. [Necessarie basi di Time Series Forecasting]

# Considerare delle fees dello 0.1% nell'acquisto e nella vendita di asset. 
# Ripetere l'allocazione senza effettuare cambiamenti se il ritorno atteso non supera il costo 
# delle fees

daily_port_build_bonus = DailyPortfolioBuilderBonus(capital = capital, data = historical_data, 
                                                    min_invest = min_invest, start="2021-07-01",
                                                    fees = 0.001)

# Salvare in un csv la composizione di portafoglio in modo che:
# - le colonne rappresentino i singoli asset
# - le righe i giorni dell'anno dal 01/07/2021 in poi

# Caso 1: portafoglio a varianza minima dei rendimenti
daily_port_bonus_min_var = daily_port_build_bonus.min_var(save_path = "output/daily_port_bonus_min_var.csv")

# Caso 2: portafoglio con rapporto maggiore tra media e deviazione standard dei rendimenti 
daily_port_bonus_rate_mean_std = daily_port_build_bonus.rate_mean_std(save_path = "output/daily_port_bonus_rate_mean_std.csv")

f.close()



    