'''
se si esegue questo script, per evitare ripetizioni di dati, è prima necessario cancellare il dataset well labeled
(file dataset_well_labeled.csv nella cartella dataset_utilizzati) perchè esso viene creato e riempito automaticamente dallo script
'''

import re
import pandas as pd


# cancella alcuni caratteri non ascii e li trasforma in ascii
def strip_non_ascii(string):
    stripped = (character for character in string if 0 < ord(character) < 127)
    return ''.join(stripped)


'''''
funzione utilizzata per unire tutti i vari tweet raccolti (sia discriminatori che neutrali) in un unico file .csv
suddiviso su 3 colonne: id, label, tweet
'''''
def dataset_union(dataframe, file_csv, counter, label, indice):
    # analizzo tutte le righe del dataframe
    for i, row in dataframe.iterrows():
        # considero il dataframe 5 e ignoro tutti i tweet non neutrali
        if indice== 5:
            if row["isHate"] != 0.0:
                continue

        # considero il dataframe 6 e ignoro tutti i tweet non neutrali e non necessari
        if indice == 6:
            if row["tagging"] == 0:
                row["tweet"] = re.sub('ass+', '', row["tweet"])
                row["tweet"] = re.sub('damn', '', row["tweet"])
                row["tweet"] = re.sub('fuck+', '', row["tweet"])
                row["tweet"] = re.sub('fucking', '', row["tweet"])
                row["tweet"] = re.sub('"+', '', row["tweet"])

        # eseguita la funzione per la sostituzione di caratteri non ascii
        row["tweet"] = strip_non_ascii(row["tweet"])

        '''
        siccome nel dataframe 5 il separatore è ';' e non ',' sostituisco queste ultime con degli spazi, 
        per non avere problemi con la formattazione
        '''
        row["tweet"] = re.sub(',', '', row["tweet"])

        '''
        counter viene aggiornato ad ogni riga letta, per questo motivo rappresenta un id univoco;
        se label = 1 -> il dataset esaminato è discriminatorio (e di conseguenza anche il testo memorizzato nella riga corrente), 
        altrimenti (label = 0) -> il dataset esaminato è neutrale (e anche il testo della riga corrente)
        memorizzo nel dataset il testo della riga corrente
        '''
        file_csv.write(str(counter) + ',' + str(label) + ',' + row["tweet"].strip() + '\n')

        counter += 1

    return counter


# definisco il nome e il path del file .csv che conterrà il dataset well labeled (creato da me)
file_path = 'C:\\Users\\angel\\Desktop\\tirocinio\\ProgettoTesi\\dataset_utilizzati\\well-labeled' \
            '\\dataset_well_labeled.csv '

# dataframe contenenti tweet discriminatori raccolti, analizzati e modificati personalmente da me
data1 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\detecting_hate_tweets\train'
                    r'-discriminatory.csv')
data2 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\ethos\Ethos_Dataset_Binary'
                    r'-discriminatory.csv')
data3 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\HSandOffensive\hate-speech-and'
                    r'-offensive-language-discriminatory.csv')
data4 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\CR\Dataset_Discrimination_CR.csv',
                    encoding='cp1252')

# dataframe contenenti tweet neutrali per la costruzione del dataset
data5 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\ethos\Ethos_Dataset_Binary.csv',
                    sep=';')
data6 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\suspicious'
                    r'\Suspicious_Communication_on_Social_Platforms-neutral.csv')
data7 = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\CR\Dataset_Neutral_CR_OK.csv')


# apro il file in modalità append
file = open(file_path, "a")
# definisco le colonne di cui sarà composto il dataset
file.write("id,label,tweet\n")

c = 1

c = dataset_union(data1, file, c, 1, 1)
print("dataset train-discriminatory ok")

c = dataset_union(data2, file, c, 1, 2)
print("dataset ethos-discriminatory ok")

c = dataset_union(data3, file, c, 1, 3)
print("dataset HS and offensive language-discriminatory ok")

c = dataset_union(data4, file, c, 1, 4)
print("dataset CR-discriminatory ok")

c = dataset_union(data5, file, c, 0, 5)
print("dataset ethos-neutral ok")

c = dataset_union(data6, file, c, 0, 6)
print("dataset suspicious-neutral ok")

c = dataset_union(data7, file, c, 0, 7)
print("dataset CR-neutral ok")

file.close()
