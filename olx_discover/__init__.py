from celery import Celery
from celery.schedules import crontab
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('settings')


@app.cli.command()
def init_db():
    """
    Initialize the database.
    """

    print('Running "db.create_all()"')
    db.create_all()

    from olx_discover.models import AdsOrigin
    ads_origin = AdsOrigin(
        url='http://sc.olx.com.br/florianopolis-e-regiao/norte/imoveis/aluguel?',
        label='Aluguel de apartamentos em Canas e Cachoeiras'
    )

    db.session.add(ads_origin)
    db.session.commit()
    print('Created new object AdsOrigin "{} - {}"'.format(ads_origin.id, ads_origin.label))

    return None


mail = Mail(app)
db = SQLAlchemy(app)


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.beat_schedule = {
    # Executes every hour
    'test': {
        'task': 'olx_discover.tasks.send_email_on_new_ads',
        'schedule': crontab(minute=0),
    },
}


from olx_discover import tasks
from olx_discover import views
