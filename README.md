# CS2102 Assignment

Instruction Guide

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

## Alternatively using your own localhost PostgreSQL
psql cs2102_project < Design/init.sql
```

```

## Flask app

> UI documentation available at https://www.muicss.com/

```
python app.py
or
flask run
```


## Directory
```bash
|-- Designs
|   |-- ddl.sql
|   |-- er_diagram.pdf
|   |-- ER.png
|   |-- ER.sql
|   |-- insert_user.sql
|   `-- triggers.sql
|-- flask
|   |-- app.py
|   |-- data
|   |   |-- bid.py
|   |   |-- cars.py
|   |   |-- dbconfig.py
|   |   |-- __init__.py
|   |   |-- models.py
|   |   |-- rides.py
|   |   `-- users.py
|   |-- requirements.txt
|   |-- static
|   |   `-- login-bg.jpg
|   `-- templates
|       |-- addBid.html
|       |-- addCar.html
|       |-- addRide.html
|       |-- approveBid.html
|       |-- index.html
|       |-- listBid.html
|       |-- listCar.html
|       |-- login.html
|       |-- pastRide.html
|       |-- signup.html
|       |-- updateCar.html
|       |-- updateRide.html
|       `-- updateUser.htm
|-- README.md
```
