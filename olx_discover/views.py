from flask import render_template

from olx_discover import app
from olx_discover.utils import OlxDiscover


@app.route('/')
def hello_world():
    leste = OlxDiscover('https://sc.olx.com.br/florianopolis-e-regiao/leste/imoveis/aluguel/apartamentos?pe=1600&ps=600&ret=1040&sd=2620&sd=2621&sd=2622&sd=2623&sd=2624&sd=2625&sd=2626&sr=1')
    norte = OlxDiscover('https://sc.olx.com.br/florianopolis-e-regiao/norte/imoveis/aluguel/apartamentos?pe=1600&ps=600&ret=1040&sd=2542&sd=2543&sd=2545&sd=2546&sd=2548&sd=2551&sd=2552&sd=2553&sd=2554&sd=2555&sd=2557&sd=2558&sd=2559&sd=2560&sr=1')
    centro = OlxDiscover('https://sc.olx.com.br/florianopolis-e-regiao/centro/imoveis/aluguel/apartamentos?pe=1600&ps=700&ret=1040&sd=2562&sd=2563&sd=2564&sd=2565&sr=1')
    sul = OlxDiscover('https://sc.olx.com.br/florianopolis-e-regiao/sul/imoveis/aluguel/apartamentos?pe=1600&ps=600&ret=1040&sd=2532&sd=2533&sd=2534&sd=2535&sd=2536&sd=2539&sr=1')

    carros = OlxDiscover('https://sc.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/flex?cf=1&ctp=1&ctp=8&ctp=9&pe=18000&rs=26')

    all_ads = list()
    all_ads.extend(carros.get_only_valid_ads())

    # MARROM
    # all_ads.extend(norte.get_only_valid_ads())

    # TOP
    # all_ads.extend(sul.get_only_valid_ads())

    # BAD
    # all_ads.extend(centro.get_only_valid_ads())

    return render_template('email.html', ad_list=all_ads)
