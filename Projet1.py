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

    # conversion de l'argument 'valeur' pour matcher les cles du dictionnaire de l'api AlphaVantage
    for i, val in enumerate(arg.valeur):
        if val == 'ouverture':
            arg.valeur[i] = '1. open'
        elif val == 'max':
            arg.valeur[i] = '2. high'
        elif val == 'min':
            arg.valeur[i] = '3. low'
        elif val == 'fermeture':
            arg.valeur[i] = '4. close'
        elif val == 'volume':
            arg.valeur[i] = '5. volume'

    #conversion des string date en objet date
    arg.dateDebut = datetime.datetime.strptime(arg.dateDebut, '%Y-%m-%d')
    arg.dateFin = datetime.datetime.strptime(arg.dateFin, '%Y-%m-%d')

    #ajustement des valeurs de date pour requete
    if arg.dateDebut > arg.dateFin:
        arg.dateDebut = arg.dateFin

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


def traitmentDonnee(reponseApi, arg):
    resultat = []

    #On parcourt la reponse de l'Api ligne par ligne
    for cleDateRequete in reponseApi['Time Series (Daily)']:

        #conversion de la string date de la requete en objet date
        dateRequete = datetime.datetime.strptime(cleDateRequete, '%Y-%m-%d')

        #si on est dans le range de date demande par l'utilisteur
        if dateRequete >= arg.dateDebut and dateRequete <= arg.dateFin:

            requeteFiltree = reponseApi['Time Series (Daily)'][cleDateRequete]

            selectionDonnees = []

            for cleValeur in requeteFiltree:
                #selon ce que l'utilisateur veut voir comme valeur
                if cleValeur in arg.valeur:
                    selectionDonnees.append(str(requeteFiltree[cleValeur]))

            resultat.append(tuple(selectionDonnees))

    print(resultat)


def main():
    arg = conversionLigneCommande()
    req = requeteApi(arg)
    traitmentDonnee(req, arg)


if __name__ == '__main__':
    main()