import json


def stare_initiala():
    albe = dict()
    negre = dict()
    coloana = 65
    for i in range(1, 9):
        albe[i] = {
            'linie': 2,
            'coloana': chr(coloana + i - 1),
            'pas2': True
        }

        negre[i] = {
            'linie': 7,
            'coloana': chr(coloana + i - 1),
            'pas2': True
        }

    return (albe, negre, creeaza_matrice(albe, negre))


def creeaza_matrice(albe: dict, negre: dict):
    matrice = [[0] * 8 for i in range(8)]
    for cheia in albe.keys():
        linie = albe[cheia]['linie'] - 1
        coloana = ord(albe[cheia]['coloana']) - 65
        matrice[linie][coloana] = 'A'
        linie = negre[cheia]['linie'] - 1
        coloana = ord(negre[cheia]['coloana']) - 65
        matrice[linie][coloana] = 'N'

    return matrice


def stare_finala(configuratie: dict):
    for pion in configuratie.keys():
        if pion['linie'] % 7 == 0:
            return True

    return False


def salvaza_stare(configuratie: dict, nume_fisier: str):
    with open(nume_fisier, 'w') as fp:
        json.dump(configuratie, fp)


def incarca_stare(nume_fisier: str) -> dict:
    with open(nume_fisier, 'r') as fp:
        data = json.load(fp)
    return data
