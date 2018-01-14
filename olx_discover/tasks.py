from celery.utils.log import get_task_logger

from olx_discover import celery, app
from olx_discover.models import AdsOrigin
from olx_discover.views import OlxDiscover

LOGGER = get_task_logger('tasks')


@celery.task
def send_email_on_new_ads():
    with app.app_context():
        ads_origin_list = AdsOrigin.query.all()
        if not ads_origin_list:
            LOGGER.info('Não possuí origem cadastrado')
            return None

        for ads_origin in ads_origin_list:
            olx_discover = OlxDiscover(ads_origin.url)

            try:
                has_sent = olx_discover.send_emails_on_new_ads()
            except Exception as e:
                LOGGER.exception(e)
                has_sent = None

            if has_sent:
                LOGGER.info('Email enviado.')
            else:
                LOGGER.info('Não existem novos Ads para enviar email.')
