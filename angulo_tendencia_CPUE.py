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
from sklearn.linear_model import LinearRegression
from tqdm.auto import tqdm
tqdm.pandas()

# from datetime import date, time, datetime
plt.rcParams["figure.figsize"] = (16,8)
import warnings
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")


class reducirDataFramebyStep:

    def __init__(self, tPaso):
        self.paso = tPaso
        self.contador = 0

    def setColumnsSteps(self, row):
        if self.contador % self.paso == 0 and self.contador != 0 :
            row['excluir'] = False
        else:
            row['excluir'] = True
        self.contador += 1
        return row

    def reduceDataFramebyStep(self, tempDFInd):            
        tempDFInd = tempDFInd.apply(self.setColumnsSteps, axis= 1)
        return tempDFInd[tempDFInd['excluir'] == False]



intervaloTimeCPUE = True
makeTrends = False

lstInd = ['CPUE kg/dia']
lst_distGasPla = ['entre_0_5KM_gas', 'dist_0_5KM_Pla']
pathInput = 'BD/Dados_distancias_CPUE_coordPequeirosValidadoUpgrade_comID_Unicos_05_10_2023.csv'


df_freq = pd.read_csv(pathInput, low_memory=False)  # 
print("Tabela atualizada foi carregada ")

print(f"Loading {df_freq.shape[0]} registros com {df_freq.shape[1]} columnas ")
allColumns = [kk for kk in df_freq.columns]
print(df_freq.columns)
print(df_freq.head())

yyinterv = ['01-01-2005', '01-01-2008', '01-01-2013', '01-01-2021']
yyIndInterv = ['yy05_07_', 'yy08_12_', 'yy13_20']
df_freq['Data Chegada'] = pd.to_datetime(df_freq['Data Chegada'], format='%Y-%m-%d')
df_freq = df_freq.sort_values(by='Data Chegada')

lst_colnDF = ['SubArtes'] + lst_distGasPla
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

indic = 'CPUE kg/dia'
for tiname in [ 'BAIXO SUL', 'BTS']:  #
    dictComTI = {}
    lst_subArtes= dictTISubArte[tiname]
    for cc, subArt in enumerate(lst_subArtes):

        if cc > -1:
            df_tendecia = pd.DataFrame({}, columns=[])
            dict_tend = {}

            dict_tend['TI'] = tiname
            dict_tend['SubArtes'] = subArt
            dict_tend['tipo'] = 'angulo tendencia'            

            df_subArte = df_freq[(df_freq['SubArte'] == subArt) & (df_freq['TI'] == tiname)]
            nameSub = subArt.replace(' ', '_')
            print("== # ", cc, "  >  ", nameSub, " == > ", df_subArte.shape, " =====" , "in TI => ", tiname)
            print("size ", df_subArte.shape)


                    
            if makeTrends:
                print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                
                dict_tend['indicador'] = indic
                # dict_p['indicador'] = indic        
                    
                for dist in lst_distGasPla[:]:
                    
                    df_dist = copy.deepcopy(df_subArte[df_subArte[dist] == True])
                    df_dist = df_dist.sort_values(by='Data Chegada')
                    df_dist.dropna(subset=['CPUE kg/dia'], inplace=True)
                    sizeTab = df_dist.shape[0]
                    print(" ==> ", indic, " ==>   ", dist, " ==> ", sizeTab)
                    # print(" tamanho tabela resultante ", sizeTab)
                    

                    if sizeTab > 3: 
                        if sizeTab > 30000:
                            reducirDF = reducirDataFramebyStep(3)
                            df_reducida = reducirDF.reduceDataFramebyStep(df_dist)
                            print("new dimension ", df_reducida.shape[0])
                            
                        else:
                            df_reducida = copy.deepcopy(df_dist)
                        
                        colParInclina = ['Data Chegada','CPUE kg/dia']
                        newdf = df_reducida[colParInclina]
                        newdf.columns = ['tempo','CPUE kg/dia']
                        data_inic = newdf['tempo'].iloc[0]
                        data_end = newdf['tempo'].iloc[newdf.shape[0] - 1]
                        print("tamanho da tabela ", newdf.shape[0])
                        data_inic = data_inic.date()
                        data_end = data_end.date()
                        print("data inicial = ", data_inic)
                        print("data final = ", data_end)
                        # executando a função de agregação das variaveis 
                        def set_variaveis_tempo(row):            
                            d2 = row['tempo']
                            # print('d2 = ', type(d2), "  ", d2)
                            # d2 = datetime.datetime.strptime(d2, '%Y-%m-%d')    
                            d2 = d2.date()
                            # print("{} | {} ".format(row.index, d2))
                            diff = d2 - data_inic
                            year_float = diff.days / 365        

                            vals_radn = year_float *  2 * np.pi
                            # print("year em radiam", vals_radn)

                            row['date'] = year_float
                            row['seno'] = math.sin(vals_radn)
                            row['coseno'] = math.cos(vals_radn)
                            row['constante'] = 1 
                            
                            return row
                        newdf = newdf.apply(set_variaveis_tempo, axis= 1)

                        # definicao das variaveis para a sertie harmonica 
                        X = newdf[['constante','date','seno','coseno']]  # 
                        y = newdf['CPUE kg/dia']

                        regresion_lineal = LinearRegression()
                        regresion_lineal.fit(X, y) 
                        coefic = regresion_lineal.coef_
                        print("lista de coeficients ", coefic) 
                        prediction = regresion_lineal.predict(X)
                        newdf[indic + ' est'] = prediction

                        indexC = [kk for kk in range(0, newdf.shape[0])]
                        newdf['contador'] = indexC

                        # criando e treinando o modelo
                        modelo_lineal = LinearRegression()
                        Xind = newdf[['constante', 'contador']]
                        yest = newdf[indic + ' est']
                        modelo_lineal.fit(Xind,  yest) 
                        coefic_linealred = modelo_lineal.coef_
                        print("lista de coeficients ", coefic_linealred) 
                        angulo_linha = math.degrees(math.atan(coefic_linealred[1]))

                        dict_tend[dist + '_pend'] = round(coefic_linealred[1], 4)
                        dict_tend[dist + '_angu'] =  round(angulo_linha, 4)
                        conclus = "Baixa"

                        if math.fabs(angulo_linha) < 13.5:
                            conclus = "Baixo"
                        elif math.fabs(angulo_linha) >= 13.5 and math.fabs(angulo_linha) < 22.5:
                            conclus = "Medio"
                        else:
                            conclus = "Alto"
                        
                        dict_tend[dist + '_Aval'] = conclus

                    else:            
                        dict_tend[dist + '_pend'] = 'sem info'
                        dict_tend[dist + '_angu'] = 'sem info'
                        dict_tend[dist + '_Aval'] = 'sem info'
                    dict_tend["Quant-" + dist] = df_dist.shape[0]

                dict_tend['Quantidade'] = df_subArte.shape[0]          

                df_tend = pd.DataFrame([dict_tend])             

                df_tendecia = pd.concat([df_tendecia, df_tend], axis= 0, ignore_index=True)

                
                print("data frame de tendencias ")
                # print( df_tendecia )
                idTI = tiname.replace(" ", "_")
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_angulo_Tendencia_Indicador_CPUE_{idTI}_{nameSub}_05_10_2023_magn.csv"

                df_tendecia.to_csv(path_saveTendencia, index=False)
                print("tabela de angulos salvas em csv")


            if intervaloTimeCPUE:
                dict_tend['Quantidade'] = df_subArte.shape[0]
                
                for cc in range(len(yyinterv)):                    
                    if cc > 0:
                        indicador = yyIndInterv[cc - 1]
                        # date_string = "2023-09-01 14:30:00.123"
                        date_format = "%d-%m-%Y"
                        dict_tend['intervalo'] = indicador

                        # Convert string to datetime using strptime
                        # date_obj = datetime.strptime(date_string, date_format)
                        date_t0 = datetime.strptime(yyinterv[cc - 1],  date_format)
                        date_t1 = datetime.strptime(yyinterv[cc],   date_format)
                        print(" Time Date ", date_t0, " -> ", date_t1)

                        dfinterval = df_subArte[(df_subArte['Data Chegada'] > date_t0) & (df_subArte['Data Chegada'] < date_t1)]
                        sizeTable = dfinterval.shape[0]

                        dict_tend['Quant_' + indicador] = sizeTable

                        for mdist in lst_distGasPla:
                            df_dist = copy.deepcopy(dfinterval[dfinterval[mdist] == True])    
                            df_dist = df_dist.sort_values(by='Data Chegada')  
                            df_dist.dropna(subset=['Data Chegada','CPUE kg/dia'], inplace=True)                     
                            sizeTab = df_dist.shape[0] 
                            dict_tend['indicador'] = 'CPUE_periodo'

                            indicadorCPUE = 'CPUE kg/dia'
                            if sizeTab > 3:
                                # reagrupando por 
                                if sizeTab > 30000:
                                    reducirDF = reducirDataFramebyStep(3)
                                    df_reducida = reducirDF.reduceDataFramebyStep(df_dist)
                                    print("new dimension ", df_reducida.shape[0])
                                    
                                else:
                                    df_reducida = copy.deepcopy(df_dist)

                                colParInclina = ['Data Chegada','CPUE kg/dia']
                                newdf = df_reducida[colParInclina]
                                newdf.columns = ['tempo','CPUE kg/dia']
                                data_inic = newdf['tempo'].iloc[0]
                                data_end = newdf['tempo'].iloc[newdf.shape[0] - 1]
                                print("tamanho da tabela ", newdf.shape[0])          

                                data_inic = data_inic.date()
                                data_end = data_end.date()
                                print("data inicial = ", data_inic)
                                print("data final = ", data_end)

                                # executando a função de agregação das variaveis 
                                def set_variaveis_tempo(row):            
                                    d2 = row['tempo']
                                    d2 = d2.date()
                                    # print("{} | {} ".format(row.index, d2))
                                    diff = d2 - data_inic
                                    year_float = diff.days / 365        

                                    vals_radn = year_float *  2 * np.pi
                                    # print("year em radiam", vals_radn)

                                    row['date'] = year_float
                                    row['seno'] = math.sin(vals_radn)
                                    row['coseno'] = math.cos(vals_radn)
                                    row['constante'] = 1 
                                    
                                    return row
                                
                                newdf = newdf.apply(set_variaveis_tempo, axis= 1)

                                # definicao das variaveis para a sertie harmonica 
                                X = newdf[['constante','date','seno','coseno']]  # 
                                y = newdf['CPUE kg/dia']

                                regresion_lineal = LinearRegression()
                                regresion_lineal.fit(X, y) 
                                coefic = regresion_lineal.coef_
                                print("lista de coeficients ", coefic) 
                                prediction = regresion_lineal.predict(X)
                                newdf[indic + ' est'] = prediction

                                indexC = [kk for kk in range(0, newdf.shape[0])]
                                newdf['contador'] = indexC

                                # criando e treinando o modelo
                                modelo_lineal = LinearRegression()
                                Xind = newdf[['constante', 'contador']]
                                yest = newdf[indic + ' est']
                                modelo_lineal.fit(Xind,  yest) 
                                coefic_linealred = modelo_lineal.coef_
                                print("lista de coeficients ", coefic_linealred) 
                                angulo_linha = math.degrees(math.atan(coefic_linealred[1]))

                                dict_tend[mdist + '_pend'] = round(coefic_linealred[1], 4)
                                dict_tend[mdist + '_angu'] =  round(angulo_linha, 4)
                                conclus = "Baixa"

                                if math.fabs(angulo_linha) < 13.5:
                                    conclus = "Baixo"
                                elif math.fabs(angulo_linha) >= 13.5 and math.fabs(angulo_linha) < 22.5:
                                    conclus = "Medio"
                                else:
                                    conclus = "Alto"
                                
                                dict_tend[mdist + '_Aval'] = conclus

                            else:            
                                dict_tend[mdist + '_pend'] = 'sem info'
                                dict_tend[mdist + '_angu'] = 'sem info'
                                dict_tend[mdist + '_Aval'] = 'sem info'
                            dict_tend["Quant-" + mdist] = df_dist.shape[0]

                        
                        dict_tend['Quantidade'] = df_subArte.shape[0]         
                        df_tend = pd.DataFrame([dict_tend])             
                        df_tendecia = pd.concat([df_tendecia, df_tend], axis= 0, ignore_index=True)

                print("data frame de tendencias ")

                idTI = tiname.replace(" ", "_")
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_angulo_INTEVALO_05-07_Tendencia_Indicador_CPUE_{idTI}_{nameSub}_05_10_2023_magn.csv"

                df_tendecia.to_csv(path_saveTendencia, index=False)
                print("tabela de angulos salvas em csv")