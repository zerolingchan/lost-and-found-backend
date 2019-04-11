# lost-and-found-backend

## introduction

失物招领

## install
```bash
git clone https://github.com/zerolingchan/lost-and-found-backend.git
cp config.py.example config.py
vim config.py # setup variable
pip install -r requirements

# migrate database and generate table
flask db upgrade
python run.py
```

## contribution
- `config.py` all flask config 
- `app/model` model direction
- `app/route` route direction
