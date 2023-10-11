import pandas as pd 
import os
import  sys

knowTime = True
showMinMax = False
showComunidades = False
lst_subArtes = [
    'MARISCAGEM', 'ABALO', 'CERCO', 'GAIOLA', 'CALÃO', 
    'LINHA DE MÃO', 'EMALHE', 'ARRAEIRA', 'REÇA', 'GROSEIRA', 
    'REDINHA', 'MANZUÁ', 'ARRASTO DE FUNDO OU BALOEIRO', 
    'MERGULHO', 'PESQUEIRO', 'TARRAFA', 'ESPINHEL', 'JERERÉ', 
    'TAINHEIRA', 'PARUZEIRA', 'FUNDO CAMARÃO', 'FUNDO PEIXE', 
    'SUPERFÍCIE BOIADA'
]

dictSubArttime = {}


if knowTime:
    pathInput= 'BD/Dados_distancias_CPUE_coordPequeirosValidado_Menor5KM_remDupIDs_26_08_2023.csv'
else:
    pathInput = 'BD/Dados_distancias_CPUE_coordPequeirosValidado_Menor5KM_remDupIDs_26_08_2023.csv'
df_freq = pd.read_csv(pathInput, low_memory=False)

print("tamanho ", df_freq.shape)
print(df_freq.columns)
# 'Nome Pesqueiro', 'Coord x Pesqueiro', 'Coord y Pesqueiro'
print(df_freq['TI'].unique())
lstSubA = [kk for kk in df_freq['SubArte'].unique()]
print(len(lstSubA))

# sys.exit()
for tiname in ['BTS', 'BAIXO SUL']:
    for cc, subArt in enumerate(lst_subArtes):
        print(cc, " filtering by ", subArt, "in TI => ", tiname)
        df_subArte = df_freq[(df_freq['SubArte'] == subArt) & (df_freq['TI'] == tiname)]
        print(" => ", df_subArte.shape[0])
        
        if knowTime:
            df_subArte = df_subArte.dropna(axis= 0, subset=['Data Saída', 'Data Chegada'])
            lstDatas = [kk for kk in df_subArte['Data Saída'].unique()]
            print(df_subArte.shape)
            
            # try:
            df_subArte['Data Saída'] == pd.to_datetime(df_subArte['Data Saída'], format='%d/%m/%Y') # 
            df_subArte['Data Chegada'] == pd.to_datetime(df_subArte['Data Chegada'], format='%Y-%m-%d') # , format="%m/%d/%Y, %H:%M:%S"
            print(" calculo Date")
            datemin = df_subArte['Data Saída'].min()
            datemax = df_subArte['Data Chegada'].max()

            print(f"datas entre {datemin}  e {datemax} with {df_subArte.shape[0]} registros")
            # except:
            #     for ii, dat in enumerate(lstDatas):
            #         if len(str(dat)) != 10:
            #             print(dat)

        elif showMinMax:
            df_subArte = df_subArte[df_subArte['dist_gas'] != 3.413]
            distminGas = df_subArte['dist_gas'].min()
            distmaxGas = df_subArte['dist_gas'].max()

            distminPlat = df_subArte[df_subArte['dist_plat'] < 5000]['dist_plat'].min()            
            distmaxPlat = df_subArte[df_subArte['dist_plat'] < 5000]['dist_plat'].max()

            print(f"Distancia minima a Plataforma  {distminPlat} e maximas  {distmaxPlat}")
            print(f"Distancia minima a Gasoduto  {distminGas}  e maximas  {distmaxGas}")
            print("===================="*3)

        elif showComunidades:
            lstUniq = [ll for ll in df_subArte['Comunidade'].unique()]
            print("TI ", tiname," subArte = ", subArt, " ==> \n   ", lstUniq)
            print("===================================================")