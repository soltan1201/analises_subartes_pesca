import os
import copy
import time
import pymannkendall as mk
# Raising a ValueError
from datetime import datetime
import seaborn as sns
import sys
sns.set_theme(style="darkgrid")
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from tqdm.auto import tqdm
tqdm.pandas()

lst_distG = [
    'menor500M_gas', 'entre_0_5KM_gas', 'entre_05_1KM_gas', 
    'entre_1_2KM_gas', 'entre_2_3KM_gas', 'entre_3_4KM_gas', 
    'entre_4_5KM_gas' , 'maior5KM_gas', 'maior5KM_Pla'
]
lst_distP = [
    'dist_0_500M_Pla',  'dist_0_5KM_Pla', 'dist_05_1KM_Pla', 
    'dist_1_2KM_Pla', 'dist_2_3KM_Pla', 'dist_3_4KM_Pla',
    'dist_4_5KM_Pla'
]
lst_distG = lst_distG + lst_distP
lst_distGasPla = ['entre_0_5KM_gas', 'dist_0_5KM_Pla', 'maior5KM_gas', 'maior5KM_Pla']
makePlots = False
makePlotOcorrSA = True
dictTendencia = {
    'increasing' : 'crescente',
    'decreasing' : 'decrescente',
    'no trend' : 'não tendencia'
}
dictComun = {}

path = os.getcwd()
pathInput = 'BD/Dados_distancias_CPUE_coordPequeirosValidadoUpgrade_comID_Unicos_05_10_2023.csv'

input_path = os.path.join(path, pathInput)
print('loading file CSV from FOLDER DB \n =====>  ', input_path)


df_freq = pd.read_csv(input_path, low_memory=False)  # 
print("Tabela atualizada foi carregada ")


print(f"Loading {df_freq.shape[0]} registros com {df_freq.shape[1]} columnas ")
allColumns = [kk for kk in df_freq.columns]
# print(df_freq.columns)
# print(df_freq.head())

yyinterv = ['01-01-2005', '01-01-2008', '01-01-2013', '01-01-2021']
yyIndInterv = ['yy05_07_', 'yy08_12_', 'yy13_20',"todo_o_Periodo"]
df_freq['Data Chegada'] = pd.to_datetime(df_freq['Data Chegada'], format='%Y-%m-%d')
df_freq = df_freq.sort_values(by='Data Chegada')

lst_colnDF = ['SubArtes'] + lst_distG

lst_subArtesAct = [
    'TAINHEIRA','JERERÉ','TARRAFA','PESQUEIRO', 'GAIOLA','MANZUÁ','FUNDO CAMARÃO',
    'CALÃO', 'MERGULHO','ARRAEIRA','SUPERFÍCIE BOIADA','ABALO','REDINHA','GROSEIRA',
    'EMALHE','LINHA DE MÃO','CERCO', 'FUNDO PEIXE','MARISCAGEM','ARRASTO DE FUNDO OU BALOEIRO'    
]
df_freq = df_freq[df_freq["SubArte"].isin(lst_subArtesAct)]
print("new size table ", df_freq.shape)

dictTI = {
    'BTS': 'BTS', 
    'BAIXO SUL': 'BS'
}
dictTISubArte = {
    'BTS': [
        'TAINHEIRA','JERERÉ','TARRAFA','PESQUEIRO',
        'GAIOLA','MANZUÁ','FUNDO CAMARÃO','MARISCAGEM',
        'CALÃO', 'MERGULHO','ARRAEIRA','SUPERFÍCIE BOIADA','ABALO','REDINHA','GROSEIRA',
        'EMALHE','LINHA DE MÃO','CERCO', 'FUNDO PEIXE'
    ], 
    'BAIXO SUL': [
        "GAIOLA", 'CALÃO', 'MANZUÁ','ARRASTO DE FUNDO OU BALOEIRO', 'SUPERFÍCIE BOIADA',
        'GROSEIRA','LINHA DE MÃO', 'ARRAEIRA', 'MERGULHO', "MARISCAGEM"
    ]
}

if makePlotOcorrSA:
    df_groupBS = df_freq[df_freq["TI"] == 'BAIXO SUL'][["SubArte","Arte"]].groupby(["SubArte"], as_index=False).agg('count')
    df_groupBTS = df_freq[df_freq["TI"] == 'BTS'][["SubArte","Arte"]].groupby(["SubArte"], as_index=False).agg('count')
    df_groupBTS.columns =["SubArte","BTS"]
    print(df_groupBTS.head(2))
    print(df_groupBS.head(2))
    def setnewColumns(row):
        subArte = row["SubArte"]
        try:
            quant = df_groupBS[df_groupBS['SubArte'] == subArte]["Arte"].values[0]
        except:
            quant = 0
        
        # print(f"quantidade {subArte} => {quant}" )
        row["BAIXO SUL"] = quant

        return row 
    df_groupBTS = df_groupBTS.apply(setnewColumns, axis= 1)

    print(df_groupBTS.head())
    print(df_groupBTS.tail())

    df_groupBTS.plot.barh(x='SubArte', y=["BAIXO SUL",  'BTS']) 
    plt.show()

else:
    for tiname in [ 'BAIXO SUL', 'BTS']:  #
        dictComTI = {}
        lst_subArtes= dictTISubArte[tiname]

        for cc, subArt in enumerate(lst_subArtes):
            df_subArte = df_freq[(df_freq['SubArte'] == subArt) & (df_freq['TI'] == tiname)]
            nameSub = subArt.replace(' ', '_')
            print("== # ", cc, "  >  ", nameSub, " == > ", df_subArte.shape, " =====" , "in TI => ", tiname)
            print("size ", df_subArte.shape)
            df_tendecia = pd.DataFrame({}, columns=lst_colnDF)
            dict_tend = {}
            dict_p = {}
            dict_tend['TI'] = tiname
            dict_p['TI'] = tiname
            dict_tend['SubArtes'] = subArt
            dict_p['SubArtes'] = subArt
            dict_tend['tipo'] = 'TMA' # tamanho mínimo de amostra


            for cc in range(len(yyinterv)):
                
                if cc > 0:
                    indicador = yyIndInterv[cc - 1]
                    # date_string = "2023-09-01 14:30:00.123"
                    date_format = "%d-%m-%Y"
                    dict_tendQ['intervalo'] = indicador
                    dict_pQ['intervalo'] = indicador  
                    # Convert string to datetime using strptime
                    # date_obj = datetime.strptime(date_string, date_format)
                    date_t0 = datetime.strptime(yyinterv[cc - 1],  date_format)
                    date_t1 = datetime.strptime(yyinterv[cc],   date_format)
                    print(" Time Date ", date_t0, " -> ", date_t1)

                    dfinterval = df_subArte[(df_subArte['Data Chegada'] > date_t0) & (df_subArte['Data Chegada'] < date_t1)]
                    sizeTable = dfinterval.shape[0]
                    print("size table in interval ", sizeTable)
                    dict_tendQ['Quantidade'] = sizeTable
                    dict_pQ['Quantidade'] = sizeTable
                    # print(dfinterval.columns)
                    # print(dfinterval[['SubArte', 'Data Chegada', 'Data Saída']].head(10))
                    
                    for mdist in lst_distG:
                        df_dist = copy.deepcopy(dfinterval[dfinterval[mdist] == True])                           

                        if df_dist.shape[0] > 5:
                            # reagrupando por 
                            df_quantidade = refazedDataFrameQuantidade(df_dist)

                            print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                            print("===>  ", df_quantidade.head())
