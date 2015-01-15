from fabric.api import run, env, cd

env.use_ssh_config = True
env.user = 'dogebot'
env.hosts = [
    'dogebot'
]


def run_dash():
    with cd('~/dogebot/'):
        run('. ../packs/bin/activate && python manage.py runserver')


def deploy():
    with cd('~/dogebot/'):
        run('git pull origin')
        run('. ../packs/bin/activate && pip install -r requirements.txt')
