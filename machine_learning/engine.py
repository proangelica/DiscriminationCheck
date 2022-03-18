# pip install flask
# pip install -U flask-cors
# set FLASK_APP=engine.py
# flask run
# Running on http://127.0.0.1:5000/
import time
import pickle
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

import re

import seaborn as sns
sns.set()  # use seaborn plotting style

# turn on CORS to handle the popup.js request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        start_time = time.time()
        # prendo il titolo che mi è stato mandato
        string = str(request.form)
        # rimuovo tutto quello che c'è prima di startheader
        headline = re.sub('^(.*)(?=startheader)', "", string)
        # rimuovo tutto quello che c'è dopo startheader
        sep = "endheader"
        headline = headline.split(sep, 1)[0]
        # cancello la parola startheader così rimane solo il titolo effettivo
        headline = headline.replace('startheader ', '')

        # se si sta cercando di controllare il titolo più di una volta,
        # viene spedito allo script popup.js un valore nullo (in formato JSON)
        if "<div><div align" in headline:
            return jsonify(discrimination="twotimes-value")

        print(headline)

        # carico il classificatore pickle opportuno
        [best_grid, label_encoder, vectorizer] = pickle.load(open("discrimination_NB_well.pickle", 'rb'))
        # [best_grid, label_encoder, vectorizer] = pickle.load(open("discrimination_NB_weakly.pickle", 'rb'))

        # avvio la predizione sulla stringa data in input (che è il titolo di giornale memorizzato nel tag <h1>)
        # tramite il metodo transform il testo viene trasformato in un numero (vettorizzazione)
        headline_l = vectorizer.transform([headline])
        # si memorizza la previsione effettuata dal modello
        discrimination_result = best_grid.predict(headline_l)
        # si effettua una trasformazione da intero a stringa per scoprire la classe di appartenenza della stringa
        # (neutral o discrimination)
        discrimination_result = label_encoder.inverse_transform(discrimination_result)

        print(discrimination_result[0])
        print("---Execution time: %s seconds ---" % (time.time() - start_time))

        # si restituisce allo script popup.js il risultato ottenuto dal classificatore (in formato JSON)
        return jsonify(discrimination=discrimination_result[0])

    # se il tipo di richiesta ricevuta è 'GET', si sta avviando per la prima volta il server
    # si mostra una pagina vuota con la sola informazione del funzionamento del server
    return 'Flask server works correctly'


# utilizzato per lanciare l'applicazione
if __name__ == "__main__":
    app.run(debug=True)
