import json
import random


def stare_initiala():
    albe = dict()
    negre = dict()
    coloana = 65
    for i in range(1, 9):
        albe[i] = {
            'linie': 1,
            'coloana': chr(coloana + i - 1),
            'pas2': True,
            'sens': 1
        }

        negre[i] = {
            'linie': 6,
            'coloana': chr(coloana + i - 1),
            'pas2': True,
            'sens': -1
        }

    return (albe, negre, creeaza_matrice(albe, negre))


def creeaza_matrice(albe: dict, negre: dict):
    matrice = [['0'] * 8 for i in range(8)]
    for cheia in albe.keys():
        linie = albe[cheia]['linie']
        coloana = ord(albe[cheia]['coloana']) - 65
        matrice[linie][coloana] = 'A'
        linie = negre[cheia]['linie']
        coloana = ord(negre[cheia]['coloana']) - 65
        matrice[linie][coloana] = 'N'

    return matrice


def stare_finala(matrice: list):
    for i in range(0, 8):
        if matrice[0][i] != '0' or matrice[7][i] != '0':
            return True
    return False


def salvaza_stare(configuratie: dict, nume_fisier: str):
    with open(nume_fisier, 'w') as fp:
        json.dump(configuratie, fp)


def incarca_stare(nume_fisier: str) -> dict:
    with open(nume_fisier, 'r') as fp:
        data = json.load(fp)
    return data

# De acum in jos intr un alt modul
