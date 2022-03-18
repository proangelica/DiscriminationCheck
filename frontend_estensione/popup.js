/*quando il documento HTML è stato completamente caricato e analizzato, caricato e analizzato (a esclusione di fogli di stile CSS, immagini...), viene lanciato l'evento
ed eseguita la funzione di seguito definita*/
document.addEventListener('DOMContentLoaded', function () {
    //si seleziona l'elemento con id 'checkPage', ovvero il bottone che permette di controllare il titolo di una notizia
    var checkPageButton = document.getElementById('checkPage');
    //al click sul bottone viene associato un evento
    checkPageButton.addEventListener('click', function () {
        chrome.tabs.executeScript({
            code: `(${inContent})(${JSON.stringify({foo: 'bar'})})`
        }, ([result] = []) => {
            if (!chrome.runtime.lastError) {
                console.log(result); // shown in devtools of the popup window
            }
        });


        function inContent(params) {
            //seleziona il primo elemento <h1> che si trova nella pagina analizzata 
            const getTitle = document.getElementsByTagName('h1')[0].innerHTML;

            //si manda la frase appena selezionata al Server Flask tramite una chiamata AJAX di tipo 'POST'
            $.ajax({
                url: "http://127.0.0.1:5000/",
                type: "POST",
                async: false,
                data: "startheader " + getTitle + " endheader",
                //in caso di risposta positiva dal server, si esegue questa funzione
                success: function(resp){
                    //il server restituisce una stringa in formato JSON (quindi come una coppia chiave/valore) per cui si preleva il valore della stringa ricevuta
                    var discrimination_result = JSON.stringify(resp.discrimination);
                    var result = "";

                    //se il server ha restituito la stringa "twotimes-value" vuol dire che il titolo è stato analizzato precedentemente, quindi verrà ignorato
                    if (discrimination_result.indexOf("twotimes-value") === -1){
                        //si seleziona l'elemento <h1>
                        const parent = document.querySelector('h1');
                        //si crea un nuovo elemento <div> che servirà per contenere una delle due icone
                        const child = document.createElement('div');

                        //se il risultato ricevuto dal server è "discrimination" si modifica lo stile del titolo, evidenziandolo in rosso
                        if (discrimination_result.indexOf("discrimination") !== -1){
                            result = "discrimination";
                            parent.style.color = "#ff0000";
                        } else if (discrimination_result.indexOf("neutral") !== -1)
                            result = "neutral";
                        
                        //si aggiunge la giusta icona in base al risultato ottenuto
                        child.innerHTML = "<div align='center'><p><font color='black'>_________________</font></p><br><img src='https://raw.githubusercontent.com/proangelica/DiscriminationCheck/main/icon_" + result + ".jpg' alt='prova' width='150' height='150'></div>";
                        parent.insertAdjacentHTML('beforeend', child.outerHTML);

                        return { 
                            success: true,
                            html: document.body.innerHTML,
                        };
                    } else{ 

                    }
                },
                //in caso non si riesca a raggiungere il server, si esegue questa funzione
                error: function(e) {
                    alert("Flask server is down or is unreachable")
                }
            });
        }
        
        //l'estensione viene chiusa automaticamente
        window.close();

    }, false);
}, false);