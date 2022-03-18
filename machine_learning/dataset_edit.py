'''
se si esegue questo script, per evitare ripetizioni di dati, è prima necessario cancellare:
- i file 'discrimination.txt' e 'neutral.txt', sia all'interno della cartella del dataset weakly labeled che nella
    cartella del dataset well labeled;
- i contenuti delle cartelle discrimination e neutral all'interno di train e di test, sia per il dataset weakly labeled
    che per quello well labeled;
'''

import re
import pandas as pd


# cancella alcuni caratteri non ascii e li trasforma in ascii
def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


# i tweet del dataset weakly labeled vengono divisi in due file .txt in base all'etichetta
file_path_weakly_discrimination = 'dataset\\dataset_weakly_labeled\\discrimination.txt'
file_path_weakly_neutral = 'dataset\\dataset_weakly_labeled\\neutral.txt'

# file aperti in modalità append (su ogni riga si troverà un tweet)
file_weakly_discrimination = open(file_path_weakly_discrimination, "a")
file_weakly_neutral = open(file_path_weakly_neutral, "a")

# i tweet del dataset well labeled vengono divisi su due file .txt in base all'etichetta
file_path_well_discrimination = 'dataset\\dataset_well_labeled\\discrimination.txt'
file_path_well_neutral = 'dataset\\dataset_well_labeled\\neutral.txt'

# file aperti in modalità append (su ogni riga si troverà un tweet)
file_well_discrimination = open(file_path_well_discrimination, "a")
file_well_neutral = open(file_path_well_neutral, "a")


'''
analizzo tutti i tweet del dataset, sostituendo eventuali abbreviazioni, acronimi e/o caratteri unicode
id indica di quale dataset si tratta;
file_d e file_n sono rispettivamente i file .txt di dati discriminatori e dati neutrali, uno per ogni riga
'''
def fixing_dataset(dataframe, id, file_d, file_n):
    # contatori
    discriminatory = 0
    neutral = 0

    # variabili usate per dare il nome ai file discriminatori e neutrali usati in [prediction]
    prediction_d = 1
    prediction_n = 1

    # si scorrono tutte le righe del dataframe, sostituendo abbreviazioni, acronimi, caratteri unicode...
    for i, row in dataframe.iterrows():
        row["tweet"] = strip_non_ascii(row["tweet"])
        row["tweet"] = row["tweet"].lower()
        row["tweet"] = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                              row["tweet"])
        row["tweet"] = re.sub(r',', '', row["tweet"])
        row["tweet"] = re.sub(r'\bthats\b', 'that is', row["tweet"])
        row["tweet"] = re.sub(r'\bcuz\b', 'because', row["tweet"])
        row["tweet"] = re.sub(r'\bluv\b', 'love', row["tweet"])
        row["tweet"] = re.sub(r'\bu\b', 'you', row["tweet"])
        row["tweet"] = re.sub(r'\by\b', 'why', row["tweet"])
        row["tweet"] = re.sub(r'\bistg\b', 'i swear to god', row["tweet"])
        row["tweet"] = re.sub(r'\bgr8\b', 'great', row["tweet"])
        row["tweet"] = re.sub(r'\bbc\b', 'because', row["tweet"])
        row["tweet"] = re.sub(r'\baf\b', 'as fuck', row["tweet"])
        row["tweet"] = re.sub(r'\bive\b', 'i have', row["tweet"])
        row["tweet"] = re.sub(r'\bim\b', 'i am', row["tweet"])
        row["tweet"] = re.sub(r'\bbihday\b', 'birthday', row["tweet"])
        row["tweet"] = re.sub(r'\bidgaf\b', "i don't give a fuck", row["tweet"])
        row["tweet"] = re.sub(r'\bya\b', 'yeah', row["tweet"])
        row["tweet"] = re.sub(r'\bcant\b', 'can not', row["tweet"])
        row["tweet"] = re.sub(r'\bits\b', 'it is', row["tweet"])
        row["tweet"] = re.sub(r'\bwont\b', 'will not', row["tweet"])
        row["tweet"] = re.sub(r'\bthats\b', "that's", row["tweet"])
        row["tweet"] = re.sub(r'\bid\b', 'i would', row["tweet"])
        row["tweet"] = re.sub(r'\bwth\b', 'what the hell', row["tweet"])
        row["tweet"] = re.sub(r'\br\b', 'are', row["tweet"])
        row["tweet"] = re.sub(r'\bu\b', 'you', row["tweet"])
        row["tweet"] = re.sub(r'\bk\b', 'OK', row["tweet"])
        row["tweet"] = re.sub(r'\bsux\b', 'sucks', row["tweet"])
        row["tweet"] = re.sub(r'\bno+\b', 'no', row["tweet"])
        row["tweet"] = re.sub(r'\bcoo+\b', 'cool', row["tweet"])
        row["tweet"] = re.sub(r'\bb\b', 'be', row["tweet"])
        row["tweet"] = re.sub(r'\bdoesnt\b', 'does not', row["tweet"])
        row["tweet"] = re.sub(r'\blookin\b', 'looking', row["tweet"])
        row["tweet"] = re.sub(r'\bjk\b', 'just kidding', row["tweet"])
        row["tweet"] = re.sub(r'\bomg\b', 'oh my god', row["tweet"])
        row["tweet"] = re.sub(r'\bomfg\b', 'oh my fucking god', row["tweet"])
        row["tweet"] = re.sub(r'\bimo\b', 'in my opinion', row["tweet"])
        row["tweet"] = re.sub(r'\bsmh\b', 'shaking my head', row["tweet"])
        row["tweet"] = re.sub(r'\bsmfh\b', 'shaking my fucking head', row["tweet"])
        row["tweet"] = re.sub(r'\bikr\b', 'i know right', row["tweet"])
        row["tweet"] = re.sub(r'\byall\b', 'you all', row["tweet"])
        row["tweet"] = re.sub(r"\by'all\b", 'you all', row["tweet"])
        row["tweet"] = re.sub(r'\bidk\b', "i don't know", row["tweet"])
        row["tweet"] = re.sub(r'\bbtw\b', 'by the way', row["tweet"])
        row["tweet"] = re.sub(r'\btbh\b', 'to be honest', row["tweet"])
        row["tweet"] = re.sub(r'\boomf\b', 'one of my followers', row["tweet"])
        row["tweet"] = re.sub(r'\brt\b', '', row["tweet"])
        row["tweet"] = re.sub(r'\brly\b', 'really', row["tweet"])
        row["tweet"] = re.sub(r'\bppl\b', 'people', row["tweet"])
        row["tweet"] = re.sub(r'\bgf\b', 'girlfriend', row["tweet"])
        row["tweet"] = re.sub(r'\bbf\b', 'boyfriend', row["tweet"])
        row["tweet"] = re.sub(r'wtf', 'what the fuck', row["tweet"])
        row["tweet"] = re.sub(r'lol', 'laughing out loud', row["tweet"])
        row["tweet"] = re.sub(r'lmao', 'laughing my ass off', row["tweet"])
        row["tweet"] = re.sub(r'w/', 'with', row["tweet"])
        row["tweet"] = re.sub(r'&lt;3+', '', row["tweet"])
        row["tweet"] = re.sub(r'&#39', "'", row["tweet"])
        row["tweet"] = re.sub(r'&gt;', '>', row["tweet"])
        row["tweet"] = re.sub(r'&amp;', '&', row["tweet"])
        row["tweet"] = re.sub(r'!+', '', row["tweet"])
        row["tweet"] = re.sub(r'&#[0-9]+;', '', row["tweet"])
        row["tweet"] = re.sub(r'#', '', row["tweet"])
        row["tweet"] = re.sub('@[a-z0-9_:]*', '', row["tweet"])

        # il tweet memorizzato nella riga corrente è stato etichettato come discriminatorio
        if row["label"] == '1' or row["label"] == 1:
            # alla fine del file discriminatorio viene aggiunto il tweet corrente e aggiornato il contatore opportuno
            file_d.write(row["tweet"].strip() + '\n')
            discriminatory += 1
        # il tweet memorizzato nella riga corrente è stato etichettato come neutrale
        else:
            # sto considerando il dataframe corrispondente al dataset weakly labeled
            if id == 0:
                '''
                controllo che il numero di tweet neutrali sia pari a quello dei discriminatori (ovvero 2242)
                in modo da mantenerli in numero uguale
                '''
                if neutral < 2242:
                    # alla fine del file neutrale viene aggiunto il tweet corrente e aggiornato il contatore opportuno
                    file_n.write(row["tweet"].strip() + '\n')
                    neutral += 1
                # ignoro i tweet in più (non necessari)
                else:
                    continue
            # sto considerando il dataframe corrispondente al dataset well labeled (id = 1)
            else:
                # alla fine del file neutrale viene aggiunto il tweet corrente e aggiornato il contatore opportuno
                file_n.write(row["tweet"].strip() + '\n')
                neutral += 1

        ''''
        creo un file per ogni tweet discriminatorio e un file per ogni tweet neutrale
        in base al parametro id capisco se sto considerando il dataset weakly o well labeled
        in base al valore dei contatori prediction_d e prediction_n divido i tweet tra train e test
        train e test sono suddivisi a loro volta in discrimination e neutral
        '''
        # il tweet memorizzato nella riga corrente è stato etichettato come discriminatorio
        if row["label"] == 1 or row["label"] == '1':
            # sto considerando il dataframe corrispondente al dataset weakly labeled
            if id == 0:
                '''
                ho diviso il dataset (file totali 4484) in 80% train (3588 file) e 20% test (896 file)
                a loro volta: il train è suddiviso in 1794 file discriminatori e 1794 file neutrali;
                il test è suddiviso in 448 file discriminatori e 448 file neutrali
                '''
                if prediction_d <= 1794:
                    file_path_weakly_train_discrimination = 'dataset\\dataset_weakly_labeled\\train\\discrimination\\' \
                                                            + str(prediction_d) + '.txt'

                    # creo un file .txt (dataset weakly labeled -> train -> discrimination) in cui memorizzo il tweet
                    file = open(file_path_weakly_train_discrimination, "w")
                    file.write(row["tweet"].strip())
                    file.close()
                else:
                    file_path_weakly_test_discrimination = 'dataset\\dataset_weakly_labeled\\test\\discrimination\\' \
                                                           + str(prediction_d) + '.txt'

                    # creo un file .txt (dataset weakly labeled -> test -> discrimination) in cui memorizzo il tweet
                    file = open(file_path_weakly_test_discrimination, "w")
                    file.write(row["tweet"].strip())
                    file.close()

                # aggiorno il contatore dei discriminatori
                prediction_d += 1

            # sto considerando il dataframe corrispondente al dataset well labeled
            else:
                '''
                ho diviso il dataset (file totali 1694) in 80% train (1356 file) e 20% test (338 file)
                a loro volta: il train è suddiviso in 678 file discriminatori e 678 file neutrali;
                il test è suddiviso in 169 file discriminatori e 169 file neutrali
                '''
                if prediction_d <= 678:
                    file_path_well_train_discrimination = 'dataset\\dataset_well_labeled\\train\\discrimination\\' \
                                                          + str(prediction_d) + '.txt'

                    # creo un file .txt (dataset well labeled -> train -> discrimination) in cui memorizzo il tweet
                    file = open(file_path_well_train_discrimination, "w")
                    file.write(row["tweet"].strip())
                    file.close()
                else:
                    file_path_well_test_discrimination = 'dataset\\dataset_well_labeled\\test\\discrimination\\' \
                                                         + str(prediction_d) + '.txt'

                    # creo un file .txt (dataset well labeled -> test -> discrimination) in cui memorizzo il tweet
                    file = open(file_path_well_test_discrimination, "w")
                    file.write(row["tweet"].strip())
                    file.close()

                # aggiorno il contatore dei discriminatori
                prediction_d += 1
        # il tweet memorizzato nella riga corrente è stato etichettato come neutrale
        else:
            # sto considerando il dataframe corrispondente al dataset weakly labeled
            if id == 0:
                # controllo che il numero di tweet neutrali sia pari a quello dei discriminatori
                if prediction_n <= 2242:
                    if prediction_n <= 1794:
                        file_path_weakly_train_neutral = 'dataset\\dataset_weakly_labeled\\train\\neutral\\' \
                                                         + str(prediction_n) + '.txt'

                        # creo un file .txt (dataset weakly labeled -> train -> neutral) in cui memorizzo il tweet
                        file = open(file_path_weakly_train_neutral, "w")
                        file.write(row["tweet"].strip() + '\n')
                        file.close()
                    else:
                        file_path_weakly_test_neutral = 'dataset\\dataset_weakly_labeled\\test\\neutral\\' \
                                                        + str(prediction_n) + '.txt'

                        # creo un file .txt (dataset weakly labeled -> test -> neutral) in cui memorizzo il tweet
                        file = open(file_path_weakly_test_neutral, "w")
                        file.write(row["tweet"].strip() + '\n')
                        file.close()

                    # aggiorno il contatore dei neutrali
                    prediction_n += 1
                # ignoro i tweet non necessari (quelli in più)
                else:
                    continue
            # sto considerando il dataframe corrispondente al dataset well labeled
            else:
                if prediction_n <= 678:
                    file_path_well_train_neutral = 'dataset\\dataset_well_labeled\\train\\neutral\\' \
                                                   + str(prediction_n) + '.txt'

                    # creo un file .txt (dataset well labeled -> train -> neutral) in cui memorizzo il tweet
                    file = open(file_path_well_train_neutral, "w")
                    file.write(row["tweet"].strip() + '\n')
                    file.close()
                else:
                    file_path_well_test_neutral = 'dataset\\dataset_well_labeled\\test\\neutral\\' \
                                                  + str(prediction_n) + '.txt'

                    # creo un file .txt (dataset well labeled -> test -> neutral) in cui memorizzo il tweet
                    file = open(file_path_well_test_neutral, "w")
                    file.write(row["tweet"].strip() + '\n')
                    file.close()

                # aggiorno il contatore dei neutrali
                prediction_n += 1

    print("id: ", id)
    print("discriminatory: ", discriminatory)
    print("neutral: " + str(neutral) + "\n")


# memorizzo il contenuto dei file .csv nei dataframe
data_weakly_labeled = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati'
                                  r'\detecting_hate_tweets\train.csv')
data_well_labeled = pd.read_csv(r'C:\Users\angel\Desktop\tirocinio\ProgettoTesi\dataset_utilizzati\well-labeled'
                                r'\dataset_well_labeled.csv')

fixing_dataset(data_weakly_labeled, 0, file_weakly_discrimination, file_weakly_neutral)
fixing_dataset(data_well_labeled, 1, file_well_discrimination, file_well_neutral)

file_weakly_discrimination.close()
file_weakly_neutral.close()

file_well_discrimination.close()
file_well_neutral.close()

print("ok")
