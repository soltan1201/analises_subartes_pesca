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

path_folder = '/home/superusuario/Dados/proj/BCA_RAI/enviar/'
def get_analise_Kendall (tempDF, indicador):
    result = mk.original_test(tempDF[indicador])    
    return result[0], result[2]

def get_Tendencia_Kendall (tempDF):
    result = mk.original_test(tempDF['count'])    
    return result[0], result[2]


def plot_CPUE(temp_dfV, subarte, distGas, mfolder, nameTI):
    # import seaborn as sns
    sns_plotV = sns.lineplot(x = 'Data Chegada', y ='CPUE kg/dia', color='#45b39d', linewidth=2 , data = temp_dfV)
    plt.xticks(rotation=25)
    mytile = "Plot Serie de Valor Total com TI {} SubArte {} \n com distancia \n Gasoduto {}".format(nameTI,subarte, distGas)
    plt.title(mytile)
    # plt.show()
    nameSaveS = mfolder + "/CPUE_kg_dia_TI_{}_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI,subarte, distGas)
    sns_plotV.figure.savefig(nameSaveS)
    plt.close()

def plot_Captura(temp_dfC, subarte, distGas, mfolder, nameTI):
    
    sns_plotCap = sns.lineplot(x = 'Data Chegada', y ='KgTotal', color='#5dade2', linewidth=2 , data = temp_dfC)
    plt.xticks(rotation=25)
    
    mytile = "Plot Serie de Captura total com TI {} e SubArte {}  \n com distancia Gasoduto {}".format(nameTI, subarte, distGas)
    plt.title(mytile)

    nameSaveC = mfolder + "/CapturaTotal_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI, subarte, distGas)
    sns_plotCap.figure.savefig(nameSaveC)
    plt.close()
    # sns_plotCap.close()

def plot_Renda(temp_dfR, subarte, distGas, mfolder, nameTI):
    
    sns_plotRend = sns.lineplot(x = 'Data Chegada', y ='R$Total', color='#e67e22', linewidth=2 , data = temp_dfR)
    plt.xticks(rotation=25)

    mytile = "Plot Serie de Renda Total com TI {} SubArte {}  \n com distancia Gasoduto {}".format(nameTI, subarte, distGas)
    plt.title(mytile)

    nameSaveR = mfolder + "/RendaTotal_TI_{}_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI, subarte, distGas)
    sns_plotRend.figure.savefig(nameSaveR)
    plt.close()

# 'Valor/Kg(R$)'
def plotValor_vs_Kg(temp_dfR, subarte, distGas, mfolder, nameTI):

    sns_plotValorKG = sns.lineplot(x = 'Data Chegada', y ='Valor/Kg(R$)', color='#3780b6', linewidth=2 , data = temp_dfR)
    plt.xticks(rotation=25)

    mytile = "Plot Serie de Valor por Kg com SubArte {}  \n com distancia Gasoduto {}".format(nameTI, subarte, distGas)
    plt.title(mytile)

    nameSaveR = mfolder + "/ValorVsKg_TI_{}_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI, subarte, distGas)
    sns_plotValorKG.figure.savefig(nameSaveR)
    plt.close()

# 'Quant. Dias Pescou Mês'
def plotQuantidadeDias_Pesca(temp_dfR, subarte, distGas, mfolder,nameTI):

    sns_plotDiasPesc = sns.lineplot(x = 'Data Chegada', y ='Quant. Dias Pescou Mês', color='#41b637', linewidth=2 , data = temp_dfR)
    plt.xticks(rotation=25)

    mytile = "Plot Serie de Quantidade deDias de pesca com TI {} e SubArte {}  \n com distancia Gasoduto {}".format(nameTI, subarte, distGas)
    plt.title(mytile)

    nameSaveR = mfolder + "/QuantDiasPesca_TI_{}_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI, subarte, distGas)
    sns_plotDiasPesc.figure.savefig(nameSaveR)
    plt.close()

def show_values(axs, orient="v", space=.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{}'.format(int(p.get_height()))   # :.1f
                ax.text(_x, _y, value, ha="center")
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{}'.format(int(p.get_width())) # :.1f
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)


def plot_Quantidade(temp_dfQ, subarte, distGas, mfolder,nameTI):
    # print("rodando dentro da função ")
    # print(temp_dfQ.shape)
    yeartmp = 2021
    def set_year(row):
        yeartmp = 2021
        data_chega = row['Data Saída']
        try:
            lstDtr = data_chega.split('/')
        except:
            lstDtr = [1,1,yeartmp]
        # print(lstDtr)
        row['year'] = int(lstDtr[2])
        yeartmp = int(lstDtr[2])
        return row

    temp_dfQ = temp_dfQ.apply(set_year, axis= 1)
    count_yy = temp_dfQ['year'].value_counts()
    # print(count_yy)

    lst_year =[]
    lst_count = []
    for year in range(2005, 2022):

        valor = 0
        try:
            valor = count_yy[year]
            # print("year {} == {}".format(year, valor))
        except:
            # print("year {} == {}".format(year, valor))
            pass

        lst_year.append(str(year))
        lst_count.append(valor)
    
    
    df_yy_count = pd.DataFrame({
        'year': lst_year,
        'count': lst_count
    })

    # print("dataframe Year \n", df_yy_count)
    #create vertical barplot
    # sns_plotYY = sns.barplot(y="year", x="count", data=df_yy_count, color='#5082BC',errorbar=None)
    # sns_plotYY.set_xlabel("Quantidade")


    fig, ax = plt.subplots(figsize=(7,9))
    bar = ax.barh(df_yy_count["year"], df_yy_count["count"], color='#5082BC')
    plt.tight_layout()
    plt.xticks(rotation=25)
    maximo = np.max(df_yy_count["count"])
    plt.xlim(0, maximo + 0.2 * maximo)
    mytile = "Plot número de registros por ano TI {} e subArte {} com distancia Gasoduto {}".format(nameTI, subarte, distGas)
    plt.title(mytile)
    plt.subplots_adjust(top=0.9, bottom=0.1)

    rects = ax.patches
    # Place a label for each bar
    for rect in rects:
        # Get X and Y placement of label from rect
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label; change to your liking
        space = 10
        # Vertical alignment for positive values
        ha = 'left'

        # If value of bar is negative: place label to the left of the bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label to the right
            ha = 'right'

        # Use X value as label and format number
        label = '{:,.0f}'.format(x_value)

        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at bar end
            xytext=(space, 0),          # Horizontally shift label by `space`
            textcoords='offset points', # Interpret `xytext` as offset in points
            va='center',                # Vertically center label
            ha=ha,                      # Horizontally align label differently for positive and negative values
            color = 'black')            # Change label color to white

    #show values on barplot
    # show_values(sns_plotYY)
    # plt.show()
    # path_folder +
    nameSaveR =  mfolder + "/NumeroRegistros_TI_{}_SubArte_{}_dist_Gasoduto_{}.png".format(nameTI, subarte, distGas)  
    # sns_plotYY.figure.savefig(nameSaveR)
    plt.savefig(nameSaveR, dpi=350, format='png', bbox_inches='tight')
    plt.close()


def refazedDataFrameQuantidade(temp_dfQ) :
    yeartmp = 2021
    def set_year(row):
        yeartmp = 2021
        data_chega = row['Data Saída']
        try:
            lstDtr = data_chega.split('/')
        except:
            lstDtr = [1,1,yeartmp]
        # print(lstDtr)
        row['year'] = int(lstDtr[2])
        yeartmp = int(lstDtr[2])
        return row

    temp_dfQ = temp_dfQ.apply(set_year, axis= 1)
    count_yy = temp_dfQ['year'].value_counts()
    count_yy = count_yy.reset_index()
    # print(count_yy)

    return count_yy


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


def building_serie_Renda_mensal(temp_dfM):
    monthtmp = 1
    yeartmp = 2021
    def set_year(row):
        yeartmp = 2021 
        data_chega = row['Data Saída']
        
        try:
            lstDtr = data_chega.split('/')
        except:
            lstDtr = [1,1,yeartmp]
        
        # print(lstDtr)
        row['month'] = int(lstDtr[1])
        row['year'] = int(lstDtr[2])
        row['year_month'] = str(lstDtr[2]) + '_' + str(int(lstDtr[1]))
        yeartmp = int(lstDtr[2])
        monthtmp = int(lstDtr[1])

        # row['Combustível(gasto R$)'] = row['Litros Combust.'] * row['Combustível(R$)']
        row['CM'] = row['Litros Combust.'] * row['Combustível(R$)'] + row['Rancho(R$)'] + \
                        row['Gêlo(R$)'] + row['Isca(R$)']      
        return row

    temp_dfM = temp_dfM.apply(set_year, axis= 1)
    lstInt = ['year', 'month', 'R$Total', 'year_month', 'CM' ]
    df_group = temp_dfM.groupby(['year', 'month'], as_index=False).agg({'R$Total':'sum', 'year_month': 'count', 'CM': 'sum'})
    
    def calculate_RM(row):
        row["RM"] = (row['R$Total'] / row['year_month']) - (row['CM'] / row['year_month'])
        row['data saida'] = datetime(int(row['year']), int(row['month']), 1)
        return row

    df_group = df_group.apply(calculate_RM, axis= 1)
    df_group = df_group.sort_values(by='data saida')
    
    return df_group

# lstInd = ['CPUE kg/dia', 'KgTotal', 'R$Total']'KgTotal',
lstInd = ['CPUE kg/dia']

ofolder = 'tables_Out_2023/plotNumRegYearG'
excelFolder = 'tables_Out_2023/tableSavedDist'
excelFoldersubart = 'tables_Out_2023/tableSavedSubArtes'
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
makePlots = True
makeTrends= False
tendenciaQuant = False
knowComunidades = False
saveSubArteInd = False
intervaloTime = False
frequenceSerie = False
intervaloTimeCPUE = False
frequenceSerieRendaM = False

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
# pathFileExcel = 'BD/Dados_distancias_CPUE_coordPequeirosValidadoUpgrade_comID_Unicos_05_10_2023.xlsx'

# df_freq.to_excel(pathFileExcel) 


# sys.exit()

print(f"Loading {df_freq.shape[0]} registros com {df_freq.shape[1]} columnas ")
allColumns = [kk for kk in df_freq.columns]
print(df_freq.columns)
print(df_freq.head())
# print(df_freq[df_freq['SubArte'] == 'PESQUEIRO']['TI'].unique())
# sys.exit()
# intervalos de analises de tendencia para a serie historia dividia em 3
# yyinterv = ['01-01-2005', '01-01-2011', '01-01-2016', '01-01-2022']
# yyIndInterv = ['yy05_10_', 'yy10_15_', 'yy15_22']
yyinterv = ['01-01-2005', '01-01-2008', '01-01-2013', '01-01-2021']
yyIndInterv = ['yy05_07_', 'yy08_12_', 'yy13_20']
df_freq['Data Chegada'] = pd.to_datetime(df_freq['Data Chegada'], format='%Y-%m-%d')
df_freq = df_freq.sort_values(by='Data Chegada')
# sys.exit()
# lst_subArtes = [kk for kk in df_freq['SubArte'].unique()]
# lst_subArtes.remove('Não Informado')
# lst_subArtes.remove('PESQUEIRO')


# lst_subArtes = ['LINHA DE MÃO']
# lst_dist = [ 'entre_0_5KM'] 
lst_colnDF = ['SubArtes'] + lst_distG
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
# sys.exit()
for tiname in [ 'BAIXO SUL', 'BTS']:  #
    dictComTI = {}
    lst_subArtes= dictTISubArte[tiname]
    for cc, subArt in enumerate(lst_subArtes):

        if cc > -1:
            df_tendecia = pd.DataFrame({}, columns=lst_colnDF)
            dict_tend = {}
            dict_p = {}
            dict_tend['TI'] = tiname
            dict_p['TI'] = tiname
            dict_tend['SubArtes'] = subArt
            dict_p['SubArtes'] = subArt
            dict_tend['tipo'] = 'tendencia'
            dict_p['tipo'] = 'p_value'

            df_tendeciaQuant = pd.DataFrame({}, columns=['TI', 'SubArtes', 'tendencia', 'tipo', 'indicador'])
            dict_tendQ = {}
            dict_pQ = {}
            dict_tendQ['TI'] = tiname
            dict_pQ['TI'] = tiname
            dict_tendQ['SubArtes'] = subArt
            dict_pQ['SubArtes'] = subArt
            dict_tendQ['tipo'] = 'tendencia'
            dict_pQ['tipo'] = 'p_value'
            dict_tendQ['Quantidade'] = 0
            dict_pQ['Quantidade'] = 0
            
            
            df_subArte = df_freq[(df_freq['SubArte'] == subArt) & (df_freq['TI'] == tiname)]
            nameSub = subArt.replace(' ', '_')
            print("== # ", cc, "  >  ", nameSub, " == > ", df_subArte.shape, " =====" , "in TI => ", tiname)
            print("size ", df_subArte.shape)
            
            # sys.exit()
            if saveSubArteInd:            
                nameSaveR = excelFoldersubart + "/tableTI_{}_subArte_{}_withDist.xlsx".format(dictTI[tiname],subArt)
                df_subArte.to_excel(nameSaveR)                
                print("saving in => ", nameSaveR) 


            if knowComunidades:
                # dictComun
                lstComunidade = [com for com in df_subArte['Comunidade'].unique()]
                # dictComun[subArt] = lstComunidade
                dictComTI[subArt] = lstComunidade


            #  makePolts = True
            if makePlots:
                print('========= PROCESSING ALL GRAPH ===========')
                for dist in lst_distG[:]:
                    # print("           ", dist)
                    df_dist = copy.deepcopy(df_subArte[df_subArte[dist] == True])
                    df_dist = df_dist.sort_values(by='Data Chegada')

                    # print(df_dist[[dist, 'Data Chegada']].head(8))
                    # print(df_dist[[dist,'Data Saída']].head(8))
                    sizeTab = df_dist.shape[0]
                    print("TI {} => subArtes {} | dist {} | size {}".format(dictTI[tiname], subArt, dist, df_dist.shape[0])) 

                    if sizeTab > 2:   
                        # # sys.exit()
                        plot_CPUE(df_dist, subArt, dist, ofolder, dictTI[tiname])
                        print("saving CPUE")
                        time.sleep(5)    # Pause 5.5 seconds

                        # plot_Captura(df_dist, subArt, dist, ofolder)
                        # print("saving Captura")
                        # time.sleep(5)

                        plot_Renda(df_dist, subArt, dist, ofolder,dictTI[tiname])
                        print("saving Renda Total")
                        time.sleep(5)    # Pause 5.5 seconds

                        plot_Quantidade(df_dist, subArt, dist, ofolder, dictTI[tiname])
                        print("saving Quantidade")
                        time.sleep(5)    # Pause 5.5 seconds

                        # plotValor_vs_Kg(df_dist, subArt, dist, ofolder)
                        # print("saving Serie Valor vs Kg")
                        # time.sleep(5)    # Pause 5.5 seconds
                        # try:
                        #     plotQuantidadeDias_Pesca(df_dist, subArt, dist, ofolder)
                        #     print("saving Quantidade de Dias de pesca")
                        #     time.sleep(5)    # Pause 5.5 seconds
                        # except:
                        #     print("ERRO TRY TO SAVE QUANTIDADE DIAS PESCA ")

        
            if makeTrends:
                print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                for indic  in lstInd:
                    dict_tend['indicador'] = indic
                    dict_p['indicador'] = indic        
                    
                    for dist in lst_distG[:]:
                        
                        df_dist = copy.deepcopy(df_subArte[df_subArte[dist] == True])
                        df_dist = df_dist.sort_values(by='Data Chegada')
                        sizeTab = df_dist.shape[0]
                        print(" ==> ", indic, " ==>   ", dist, " ==> ", sizeTab)
                        # print(" tamanho tabela resultante ", sizeTab)

                        if sizeTab > 3: 
                            if sizeTab > 30000:
                                reducirDF = reducirDataFramebyStep(3)
                                df_reducida = reducirDF.reduceDataFramebyStep(df_dist)
                                print("new dimension ", df_reducida.shape[0])
                                del(df_dist)
                                result_tend, result_p = get_analise_Kendall(df_reducida, indic) 
                            else:
                                result_tend, result_p = get_analise_Kendall(df_dist, indic) 
                            
                            dict_tend[dist] = dictTendencia[result_tend]

                            if  result_p< 0.05:
                                dict_p[dist] = 'significativo'                        
                            else:
                                dict_p[dist] = 'não significativo'    

                        else:            
                            dict_tend[dist] = 'sem informacao'
                            dict_p[dist] = 'sem informacao'

                        dict_tend["Quan-" + dist] = sizeTab
                        dict_p["Quan-" + dist] = sizeTab

                    dict_tend['Quantidade'] = df_subArte.shape[0]
                    dict_p['Quantidade'] = df_subArte.shape[0]

                    df_tend = pd.DataFrame([dict_tend])
                    df_p = pd.DataFrame([dict_p])

                    df_tendecia = pd.concat([df_tendecia, df_tend, df_p], axis= 0, ignore_index=True)

                
                print("data frame de tendencias ")
                # print( df_tendecia )
                idTI = tiname.replace(" ", "_")
                path_saveTendencia = f"tables_Out_2023/tendenciasInd/tabela_Tendencia_5KM_Indicador_{idTI}_{nameSub}_gasoduto_08_09_2023_update.csv"
                path_saveTendencia = f"tables_Out_2023/tendenciasInd/tabela_Tendencia_5KM_Indicador_{idTI}_{nameSub}_gasoduto_08_09_2023_update.csv"
                df_tendecia.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em csv")
                # path_saveTendencia = f"plotsAgos23/tendenciasXLSX/tabela_{idTI}_{nameSub}_gasoduto_26_08_2023.xlsx"
                # df_tendecia.to_excel(path_saveTendencia)  # , index=False


            if tendenciaQuant:
                if df_subArte.shape[0] > 0:
                    df_quantidade = refazedDataFrameQuantidade(df_subArte)
                    print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                    print("===>  ", df_quantidade.head())

                    dict_tendQ['indicador'] = 'frequencia'
                    dict_pQ['indicador'] = 'frequencia'         

                    df_quantidade = df_quantidade.sort_values(by='year')
                    sizeTab = df_quantidade.shape[0]
                else:
                    sizeTab = 0

                if sizeTab > 2:  
                    result_tend, result_p = get_Tendencia_Kendall(df_quantidade) 
                    dict_tendQ['tendencia'] = dictTendencia[result_tend]

                    if  result_p < 0.05:
                        dict_pQ['tendencia'] = 'significativo'                        
                    else:
                        dict_pQ['tendencia'] = 'não significativo'            
                
                else:            
                    dict_tendQ['tendencia'] = 'sem informacao'
                    dict_pQ['tendencia'] = 'sem informacao'

                df_tendQ = pd.DataFrame([dict_tendQ])
                df_pQ = pd.DataFrame([dict_pQ])

                df_tendeciaQuant = pd.concat([df_tendeciaQuant, df_tendQ, df_pQ], axis= 0, ignore_index=True)
                
                print("data frame de tendencias ")
                print(df_tendeciaQuant.head())
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_TENDENCIA_QUANT_{nameSub}_gasoduto_08_09_2023.csv"
                path_saveTendencia = os.path.join(path, path_saveTendencia)
                print(path_saveTendencia)
                df_tendeciaQuant.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em xlsx")


            if intervaloTime:

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
                                
                                dict_tendQ['indicador'] = 'frequencia'
                                dict_pQ['indicador'] = 'frequencia'         

                                df_quantidade = df_quantidade.sort_values(by='year')
                                sizeTab = df_quantidade.shape[0]                                

                                if sizeTab > 2:
                                    print("    calculando tendencia   ")
                                    result_tend, result_p = get_Tendencia_Kendall(df_quantidade) 
                                    dict_tendQ[mdist] = dictTendencia[result_tend]
                                    print("show tendencia result > ", result_tend, " | p-value ", result_p)
                                    if  result_p < 0.05:
                                        dict_pQ[mdist] = 'significativo'                        
                                    else:
                                        dict_pQ[mdist] = 'não significativo'     

                                    dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                                    dict_pQ['Quant_' + mdist] = df_dist.shape[0]         
                                
                                else: 
                                    dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                                    dict_pQ['Quant_' + mdist] = df_dist.shape[0]           
                                    dict_tendQ[mdist] = 'sem informacao'
                                    dict_pQ[mdist] = 'sem informacao'
                                
                            else:
                                dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                                dict_pQ['Quant_' + mdist] = df_dist.shape[0]
                                dict_tendQ[mdist] = 'sem informacao'
                                dict_pQ[mdist] = 'sem informacao'

                        df_tendQ = pd.DataFrame([dict_tendQ])
                        df_pQ = pd.DataFrame([dict_pQ])

                        df_tendeciaQuant = pd.concat([df_tendeciaQuant, df_tendQ, df_pQ], axis= 0, ignore_index=True)
                        

                # sys.exit()
                print("data frame de tendencias ")
                print(df_tendeciaQuant.head())
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_INTERVALO_NEW_TENDENCIA_QUANT{tiname}_{nameSub}_gasoduto_08_09_2023.csv"
                path_saveTendencia = os.path.join(path, path_saveTendencia)
                df_tendeciaQuant.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em xlsx")

    
            if frequenceSerie:  
                # date_string = "2023-09-01 14:30:00.123"
                date_format = "%d-%m-%Y"
                dict_tendQ['intervalo'] = 'todaSerie'
                dict_pQ['intervalo'] = 'todaSerie'  
                dict_tendQ['indicador'] = 'ocurrencia'
                dict_pQ['indicador'] = 'ocurrencia'
                dict_tendQ['Quantidade'] = df_subArte.shape[0]
                dict_pQ['Quantidade'] = df_subArte.shape[0]

                
                for mdist in lst_distG:
                    df_dist = copy.deepcopy(df_subArte[df_subArte[mdist] == True])                                   

                    if df_dist.shape[0] > 0:
                        # reagrupando por 
                        df_quantidade = refazedDataFrameQuantidade(df_dist)

                        print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                        print("===>  ", df_quantidade.shape[0] , "  <====== ")      
                        print(df_quantidade.head())    

                        totalReg = df_quantidade['count'].sum()  # total de registros 
                        dict_tendQ['Quant_' + mdist] = int(totalReg)
                        dict_pQ['Quant_' + mdist] = int(totalReg)

                        df_quantidade = df_quantidade.sort_values(by='year')
                        sizeTab = df_quantidade.shape[0]                

                        if sizeTab > 3:
                            print("  >>>>>>  calculando tendencia  <<<<<<<<< ")
                            result_tend, result_p = get_Tendencia_Kendall(df_quantidade) 
                            dict_tendQ[mdist] = dictTendencia[result_tend]
                            print("show tendencia result ", result_tend, " ", result_p)
                            if  result_p < 0.05:
                                dict_pQ[mdist] = 'significativo'                        
                            else:
                                dict_pQ[mdist] = 'não significativo'    
                            dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                            dict_pQ['Quant_' + mdist] = df_dist.shape[0]          
                        
                        else:    
                            dict_tendQ['Quant_' + mdist] = int(df_dist.shape[0])
                            dict_pQ['Quant_' + mdist] = int(df_dist.shape[0])        
                            dict_tendQ[mdist] = 'sem informacao'
                            dict_pQ[mdist] = 'sem informacao'
                            
                    else:     
                        dict_tendQ['Quant_' + mdist] = int(df_dist.shape[0])
                        dict_pQ['Quant_' + mdist] = int(df_dist.shape[0])        
                        dict_tendQ[mdist] = 'sem informacao'
                        dict_pQ[mdist] = 'sem informacao'                       

                df_tendQ = pd.DataFrame([dict_tendQ])
                df_pQ = pd.DataFrame([dict_pQ])

                df_tendeciaQuant = pd.concat([df_tendeciaQuant, df_tendQ, df_pQ], axis= 0, ignore_index=True)
                # sys.exit()
                print("data frame de tendencias ")
                print(df_tendeciaQuant.head())
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_OCURRENCIA_TENDENCIA_{tiname}_QUANT_{nameSub}_08_09_2023.csv"
                path_saveTendencia = os.path.join(path, path_saveTendencia)
                df_tendeciaQuant.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em xlsx")


            if intervaloTimeCPUE:
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
                        indicadorInfo = ['CPUE kg/dia', 'KgTotal']
                        for indSA in indicadorInfo:
                            dict_tendQ['indicador'] = indSA + '_periodo'
                            dict_pQ['indicador'] = indSA + '_periodo' 
                            for mdist in lst_distGasPla:
                                df_dist = copy.deepcopy(dfinterval[dfinterval[mdist] == True])    
                                df_dist = df_dist.sort_values(by='Data Chegada')                       
                                sizeTab = df_dist.shape[0]                               
                                
                                if sizeTab > 2:
                                    print("    calculando tendencia   ")
                                    result_tend, result_p = get_analise_Kendall (df_dist, indSA)
                                    dict_tendQ[mdist] = dictTendencia[result_tend]
                                    
                                    print("show tendencia result > ", result_tend, " | p-value ", result_p)
                                    if  result_p < 0.05:
                                        dict_pQ[mdist] = 'significativo'                        
                                    else:
                                        dict_pQ[mdist] = 'não significativo'     

                                    dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                                    dict_pQ['Quant_' + mdist] = df_dist.shape[0]         
                                
                                else: 
                                    dict_tendQ['Quant_' + mdist] = df_dist.shape[0]
                                    dict_pQ['Quant_' + mdist] = df_dist.shape[0]           
                                    dict_tendQ[mdist] = 'sem info'
                                    dict_pQ[mdist] = 'sem info'


                            df_tendQ = pd.DataFrame([dict_tendQ])
                            df_pQ = pd.DataFrame([dict_pQ])

                            df_tendeciaQuant = pd.concat([df_tendeciaQuant, df_tendQ, df_pQ], axis= 0, ignore_index=True)
                            

                # sys.exit()
                print("data frame de tendencias ")
                print(df_tendeciaQuant.head())
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_3_new_PERIODOS_CPUE_KG_TENDENCIA_QUANT{tiname}_{nameSub}_from_08_09_2023.csv"
                path_saveTendencia = os.path.join(path, path_saveTendencia)
                df_tendeciaQuant.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em format csv")


            if frequenceSerieRendaM:  
                # date_string = "2023-09-01 14:30:00.123"
                date_format = "%d-%m-%Y"
                dict_tendQ['intervalo'] = 'todaSerie'
                dict_pQ['intervalo'] = 'todaSerie'  
                dict_tendQ['indicador'] = 'Renda_Media'
                dict_pQ['indicador'] = 'Renda_Media'
                dict_tendQ['Quantidade'] = df_subArte.shape[0]
                dict_pQ['Quantidade'] = df_subArte.shape[0]

                
                for mdist in lst_distGasPla:
                    df_dist = copy.deepcopy(df_subArte[df_subArte[mdist] == True])                                   
                    # print(f"shape  ofd distance {mdist} is {df_dist.shape[0]}")
                    # print(df_dist[['SubArte', 'TI', 'Data Chegada','R$Total', mdist]].head(20))
                    # df_dist[['SubArte', 'TI', 'Data Chegada','R$Total', mdist]].to_csv(f"testando distancia_{mdist}.csv")
                    if df_dist.shape[0] > 0:
                        # reagrupando por 
                        df_quantidade = building_serie_Renda_mensal(df_dist)
                        totalReg = df_quantidade.shape[0]  # total de registros 
                        print("-*-*-*-*-*-* PROCESSING TRENDING -*-*-*-*-*-*")
                        print("===>  ", df_quantidade.shape[0] , "  <====== ")      
                        # print(df_quantidade.head(20))  
                        # df_quantidade.to_csv(f'quantidade_renda_mensal_{mdist}.csv')
                        
                        dict_tendQ['Qrm_' + mdist] = int(totalReg)
                        dict_pQ['Qrm_' + mdist] = int(totalReg)

                        # df_quantidade = df_quantidade.sort_values(by='year')
                        sizeTab = df_quantidade.shape[0]                

                        if sizeTab > 3:
                            print("  >>>>>>  calculando tendencia  <<<<<<<<< ")
                            result_tend, result_p = get_analise_Kendall(df_quantidade,'RM') 
                            dict_tendQ[mdist] = dictTendencia[result_tend]
                            print("show tendencia result ", result_tend, " ", result_p)
                            if  result_p < 0.05:
                                dict_pQ[mdist] = 'significativo'                        
                            else:
                                dict_pQ[mdist] = 'não significativo'                                  
                        
                        else:                                       
                            dict_tendQ[mdist] = 'sem informacao'
                            dict_pQ[mdist] = 'sem informacao'
                            
                    else:     
                        dict_tendQ['Qrm_' + mdist] = int(df_dist.shape[0])
                        dict_pQ['Qrm_' + mdist] = int(df_dist.shape[0])        
                        dict_tendQ[mdist] = 'sem informacao'
                        dict_pQ[mdist] = 'sem informacao'                       

                df_tendQ = pd.DataFrame([dict_tendQ])
                df_pQ = pd.DataFrame([dict_pQ])

                df_tendeciaQuant = pd.concat([df_tendeciaQuant, df_tendQ, df_pQ], axis= 0, ignore_index=True)
                # sys.exit()
                print("data frame de tendencias ")
                print(df_tendeciaQuant.head())
                path_saveTendencia = f"tables_Out_2023/tendecias/tabela_new_RENDA_MEDIA_MENSAL_INT_DISTANCIA_TENDENCIA_{tiname}_QUANT_{nameSub}_08_09_2023.csv"
                path_saveTendencia = os.path.join(path, path_saveTendencia)
                df_tendeciaQuant.to_csv(path_saveTendencia, index=False)
                print("tabela de tendencias salvas em xlsx")


    dictComun[tiname] = dictComTI
            
print(" ")
print("---------------------------------------------------------")

# if makeTrends:
#     print("data frame de tendencias ")
#     print( df_tendecia )
#     path_saveTendencia = "NewPlotsAgost/tabela_tendenciaIndicadores_gasoduto_06_08_2023.xlsx"
#     df_tendecia.to_excel(path_saveTendencia)
#     print("tabela de tendencias salvas em xlsx")

if knowComunidades:
    for TI, dictsubA in dictComun.items():
        for subA, lstCom in dictsubA.items():
            print("--------------------------")
            print("TI => ", TI , '  subArte = ', subA)        
            print(lstCom)
            print("********************************")
            print(" ")