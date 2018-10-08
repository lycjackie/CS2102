# CS2102 Assignment
Yay

## Setting up

1. Download PostgreSQL from : https://www.postgresql.org/download/

1.1 Download for macOS using `brew`
> brew install postgresql

> brew services start postgresql
2. Get python-pip. `apt-get install python-pip` or `easy_install pip`
3. Go into `flask` folder. Run `pip install -r requirements.txt`

## Connecting to Cloud Postgres
> GUI Tools available at https://www.jetbrains.com/datagrip/?fromMenu
> Alternatively you can source for your own one. Jetbrains has student account.
```
URL  :  cs2107.jackielyc.me
Port :  5432
Database : cs2102_project
```

Use any GUI tools or cmd prompt to connect.

```
psql -h cs2107.jackielyc.me -U cs2102_admin --dbname=cs2102_project
```

## Flask app

> UI documentation available at https://www.muicss.com/

```
python app.py
```
