# MyTournaments
Questa è la repository ufficiale del sito di MyTournaments.

## Come iniziare
Per ottenere una copia del sito in locale, basta seguire questi semplici passaggi:
```
git clone https://github.com/mytournaments/site.git
pip install -r requirements.txt
cd src
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
