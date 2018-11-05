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
        dest='valeur', nargs='+', default=['fermeture'],
        choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
        help="La valeur desiree (par defaut: fermeture)"
    )

    parser.add_argument(
        'symbole', metavar='symbole', help='Nom du symbole boursier desire'
    )

    return parser.parse_args()


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

    # conversion de l'argument 'valeur' pour matcher les cles du dictionnaire de l'api AlphaVantage
    for i in range(len(arg.valeur)):
        if arg.valeur[i] == 'ouverture':
            arg.valeur[i] = '1. open'
        elif arg.valeur[i] == 'max':
            arg.valeur[i] = '2. high'
        elif arg.valeur[i] == 'min':
            arg.valeur[i] = '3. low'
        elif arg.valeur[i] == 'fermeture':
            arg.valeur[i] = '4. close'
        elif arg.valeur[i] == 'volume':
            arg.valeur[i] = '5. volume'

    # conversion des string date en objet date
    arg.dateDebut = datetime.datetime.strptime(arg.dateDebut, '%Y-%m-%d')
    arg.dateFin = datetime.datetime.strptime(arg.dateFin, '%Y-%m-%d')

    # ajustement des valeurs de date pour requete
    if arg.dateDebut > arg.dateFin:
        arg.dateDebut = arg.dateFin

    resultat = []

    #On parcourt la reponse de l'Api ligne par ligne
    for cleDateRequete in reponseApi['Time Series (Daily)']:

        #conversion de la string date de la requete en objet date
        dateRequete = datetime.datetime.strptime(cleDateRequete, '%Y-%m-%d')

        #si on est dans le range de date demande par l'utilisteur
        if dateRequete >= arg.dateDebut and dateRequete <= arg.dateFin:

            requeteFiltree = reponseApi['Time Series (Daily)'][cleDateRequete]

            donneeARetourner = [str(cleDateRequete)]

            for cleValeur in requeteFiltree:
                #selon ce que l'utilisateur veut voir comme valeur
                if cleValeur in arg.valeur:
                    donneeARetourner.append(str(requeteFiltree[cleValeur]))

            resultat.append(tuple(donneeARetourner))
            resultat.reverse()

    return resultat


def main():

    arg = conversionLigneCommande()
    print('{}({}, {}, {})'.format(arg.symbole, ','.join(arg.valeur), arg.dateDebut, arg.dateFin))

    req = requeteApi(arg)

    res = traitmentDonnee(req, arg)
    print(res)


if __name__ == '__main__':
    main()