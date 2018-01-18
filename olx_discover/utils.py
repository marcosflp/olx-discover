import datetime
import re

import logging
import requests
from flask import render_template
from flask_mail import Message
from lxml import html

from olx_discover import mail, db
from olx_discover.models import Ad

LOGGER = logging.getLogger(__name__)


class OlxDiscover(object):
    amount_pagination_to_search = 20

    def __init__(self, search_url):
        self.search_url = search_url

    def __repr__(self):
        return '<OlxDiscover: {}>'.format(self.__str__())

    def __str__(self):
        return '{}'.format(self.search_url)

    def send_emails_on_new_ads(self):
        ad_list = self.get_and_save_new_ads()
        if not ad_list:
            LOGGER.info('Not sending email because there is no new ads')
            return False

        content = render_template('email.html', ad_list=ad_list)
        message = Message(
            subject='Novos Anúncios {}'.format(str(datetime.datetime.today())[:19]),
            html=content,
            sender='flask@cloudatlas.com',
            recipients=['marcos.fel93@gmail.com']
        )

        LOGGER.info('sending email about: {}'.format(message.subject))
        mail.send(message)

        return True

    def get_and_save_new_ads(self):
        ad_list = self.get_only_valid_ads()

        ad_instance_list = list()
        for ad in ad_list:

            # check if exists if not create a new
            ad_instance = Ad.query.filter(
                (Ad.url == ad['url'])
                | (Ad.image == ad['image'])
            ).first()

            if ad_instance is None:
                new_ad = Ad(
                    url=ad['url'],
                    label=ad['label'],
                    price=ad['price'],
                    details=ad['details'],
                    region=ad['region'],
                    image=ad['image']
                )

                ad_instance_list.append(new_ad)
                db.session.add(new_ad)
                LOGGER.info('Created new Ad "{}"'.format(new_ad.label))
            else:
                continue

        db.session.commit()

        return ad_instance_list

    def get_only_valid_ads(self):

        def is_valid_ad(ad):
            if not ad.get('price'):
                return False
            if not ad.get('url'):
                return False
            if not ad.get('label'):
                return False
            if not ad.get('image'):
                return False

            if not (600 <= ad['price'] <= 1600):
                return False

            forbidden_words = ['alugo', 'procuro', 'preciso', 'temporada', 'busco']
            for word in forbidden_words:
                if word in ad['label'].lower():
                    return False

            return True

        ad_list = self.fetch_ads()

        valid_ads = []
        for adv in ad_list:
            if is_valid_ad(adv):
                valid_ads.append(adv)

        return valid_ads

    def fetch_ads(self):
        ads_instance_list = list()

        last_url = ''
        for x in range(1, self.amount_pagination_to_search + 1):
            try:
                url = self.search_url + '&o={}'.format(x)
                response = requests.get(url)
                LOGGER.info('Searching on: {}'.format(url))

                if response.url == last_url:
                    LOGGER.info('No more pages. Last page: {}'.format(x))
                    break
                else:
                    last_url = response.url
            except Exception as e:
                raise e

            if not response.ok:
                raise ValueError('Response its not ok with url: {}'.format(url))

            root = html.fromstring(response.text)
            ads_list = root.xpath('//*[@id="main-ad-list"]/li/a')
            if not ads_list:
                continue

            for ad_etree in ads_list:
                url_list = ad_etree.xpath('.//@href')
                label_list = ad_etree.xpath('.//h3[contains(@class, "OLXad-list-title")]/text()')
                price_list = ad_etree.xpath('.//p[@class="OLXad-list-price"]/text()')
                details_list = ad_etree.xpath('.//p[contains(@class, "detail-specific")]/text()')
                region_list = ad_etree.xpath('.//p[contains(@class, "detail-region")]/text()')
                image_list = ad_etree.xpath('.//div[contains(@class, "OLXad-list-image-box")]/img/@data-original')

                ad = dict()
                if url_list:
                    ad['url'] = self._parse_url(url_list[0])
                if label_list:
                    ad['label'] = self._parse_label(label_list[0])
                if price_list:
                    ad['price'] = self._parse_price(price_list[0])
                if details_list:
                    ad['details'] = self._parse_details(details_list[0])
                if region_list:
                    ad['region'] = self._parse_region(region_list[0])
                if image_list:
                    ad['image'] = image_list[0]

                ads_instance_list.append(ad)

        return ads_instance_list

    @staticmethod
    def _parse_url(text):
        return re.sub('[\n\t]', '', text).strip()

    @staticmethod
    def _parse_label(text):
        return re.sub('[\n\t]', '', text).strip()

    @staticmethod
    def _parse_price(text):
        return int(text.strip().split()[1].replace('.', ''))

    @staticmethod
    def _parse_details(text):
        return re.sub('[\n\t]', '', text).strip()

    @staticmethod
    def _parse_region(text):
        return re.sub('[\n\t]', '', text).strip()

    def _parse_inserted_in(self, text):
        pass
