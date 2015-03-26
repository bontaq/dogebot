A doge tipbot for soundcloud!  It's very much in Alpha/Gamma/Beta so don't be too surprised.

This bot works via messages sent directly to it and mentions detected by users on songs.

Instructions (for unix, after cloning to directory):

1) install dogecoind by following https://github.com/dogecoin/dogecoin/blob/master/doc/build-unix.md

2) start dogecoind after building from in /src.  let it sync.

3) ```apt-get install postgresql```

4) ```createdb doge```

5) update dogebot/local_settings.py if you have a password or differences

6) ```apt-get install rabbitmq-server```

7) ```easy_install pip```

8) ```pip install virtualenv```

9) create a new virtualenv, and from the base directory of dogebot, after activating: ```pip install -r requirements.txt```

10) start postgres if it isn't running, I use 

```pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start```

11) migrate tables with ```python manage.py syncdb && python manage.py migrate```

12) start rabbitmq with ```rabbitmq-server```

13) start celery with ```python manage.py celery worker```

You should now, after updating your local settings with your soundcloud information, be able to run ```python manage.py run_bot``` 
this command essentially does everything.  If you're on a mac, the commands are similar, just use brew instead.

To those who write fun stuff involving soundcloud, the best part of this is that I found a way to get mentions from their API.  Checkout my commit on https://github.com/bontaq/soundcloud-python if you'd like to do it too.
