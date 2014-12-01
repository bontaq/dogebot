1) Install Homebrew

   ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

2) Install Python3

   brew install python3

3) Install virtualenv

   pip install virtualenv

 if pip isn't installed,

   sudo easy_install pip

4) Create a new virtualenv

   cd
   virtualenv --python=/usr/local/bin/python3 dogeb

5) Activate virtualenv

   . dogeb/bin/activate

6) Install git

   brew install git

7) Clone git repo

   git clone https://bontaq@bitbucket.org/bontaq/dogebote.git

8) Install requirements

   cd dogebote
   pip install -r requirements.txt

9) Sync the database

   python manage.py syncdb

10) Run migrations

   python manage.py migrate

11) Run!

   python manage.py runserver

It should now be visible if you visit http://127.0.0.1:8000/ in your browser.
