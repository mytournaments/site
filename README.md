# MyTournaments
Questa è la repository ufficiale del sito di MyTournaments.

## Come iniziare
Per ottenere una copia del sito in locale, clonare la repository:
```
git clone https://github.com/mytournaments/site.git
```
Create un ambiente virutale ed installare le dipendenze:
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
