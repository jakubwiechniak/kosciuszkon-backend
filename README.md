# SETUP
App require python 3.10

## Virtual env
```
python -m venv venv
```

## Turn on venv
```
(windows) .\venv\Scripts\activate || (unix) source venv/bin/activate
```

## Install requirements
```
pip install -r requirements.txt
```

## Set environmental variable
```
(windows) set FLASK_APP=main.py || (unix) export FLASK_APP=main.py
```

## Run application
```
flask --debug run
```