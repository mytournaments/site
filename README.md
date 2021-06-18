# MyTournaments
Questa è la repository ufficiale del sito di MyTournaments.

## Come iniziare
Per ottenere una copia del sito in locale, clonare la repository ed entrare nella cartella appena creata:
```
git clone https://github.com/mytournaments/site.git
cd site
```

Prima di iniziare, creare file di conofigurazione chiamato `.env` contenente due campi:
- `SECRET_KEY`, necessario per ragioni di sicurezza (dei caratteri a caso);
- `DATABASE_URI`, l'URL al database che stai usando (puoi usare `sqlite` per il testing: `sqlite:///site.db`).

Esempio di file `.env`:
```
SECRET_KEY=dbb5e338b2849dc6a45d92dbef674f68
DATABASE_URI=sqlite:///site.db
```

Creare un ambiente virutale ed installare le dipendenze:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Prima di eseguire l'applicazione è necessario inizializzare il database, apri una shell di Python ed esegui i seguenti comandi:
```
>>> from mytournaments import db
>>> db.create_all()
```

E infine esegui `app.py`:
```
python app.py
```
