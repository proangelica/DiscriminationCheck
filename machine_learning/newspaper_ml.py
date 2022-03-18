import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV

# la funzione si occupa dello split del dataset in train e test
def train_test_generator(root):
    # array che contiene la rappresentazione di ogni tweet
    X = []

    # array di label, ognuna corrispondente al tweet memorizzato nella stessa posizione in X
    y = []

    # mi occupo dei tweet (uno per ogni riga) del file discrimination aggiungendoli in X
    path_discrimination = os.path.abspath(root + "discrimination.txt")
    with open(path_discrimination, 'r', encoding="utf8") as f:
        lines_f = f.readlines()
        for line in lines_f:
            X.append(line)
            y.append('discrimination')

    # mi occupo dei tweet (uno per ogni riga) del file neutral aggiungendo anch'essi in X
    path_neutral = os.path.abspath(root + "neutral.txt")
    with open(path_neutral, 'r', encoding="utf8") as f:
        lines_f = f.readlines()
        for line in lines_f:
            X.append(line)
            y.append('neutral')

    # si lavora usando la vettorizzazione Tf-idf che va a vedere la frequenza delle parole nelle frasi che compongono il dataset
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # encoder oggetto utilizzato per la codifica
    label_encoder = LabelEncoder()
    # non considero le label 'discrimination' o 'neutral', ma esse vengono trasformate in 0 e 1
    integer_encoded = label_encoder.fit_transform(y)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), )

    # prende la lista di tweet e le corrispondenti label e crea un training set (80%) e un test set (20%)
    training_set_data,test_set_data,training_set_labels,test_set_labels = train_test_split(X,integer_encoded,train_size=0.8,stratify=integer_encoded)

    return training_set_data, test_set_data, training_set_labels, test_set_labels, label_encoder, vectorizer


# funzione utilizzata per l'addestramento del modello
def grid_search_cv(train_set_data, test_set_data, train_set_labels, test_set_labels, label_encoder, vectorizer):
    # con la funzione len si ottiene il numero di elementi che fanno parte di un oggetto
    # con la funzione set si converte qualsiasi elemento iterabile in una sequenza di elementi iterabili distinti
    # in questo modo, si ottiene il numero di elementi distinti all'interno delle label del dataset train
    n_genes = len(set(train_set_labels))

    '''''
    # Create the parameter grid based on the results of random search (necessario per random forest)
    param_grid = {
        'bootstrap': [True],
        'max_depth': [80, 100],
        'max_features': [2, 3],
        'min_samples_leaf': [1, 3],
        'min_samples_split': [8, 10],
        'n_estimators': [50, 100, 200]
    }
    '''

    # crea la griglia di parametri (o parameter grid) per il classificatore MultinomialNB
    # i parametri cambiano a seconda del modello e possono assumere un numero discreto di valori
    param_grid = {
        'alpha': [0.01, 0.1, 0.5, 1.0, 10.0]
    }

    # si crea il classificatore
    nb = MultinomialNB()

    '''''
    si istanzia il grid search model che esegue una ricerca esauriente sui valori dei parametri specificati per un classificatore
    estimator è il classificatore
    param_grid la griglia dei parametri specificata sopra
    cv determina la strategia di suddivisione della K-fold cross validation (di default  K = 5)
    n_jobs specifica il numero di lavori da eseguire in parallelo (-1 indica di utilizzare tutti i processori)
    verbose=2 indica che viene visualizzato il tempo di calcolo per ogni suddivisione e il parametro candidato
    '''''
    grid_search = GridSearchCV(estimator=nb, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

    # esegue il fit adattando la grid search ai dati e stampa i parametri che hanno dato i migliori risultati
    grid_search.fit(train_set_data, train_set_labels)
    print(grid_search.best_params_)

    # lo stimatore scelto dalla ricerca, che ha dato il punteggio più alto sui dati esclusi
    best_grid = grid_search.best_estimator_

    # viene effettuata nuovamente la trasformazione da intero a stringa
    labels_originarie = label_encoder.inverse_transform(np.arange(n_genes))
    # si effettua la previsione sul dataset di test
    y_pred = best_grid.predict(test_set_data)

    # Classification report -> mostra le varie metriche (accuracy, precision, recall, F1-score) riferite all'esecuzione del modello
    clsf = classification_report(test_set_labels, y_pred, target_names=labels_originarie, output_dict=True)
    clsf_report = pd.DataFrame(data=clsf).transpose()
    csv_name = "classification_report_discrimination.csv"
    clsf_report.to_csv(csv_name, index=True)

    '''''
    salvataggio classificatore Pickle:
    - modello migliore selezionato precedentemente
    - encoder per la codifica/decodifica delle etichette
    - "vettorizzatore" utilizzato in precedenza sui dati del dataset
    '''''
    pickle.dump([best_grid, label_encoder, vectorizer], open("discrimination_NB_well.pickle", 'wb'))
    # pickle.dump([best_grid, label_encoder, vectorizer], open("discrimination_NB_weakly.pickle", 'wb'))

    # Confusion matrix -> dice quanto funziona bene il modello
    # viene mostrata la classificazione corretta e sbagliata (effettuata dal modello) per ogni label
    confmat = confusion_matrix(y_true=test_set_labels, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(confmat.shape[0]):
        for j in range(confmat.shape[1]):
            ax.text(x=j, y=i, s=confmat[i, j], va='center', ha='center')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.show()


if __name__ == "__main__":
    # creazione dataset
    train_scaled_D, test_scaled_D, training_set_labels, test_set_labels, label_encoder, vectorizer = train_test_generator("dataset/dataset_well_labeled/")
    # train_scaled_D, test_scaled_D, training_set_labels, test_set_labels, label_encoder, vectorizer = train_test_generator("dataset/dataset_weakly_labeled/")

    # K-fold cross validation (una procedura utilizzata per stimare l'abilità del modello su nuovi dati)
    grid_search_cv(train_scaled_D, test_scaled_D, training_set_labels, test_set_labels, label_encoder, vectorizer)
