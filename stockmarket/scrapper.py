import requests
import bs4
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re


# dict to translate short currency code to the long one
codetocurrency = {'af': 'AFN', 'dz': 'DZD', 'mg': 'MGF', 'ar': 'ARS', 'am': 'AMD', 'aw': 'AWG', 'au': 'AUD', 'cx': 'AUD', 'cc': 'AUD', 'hm': 'AUD', 'ki': 'AUD', 'nr': 'AUD', 'nf': 'AUD', 'tv': 'AUD', 'az': 'AZM', 'bs': 'BSD', 'bh': 'BHD', 'th': 'THB', 'pa': 'USD', 'bb': 'BBD', 'by': 'BYR', 'bz': 'BZD', 'bm': 'BMD', 've': 'VEB', 'bo': 'BOV', 'br': 'BRL', 'bn': 'BND', 'bg': 'BGL', 'bi': 'BIF', 'ca': 'CAD', 'cv': 'CVE', 'ky': 'KYD', 'gh': 'GHC', 'bj': 'XOF', 'bf': 'XOF', 'ci': 'XOF', 'gw': 'GWP', 'ml': 'XOF', 'ne': 'XOF', 'sn': 'XOF', 'tg': 'XOF', 'cm': 'XAF', 'cf': 'XAF', 'td': 'XAF', 'cg': 'XAF', 'gq': 'XAF', 'ga': 'XAF', 'pf': 'XPF', 'nc': 'XPF', 'wf': 'XPF', 'cl': 'CLF', 'co': 'COP', 'km': 'KMF', 'ba': 'BAM', 'ni': 'NIO', 'cr': 'CRC', 'hr': 'HRK', 'cu': 'CUP', 'cy': 'CYP', 'cz': 'CZK', 'gm': 'GMD', 'dk': 'DKK', 'fo': 'DKK', 'gl': 'DKK', 'mk': 'MKD', 'dj': 'DJF', 'st': 'STD', 'do': 'DOP', 'vn': 'VND', 'dm': 'XCD', 'gd': 'XCD', 'ms': 'XCD', 'kn': 'XCD', 'lc': 'XCD', 'vc': 'XCD', 'ai': 'XCD', 'ag': 'XCD', 'eg': 'EGP', 'sv': 'USD', 'et': 'ETB', 'ad': 'EUR', 'at': 'EUR', 'be': 'EUR', 'fi': 'EUR', 'fr': 'EUR', 'gf': 'EUR', 'tf': 'EUR', 'de': 'EUR', 'gr': 'EUR', 'gp': 'EUR', 'va': 'EUR', 'ie': 'EUR', 'it': 'EUR', 'lu': 'EUR', 'mq': 'EUR', 'yt': 'EUR', 'mc': 'EUR', 'nl': 'EUR', 'pt': 'EUR', 're': 'EUR', 'pm': 'EUR', 'sm': 'EUR', 'cs': 'CSD', 'es': 'EUR', 'fk': 'FKP', 'fj': 'FJD', 'hu': 'HUF', 'cd': 'CDF', 'gi': 'GIP', 'ht': 'USD', 'py': 'PYG', 'gn': 'GNF', 'gy': 'GYD', 'hk': 'HKD', 'ua': 'UAH', 'is': 'ISK', 'bt': 'BTN', 'in': 'INR', 'ir': 'IRR', 'iq': 'IQD', 'jm': 'JMD', 'jo': 'JOD', 'ke': 'KES', 'pg': 'PGK', 'la': 'LAK', 'ee': 'EEK', 'kw': 'KWD', 'mw': 'MWK', 'zm': 'ZMK', 'ao': 'AOA', 'mm': 'MMK', 'ge': 'GEL', 'lv': 'LVL', 'lb': 'LBP', 'al': 'ALL', 'hn': 'HNL', 'sl': 'SLL', 'ro': 'ROL', 'lr': 'LRD', 'sz': 'SZL', 'lt': 'LTL', 'ls': 'ZAR', 'ly': 'LYD', 'my': 'MYR', 'mt': 'MTL', 'tm': 'TMM', 'mu': 'MUR', 'mz': 'MZM', 'mx': 'MXV', 'md': 'MDL', 'ma': 'MAD', 'eh': 'MAD', 'ng': 'NGN', 'er': 'ERN', 'na': 'ZAR', 'np': 'NPR', 'an': 'ANG', 'il': 'ILS', 'tw': 'TWD', 'ck': 'NZD', 'nz': 'NZD', 'nu': 'NZD', 'pn': 'NZD', 'tk': 'NZD', 'kp': 'KPW', 'bv': 'NOK', 'no': 'NOK', 'sj': 'NOK', 'pe': 'PEN', 'mr': 'MRO', 'to': 'TOP', 'pk': 'PKR', 'mo': 'MOP', 'uy': 'UYU', 'ph': 'PHP', 'gb': 'GBP', 'bw': 'BWP', 'qa': 'QAR', 'gt': 'GTQ', 'za': 'ZAR', 'om': 'OMR', 'kh': 'KHR', 'mv': 'MVR', 'id': 'IDR', 'ru': 'RUR', 'rw': 'RWF', 'sh': 'SHP', 'sa': 'SAR', 'sc': 'SCR', 'sg': 'SGD', 'sk': 'SKK', 'sb': 'SBD', 'kg': 'KGS', 'so': 'SOS', 'tj': 'TJS', 'lk': 'LKR', 'sd': 'SDD', 'sr': 'SRD', 'se': 'SEK', 'li': 'CHF', 'ch': 'CHF', 'sy': 'SYP', 'bd': 'BDT', 'ws': 'WST', 'tz': 'TZS', 'kz': 'KZT', 'si': 'SIT', 'tt': 'TTD', 'mn': 'MNT', 'tn': 'TND', 'tr': 'TRL', 'ae': 'AED', 'ug': 'UGX', 'ec': 'USD', 'as': 'USD', 'io': 'USD', 'gu': 'USD', 'mh': 'USD', 'fm': 'USD', 'mp': 'USD', 'pw': 'USD', 'pr': 'USD', 'tl': 'USD', 'tc': 'USD', 'us': 'USD', 'um': 'USD', 'vg': 'USD', 'vi': 'USD', 'uz': 'UZS', 'vu': 'VUV', 'kr': 'KRW', 'ye': 'YER', 'jp': 'JPY', 'cn': 'CNY', 'zw': 'ZWD', 'pl': 'PLN'}


def get_currencies(currency_code):
    """
    Gets exchange rates for PLN

    Returns:
        currencies: dict of exchange rates
    """

    url = f'https://api.exchangerate-api.com/v4/latest/PLN'
    data = requests.get(url).json()
    currencies = data['rates']

    return currencies


def convert(inp, amount, currencies):
    """
    Converts any currency into PLN
    Args:
        inp: original currency
        amount: amount of money
        currencies: dict with updated currencies

    Returns:
        amount: amount of money after exchange
    """

    ratio = 1 / currencies[inp]
    amount = amount * ratio
    amount = float("{:.2f}".format(amount))

    return amount



def scrap_page(name, countrycode):
    """

    Scrapping stock website for stock data.

    Arguments:
        name {string} -- stock symbol
        countrycode {string} -- country code of the stock

    Returns:
        dic -- dictionary of stock data
    """

    countrycode = countrycode.lower()

    # get currency rate from the exchange-api
    currencies = get_currencies(codetocurrency[countrycode])

    # scrapping
    url = f"https://www.marketwatch.com/investing/stock/{name}?countrycode={countrycode}"
    res = requests.get(url)
    res.encoding = "utf.8"
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    change = soup.find_all(class_='value')
    price = float(re.sub('[^\d\.]', '', change[6].get_text().replace(",", "")))
    price = convert(codetocurrency[countrycode], price, currencies)
    price = float("{:.2f}".format(price))

    point_q = soup.find_all(class_='change--point--q')
    point_q = float(point_q[0].get_text())
    point_q = convert(codetocurrency[countrycode], point_q, currencies)
    # print(point_q)

    primary = soup.find_all(class_='primary')
    day_range = primary[17].get_text().split('-')
    day_lowest = convert(codetocurrency[countrycode], float(day_range[0].strip().replace(",", "")), currencies)
    day_highest = convert(codetocurrency[countrycode], float(day_range[1].strip().replace(",", "")), currencies)

    try:
        p_e = float(re.sub('[^\d\.]', '', primary[24].get_text().replace(",", "")))
    except Exception as e:
        p_e = 0


    market_cap_preprocessed = primary[19].get_text()
    endletter = ''
    if market_cap_preprocessed[-1].isalpha():
        endletter = market_cap_preprocessed[-1]
    market_cap_float = float(re.sub('[^\d\.]', '', market_cap_preprocessed.replace(",", "")))
    market_cap_float = convert(codetocurrency[countrycode], market_cap_float, currencies)
    market_cap = str(market_cap_float) + endletter



    public_float = primary[21].get_text()


    eps = float(re.sub('[^\d\.-]', '', primary[25].get_text().replace(",", "")))
    eps = convert(codetocurrency[countrycode], eps, currencies)

    try:
        dividend = float(re.sub('[^\d\.-]', '', primary[27].get_text().replace(",", "")))
        dividend = convert(codetocurrency[countrycode], dividend, currencies)
    except:
        dividend = 0


    info = {'price': price,
            'point_q': point_q,
            'day_lowest': day_lowest,
            'day_highest': day_highest,
            'p_e': p_e,
            'market_cap': market_cap,
            'public_float': public_float,
            'eps': eps,
            'dividend': dividend
            }

    return info


def history(name, countrycode):
    """

    Scrapping historical data of stock, then creating the graph using provided data.

    Arguments:
        name {string} -- stock symbol
        countrycode {string} -- country of the stock


    Returns:
        graph -- graph of the stock's historical data
    """

    # scrapping
    countrycode = countrycode.lower()
    currencies = get_currencies(codetocurrency[countrycode])
    url = f"https://www.marketwatch.com/investing/stock/{name}/download-data?countrycode={countrycode}"
    res = requests.get(url)
    res.encoding = "utf.8"
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    primary = soup.find_all(class_='table__row')

    # check how many fields the table contains
    for i, j in enumerate(primary[11:]):
        j.find(class_="cell__content u-secondary")
        try:
            j.get_text()
        except:
            break

    data = primary[11:i + 3]
    # date
    x = [j.find(class_="cell__content u-secondary").get_text()[:-5]
         for j in data][::-1]
    # day lowest
    y_preconv = [float(re.sub('[^\d\.]', '', j.find_all(class_="cell__content")[2].get_text().replace(",", "")))
         for j in data][::-1]
    y = [convert(codetocurrency[countrycode], price, currencies)
         for price in y_preconv]
    # day highest
    z_preconv = [float(re.sub('[^\d\.]', '', j.find_all(class_="cell__content")[5].get_text().replace(",", "")))
         for j in data][::-1]
    z = [convert(codetocurrency[countrycode], price, currencies)
         for price in z_preconv]

    # ploting the graph
    plt.switch_backend('AGG')
    plt.rc('grid', linestyle="--", color='green')
    plt.figure(figsize=(15, 5))
    plt.axes().set_facecolor("black")
    plt.grid(True)
    plt.plot(x, y, marker='o', markerfacecolor='black',
             markersize=5, color='lightgreen', linewidth=2, label='open price')
    plt.plot(x, z, marker='o', markerfacecolor='black',
             markersize=5, color='red', linewidth=2, label='close price')
    plt.legend(loc="upper left")

    # save graph as bytes in order to pass it to the view function, which will render it on the html side
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
