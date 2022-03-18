'''
se si esegue questo script, per evitare ripetizioni di dati, è prima necessario:
- cancellare il file 'testing weakly-labeled' e commentare la sezione di codice in cui viene aperto il file e quella in
    cui viene caricato il dataset well labeled [in questo modo i modelli implementati verranno addestrati e testati sul
    dataset weakly labeled];
- cancellare il file 'testing well-labeled' e commentare la sezione di codice in cui viene aperto il file e quella in
    cui viene caricato il dataset weakly labeled [in questo modo i modelli implementati verranno addestrati e testati sul
    dataset well labeled];
'''

import time

import metrics as metrics
import numpy as np
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression


# funzione in cui si addestrano i modelli, si testano su una frase data in input e si memorizzano le prestazioni di ognuno
def training_model(model, train, test, file, name):
    start_time = time.time()

    # fit è la funzione usata per addestrare il modello
    # gli attributi 'data' e 'target' indicano rispettivamente i dati e le etichette (in questo caso, del dataset train)
    model.fit(train.data, train.target)
    # predict è la funzione usata per testare il modello appena costruito sui dati di test
    # predicted_categories conterrà le categorie che si ottengono dalla previsione effettuata dal modello
    predicted_categories = model.predict(test.data)

    res = str(predictions("this is a test", model, train))
    print(name + res)

    print("time: " + str(time.time() - start_time) + " seconds\n")

    # le metriche sono utilizzate per valutare il modello
    accuracy = metrics.accuracy_score(test.target, predicted_categories)
    # average='weighted' indica che le metriche sono calcolate per ogni etichetta, così come la loro media ponderata in base al numero di istanze vere per ogni etichetta
    precision = metrics.precision_score(test.target, predicted_categories, average='weighted')
    recall = metrics.recall_score(test.target, predicted_categories, average='weighted')
    F1score = metrics.f1_score(test.target, predicted_categories, average='weighted')

    file.write(name + ', ' + str(accuracy) + ', ' + str(precision) + ', ' + str(recall) + ', ' + str(F1score) + '\n')


'''
a partire da una frase e da un classificatore viene effettuata la predizione e restituita
la categoria a cui la frase appartiene
'''
def predictions(headline, classifier, data_train):
    # le categorie sono le stesse sia per train che per test e sono rappresentate da indici interi
    # a ogni indice corrisponde un nome ('discrimination' o 'neutral')
    all_categories_names = np.array(data_train.target_names)
    # si effettua la previsione su una certa frase data in input
    prediction = classifier.predict([headline])
    # si restituisce
    return all_categories_names[prediction]

'''''
# caricamento dataset weakly labeled
data_train = load_files(container_path='dataset\\dataset_weakly_labeled\\train', load_content=True,
                               encoding='utf-8')
data_test = load_files(container_path='dataset\\dataset_weakly_labeled\\test', load_content=True,
                              encoding='utf-8')
file = open('testing_weakly-labeled.csv', "a")
'''''

# caricamento dataset well labeled
data_train = load_files(container_path='dataset\\dataset_well_labeled\\train', load_content=True,
                             encoding='utf-8')
data_test = load_files(container_path='dataset\\dataset_weakly_labeled\\test', load_content=True,
                            encoding='utf-8')
file = open('testing_well-labeled.csv', "a")

'''
le pipeline sono un modulo di scikit-learn che permette di ottimizzare in maniera automatica e simultanea il processo di:
- normalizzazione dei dati
- ripulitura dei valori mancanti
- riduzione della dimensionalità
- classificazione
creando algoritmi partendo dalla combinazione di oggetti di base della libreria 
(ad esempio, gli algoritmi di machine learning e i metodi di vettorizzazione da applicare ai dati)
'''
RF_tfidf = make_pipeline(TfidfVectorizer(), RandomForestClassifier())
RF_count = make_pipeline(CountVectorizer(), RandomForestClassifier())
AdaBoost_tfidf = make_pipeline(TfidfVectorizer(), AdaBoostClassifier())
AdaBoost_count = make_pipeline(CountVectorizer(), AdaBoostClassifier())
NaiveBayes_tfidf = make_pipeline(TfidfVectorizer(), MultinomialNB())    # modello migliore
NaiveBayes_count = make_pipeline(CountVectorizer(), MultinomialNB())
svm_tfidf = make_pipeline(TfidfVectorizer(), LinearSVC())
svm_count = make_pipeline(CountVectorizer(), LinearSVC())
KNN_tfidf = make_pipeline(TfidfVectorizer(), KNeighborsClassifier())
KNN_count = make_pipeline(CountVectorizer(), KNeighborsClassifier())
DT_tfidf = make_pipeline(TfidfVectorizer(), DecisionTreeClassifier())
DT_count = make_pipeline(CountVectorizer(), DecisionTreeClassifier())
MLP_tfidf = make_pipeline(TfidfVectorizer(), MLPClassifier())
MLP_count = make_pipeline(CountVectorizer(), MLPClassifier())
LR_tfidf = make_pipeline(TfidfVectorizer(), LogisticRegression())
LR_count = make_pipeline(CountVectorizer(), LogisticRegression())

file.write("classifier, accuracy, precision, recall, F1-score\n")

if __name__ == '__main__':
    training_model(RF_tfidf, data_train, data_test, file, "RandomForest (Tf-idf)")
    training_model(RF_count, data_train, data_test, file, "RandomForest (Count)")
    training_model(AdaBoost_tfidf, data_train, data_test, file, "AdaBoost (Tf-idf)")
    training_model(AdaBoost_count, data_train, data_test, file, "AdaBoost (Count)")
    training_model(NaiveBayes_tfidf, data_train, data_test, file, "MultinomialNB (Tf-idf)")
    training_model(NaiveBayes_count, data_train, data_test, file, "MultinomialNB (Count)")
    training_model(svm_tfidf, data_train, data_test, file, "LinearSVC (Tf-idf)")
    training_model(svm_count, data_train, data_test, file, "LinearSVC (Count)")
    training_model(KNN_tfidf, data_train, data_test, file, "KNNeighbors (Tf-idf)")
    training_model(KNN_count, data_train, data_test, file, "KNeighbors (Count)")
    training_model(DT_tfidf, data_train, data_test, file, "DecisionTree (Tf-idf)")
    training_model(DT_count, data_train, data_test, file, "DecisionTree (Count)")
    training_model(MLP_tfidf, data_train, data_test, file, "Multi-layer Perceptron (MLP) (Tf-idf)")
    training_model(MLP_count, data_train, data_test, file, "Multi-layer Perceptron (MLP) (Count)")
    training_model(LR_tfidf, data_train, data_test, file, "LogisticRegression (Tf-idf)")
    training_model(LR_count, data_train, data_test, file, "LogisticRegression (Count)")

    file.close()
