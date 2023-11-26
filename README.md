# Aniverse
 Aniverse is a fun online resource for anime fans where you can find extensive information about a variety of anime series, rate and discuss them, create your own "read" and "favorite" lists, and support the project through donations.
## Requirements

Make sure you have Python installed (Python 3.x is recommended) along with pip. To install project dependencies, run:

```bash
pip install -r requirements.txt

git clone https://github.com/Nikolaj-dev/Aniverse.git

cd Aniverse

python -m venv venv

#For windows 

.\venv\Scripts\activate

#For macOS or linux

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

celery -A aniverse worker -l info -P threads

