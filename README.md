# bb-manage



### Setup

1. Local settings:
```
cp main/local_settings.py.def main/local_settings.py
./renew_secret_key
```

2. Install dependencies:
```sh
pip install -r requirements.txt
```

3. Create database and migrate
```sh
echo "CREATE DATABASE bbapi CHARACTER SET utf8 COLLATE utf8_general_ci;" | mysql -uroot -p
./manage.py migrate
```
