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

from tqdm.auto import tqdm
tqdm.pandas()

# from datetime import date, time, datetime
plt.rcParams["figure.figsize"] = (16,8)
import warnings
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

def createColumnsMaior5K(row):
    menor5kGas = row['entre_0_5KM_gas']
    menor5kPla = row['dist_0_5KM_Pla']

    if menor5kGas:
        row['maior5KM_gas'] = False

    else:
        row['maior5KM_gas'] = True

    if menor5kPla:
        row['maior5KM_Pla'] = False
    else:
        row['maior5KM_Pla'] = True

    return row

colunasSemDup = [ 
        'ID', 'Arte', 'SubArte', 'TI', 'Comunidade',
        'Porto Desembarque', 'Data Registro', 'Entrevistado', 'Embarcação',
        'Núm. Pescadores', 'Pesqueiro', 'Data Saída', 'Hora Saída', 'Data Chegada',
        'Hora Chegada', 'Tipo Embarc.', 'Tipo IBAMA', 'Núm. Linhas',
        'Núm. Anzóis', 'Tamanho Anzol', 'Isca', 'Espécie Alvo', 'Comp. Rede',
        'Tamanho Malha', 'Altura Malha', 'Quantas Camboas',
        'Dias Não Despesca Camboa', 'Quant. Morredores',
        'Núm. Pescadores Participaram', 'Proprietário Camboa',
        'Núm. Armadilhas', 'Tamanho Armadilhas', 'Núm. Bocas Armadilha',
        'Utiliza Guincho', 'Quant. Dias Pescou Mês', 'Observação',
        'Profund. Lance', 'Houve Captura', 'Litros Combust.', 'Combustível(R$)',
        'Rancho(R$)', 'Gêlo(R$)', 'Isca(R$)', 'Venda Direta', 'Atravessador',
        'Consumo', 'Peixaria,Mercado', 'newID', 'Ano', 'Mês', 'KgTotal',
        'R$Total', 'CPUE kg/dia', 'Valoração', 'corresponde', 'CoordX',
        'CoordY', 'dist_gas', 'dist_plat', 'menor500M_gas', 'entre_0_5KM_gas',
        'entre_05_5KM_gas', 'entre_05_1KM_gas', 'entre_1_2KM_gas',
        'entre_2_3KM_gas', 'entre_3_4KM_gas', 'entre_4_5KM_gas',
        'dist_0_500M_Pla', 'dist_05_5KM_Pla', 'dist_0_5KM_Pla',
        'dist_05_1KM_Pla', 'dist_1_2KM_Pla', 'dist_2_3KM_Pla', 'dist_3_4KM_Pla',
        'dist_4_5KM_Pla'
    ]

path_folder = '/home/superusuario/Dados/proj/BCA_RAI/enviar/'
saveinExcel = True
pathInput = 'BD/Dados_distancias_CPUE_coordPequeirosValidadoUpgrade_remDup_08_09_2023.csv'
pathoutput = 'BD/Dados_distancias_CPUE_coordPequeirosValidadoUpgrade_comID_Unicos_05_10_2023.csv'

if os.path.isfile(pathoutput):
    df_freq = pd.read_csv(pathoutput, low_memory=False)  # 
    print("Tabela atualizada foi carregada ")
    if saveinExcel:
        df_freq.to_excel(pathoutput.replace('.csv',  '.xlsx') , index=False)

else:
    df_freq = pd.read_csv(pathInput, low_memory=False)  # 
    print("Tabela atualizada foi carregada ")


    print(f"Loading {df_freq.shape[0]} registros com {df_freq.shape[1]} columnas ")
    df_freq = df_freq[colunasSemDup]
    print(df_freq.columns)
    print(df_freq.head())




    df_freqUnic = df_freq.drop_duplicates('ID', keep='last')
    print("nova tabela sem duplicidade nos IDs tem ", df_freqUnic.shape)

    print("calculing columns Maior que 5KM")
    df_freqUnic = df_freqUnic.progress_apply(createColumnsMaior5K, axis= 1)

    df_freqUnic.to_csv(pathoutput , index = False)
    print("csv saving in DB")

