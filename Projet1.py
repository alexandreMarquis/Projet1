import argparse
import requests
import json
import datetime

def conversionLigneCommande():
    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un symbole boursier")

    parser.add_argument(
        '-d', '--debut',
        metavar='DATE', dest='dateDebut', default=str(datetime.date.today()),
        help="Date recherchee la plus ancienne (format: AAAA-MM-JJ)"
    )

    parser.add_argument(
        '-f', '--fin',
        metavar='DATE', dest='dateFin', default=str(datetime.date.today()),
        help="Date recherchee la plus recente (format: AAAA-MM-JJ)")

    parser.add_argument(
        '-v', '--valeur',
        dest='valeur', nargs='+', default='fermeture',
        choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
        help="La valeur desiree (par defaut: fermeture)"
    )

    parser.add_argument(
        'symbole', metavar='symbole', help='Nom du symbole boursier desire'
    )

    arg = parser.parse_args()

    # conversion des valeurs pour matcher les cles du dictionnaire
    for i in range(len(arg.valeur)):
        if (arg.valeur[i] == 'ouverture'):
            arg.valeur[i] = '1. open'
        elif (arg.valeur[i] == 'max'):
            arg.valeur[i] = '2. high'
        elif (arg.valeur[i] == 'min'):
            arg.valeur[i] = '3. low'
        elif (arg.valeur[i] == 'fermeture'):
            arg.valeur[i] = '4. close'
        elif (arg.valeur[i] == 'volume'):
            arg.valeur[i] = '5. volume'

    #conversion des string date en objet date
    arg.dateDebut = datetime.datetime.strptime(arg.dateDebut, '%Y-%m-%d')
    arg.dateFin = datetime.datetime.strptime(arg.dateFin, '%Y-%m-%d')

    #ajustement des valeurs de date pour requete
    if arg.dateDebut > arg.dateFin:
        dateDebut = dateFin

    return arg

def requeteApi(arg):
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    apikey = '3PQRLNKE9VP5JH12'

    params = {
        'function': function,
        'symbol': arg.symbole,
        'apikey': apikey,
        'outputsize': 'compact',
    }

    response = requests.get(url=url, params=params)

    return json.loads(response.text)


def traitmentDonnee(req, arg):





    resultat = []

    for i in req['Time Series (Daily)']:
        dateRequete = datetime.datetime.strptime(i, '%Y-%m-%d')

        if dateRequete >= dateDebut and dateRequete <= dateFin:
            tupleT = []
            for j in range(len(arg.valeur)):
                print(req['Time Series (Daily)'][i][arg.valeur[j]])
                tupleT.append(str(req['Time Series (Daily)'][i][arg.valeur[j]]))
                print(tupleT)
            resultat.append(tuple(tupleT))
            tupleT = ()

    print(resultat)


def main():
    arg = conversionLigneCommande()
    req = requeteApi(arg)
    traitmentDonnee(req, arg)

if __name__ == '__main__':
    main()