# UniHelper
Telegram bot per la ricerca delle lezioni, esami e lauree dell'università degli studi di Perugia.

Requirements:
- `pip3 install PyTelegramBotAPI`
- `pip3 install selenium`
- `pip3 install sqlite3`

Per il corretto funzionamento del programma è necessario usare il crontab:
#minute(0-59) hour(0-23) day(1-31) month(1-12) weekday(0-6)
- `1 0 * * * python3 /home/mm/Desktop/UniHelper_dbSync.py >> /home/mm/Desktop/logSync.txt`
- `1 0 1 9 * python3 /home/mm/Desktop/UniHelper_dbLezioni.py >> /home/mm/Desktop/logLezioni.txt`

Creazione e riempimento iniziale database:
- `python3 db.py`
- `python3 UniHelper_dbLezioni.py`

Avvio programma:
- Se lo si vuole fare manualmente, eseguire i passaggi nella sezione `Creazione e riempimento iniziale database` e poi lanciare il programma con `python3 UniHelper.py`
- Se lo si vuole fare in automatico, eseguire il file `initialize.sh`
