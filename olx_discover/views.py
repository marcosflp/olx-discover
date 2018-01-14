from flask import render_template

from olx_discover import app
from olx_discover.utils import OlxDiscover


@app.route('/')
def hello_world():
    olx = OlxDiscover('http://sc.olx.com.br/florianopolis-e-regiao/norte/imoveis/aluguel?')
    ads = olx.get_only_valid_ads()
    # ads = Ad.query.all()
    return render_template('email.html', ad_list=ads)
