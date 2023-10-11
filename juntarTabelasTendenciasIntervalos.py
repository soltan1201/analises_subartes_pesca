import pandas as pd
import os 
import glob

ocorrencia = False
intervalo_freq = False
periodoCPUE = False
tendencia5KM = False
raioPesqueiro = False
raioDistPesqueiro = False
intervPesq = False
rendamediamensal = True
anguloCPUE = False
intervalAnguiloCPUE = False

path_saveTendencia = ''
nameTabela = 'tabela_OCURRENCIA_TENDENCIA'
if intervalo_freq == True:
    procura = 'INTERVALO'
elif periodoCPUE:
    procura = '3PERIODOS_CPUE'
elif tendencia5KM:
    procura = 'Tendencia_5KM'
elif raioPesqueiro:
    procura = 'RAIO_PESQUEIRO'
elif intervPesq:
    procura = 'INTERVALO_PESQUEIRO'
elif rendamediamensal:
    procura = 'new_RENDA_MEDIA_MENSAL_INT'
elif ocorrencia:
    procura = "OCURRENCIA"
elif raioDistPesqueiro:
    procura = 'INTERVALO_DISTANCIA_RAIO_PESQUEIRO'
elif anguloCPUE:
     procura = 'angulo_Tendencia'
elif intervalAnguiloCPUE:
    procura = 'angulo_INTEVALO_CPUE'


folder = "tables_Out_2023/tendecias"
# folder = "tables_Out_2023/tendenciasInd"
# folder = "plotsAgos23/tedenciasOcur"

if "tendenciasInd" in folder:   
    print("indicadores ")
    path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_3_Indicador_CPUE_Serie_TENDENCIA_05_10_2023.xlsx"
    nameTabela = 'tabela_Tendencia_5KM_Indicador'

elif "tedenciasOcur" in folder:    
    print(" ocurrencias ")
    path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_3_Ocurrencia_Serie_TENDENCIA_05_10_2023_update.xlsx"
    nameTabela = 'tabela_OCURRENCIA_TENDENCIA'
else:
    print(" Intervaloes ")
    # if procura == '3PERIODOS_CPUE':
    #     nameTabela = 'tabela_3PERIODOS_CPUE_TENDENCIA'
    #     path_saveTendencia = f"plotsAgos23/tendenciasXLSX/tabela_3_PERIODOS_Serie_CPUE_TENDENCIA_08_09_2023_updateV3.xlsx"

    if procura == '3PERIODOS_CPUE':
        nameTabela = 'tabela_3_new_PERIODOS_CPUE_KG_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_3_new_PERIODOS_Serie_CPUE_KG_TENDENCIA_05_10_2023_updateV3.xlsx"

    elif procura == 'OCURRENCIA':
        nameTabela = 'OCURRENCIA_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_Ocurrencia_Serie_TENDENCIA_Maior5KM_05_10_2023_update.xlsx"
    
    elif procura == 'INTERVALO':
        nameTabela = 'INTERVALO_NEW_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_INTERVALOS_05-07_TENDENCIA_05_10_2023_updateV3.xlsx"

    elif procura == 'Tendencia_5KM':
        nameTabela = 'tabela_Tendencia_5KM_Indicado'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_mais_5KM_INDICADOR_Serie_TENDENCIA_05_10_2023_update.xlsx" 

    elif procura == 'RAIO_PESQUEIRO':
        nameTabela = 'INTERVALO_NEW_RAIO_PESQUEIRO_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_INTERVALO_NEW_RAIO_PESQUEIRO_TENDENCIA_05_10_2023_update.xlsx"     

    elif procura == 'INTERVALO_PESQUEIRO':
        nameTabela = 'tabela_INTERVALO_NEW_PESQUEIRO_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_INTERVALO_NEW_FREQUENCE_PESQUEIRO_TENDENCIA_05_10_2023_update.xlsx"    
    
    elif procura == 'new_RENDA_MEDIA_MENSAL_INT':
        nameTabela = '_new_RENDA_MEDIA_MENSAL_INT_DISTANCIA_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_new_RENDA_MEDIA_MENSAL_INT_DISTANCIA_TENDENCIA_05_10_2023_update.xlsx"

    elif procura == 'INTERVALO_DISTANCIA_RAIO_PESQUEIRO':
        nameTabela = 'INTERVALO_DISTANCIA_RAIO_PESQUEIRO_TENDENCIA'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_INTERVALO_DISTANCIA_RAIO_PESQUEIRO_05_10_2023_update.xlsx"
    
    elif procura == 'angulo_Tendencia':
        nameTabela = 'tabela_angulo_Tendencia_Indicador_CPUE'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_magnitude_angulo_Tendencia_Indicador_CPUE_05_10_2023_update.xlsx"

    elif procura == 'angulo_INTEVALO_CPUE':
        nameTabela = 'tabela_angulo_INTEVALO_05-07_Tendencia'
        path_saveTendencia = f"tables_Out_2023/tendenciasXLSX/tabela_magnitude_angulo_INTEVALO_05-07__Tendencia_CPUE_05_10_2023.xlsx"
    

nfiles = glob.glob(folder + '/*.csv')
lstDF = []
for cc, nfile in enumerate(nfiles):
    if nameTabela in nfile:
        print(nfile)
        dfCSV = pd.read_csv(nfile)
        print(dfCSV.head(2))
        lstDF.append(dfCSV)

dfConcat =  pd.concat(lstDF)

print(dfConcat.head(10))
dfConcat.to_excel(path_saveTendencia)  # , index=False
