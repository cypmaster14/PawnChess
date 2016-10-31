import json
import random


def stare_initiala():
    """
        Functia ce returneza stara initiala a unui joc
    :return: Starea initiala
    """
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
    """
        Creeaza matricea corespunzatoare configuratiei pieselor de pe tabla
    :param albe:
    :param negre:
    :return:
    """
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
    """
        Verifica daca starea actuala a jocului este una finala
    :param matrice: Starea actuala a jocului , sub forma unei matricei
    :return:
    """
    for i in range(0, 8):
        if matrice[0][i] != '0' or matrice[7][i] != '0':
            return True
    return False


def salvaza_stare(configuratie: dict, nume_fisier: str):
    """
        Functie ce salveaza starea curenta a jocului pe disk
    :param configuratie:
    :param nume_fisier:
    :return:
    """
    with open(nume_fisier, 'w') as fp:
        json.dump(configuratie, fp)


def incarca_stare(nume_fisier: str) -> dict:
    """
        Functia ce incarca o veche configuratie a jocului
    :param nume_fisier:
    :return:
    """
    with open(nume_fisier, 'r') as fp:
        data = json.load(fp)

    piese_albe = data['albe']
    piese_negre = data['negre']

    return piese_albe, piese_negre, creeaza_matrice(piese_albe, piese_negre)
