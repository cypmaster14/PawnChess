from stari import *
from UtilitarTranzit import *
import sys

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()


def validare_sintaxa_miscare(miscare: str):
    if miscare[0].isalpha() and miscare[0] >= 'A' and miscare[0] <= 'H' and miscare[1].isdigit() and int(
            miscare[1]) >= 0 and \
                    int(miscare[1]) <= 8:
        return True

    return False


def mut_piesa_mea(matrice: list, miscare: str, jucator: str):
    linie, coloana = get_pozitie(miscare)
    if matrice[linie][coloana] == jucator:
        return True
    return False


def get_pozitie(pozitie: str) -> tuple:
    return int(pozitie[1]), ord(pozitie[0]) - 65


def get_piesa_din_dictionar(piesa: str, culoare_jucator: str) -> int:
    linie, coloana = get_pozitie(piesa)
    for piesa in configuratie_curenta[culoare_jucator].keys():
        if configuratie_curenta[culoare_jucator][piesa]['linie'] == linie and \
                                ord(configuratie_curenta[culoare_jucator][piesa]['coloana']) - 65 == coloana:
            return piesa


def miscare_valida(pion: str, miscare: str):
    global matrice_configuratie_anterioara, matrice_configuratie_curenta
    ln_urm, col_urm = get_pozitie(miscare)
    ln_act, col_act = get_pozitie(pion)
    return mutare_valida_jucator(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act, col_act, ln_urm,
                                 col_urm, 1)


def realizare_tranzitie(piesa_mutata: str, noua_pozitie: str, jucator: str, culoare_jucator: str):
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, configuratie_curenta
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    matrice_configuratie_anterioara = [list(x) for x in matrice_configuratie_curenta]
    matrice_configuratie_curenta[linie_veche][coloana_veche] = '0'
    matrice_configuratie_curenta[linie_noua][coloana_noua] = jucator
    pion = get_piesa_din_dictionar(piesa_mutata, culoare_jucator)
    configuratie_curenta[culoare_jucator][pion]['linie'], configuratie_curenta[culoare_jucator][pion][
        'coloana'] = linie_noua, coloana_noua


def joaca_utilizatorul():
    while True:
        try:
            piesa_mutata = input('Introduce-ti piesa pe care doriti sa o mutati(Ex:a2):')
            piesa_mutata = piesa_mutata.upper()
            if validare_sintaxa_miscare(piesa_mutata):
                if not mut_piesa_mea(matrice_configuratie_curenta, piesa_mutata, 'A'):
                    raise Exception('Nu a-ti mutat o piesa care va apartine')
            else:
                raise Exception('Eroare la sintaxa mutarii')
            pozitie_viitoare = input('Introduce-ti noua pozitie a piesei(Ex:a4):')
            pozitie_viitoare = pozitie_viitoare.upper()
            if validare_sintaxa_miscare(pozitie_viitoare):
                if miscare_valida(piesa_mutata, pozitie_viitoare):
                    realizare_tranzitie(piesa_mutata, pozitie_viitoare, 'A', 'albe')
                    break
                else:
                    raise Exception('Miscare invalida , incercati din nou')

            else:
                raise Exception('Eroare la sintaxa noi pozitii')
        except Exception as e:
            print(e)


def joaca_calculatorul():
    # Calculatorul va juca mereu cu piesele negre

    dictionar_lista_adiacenta = dict()

    for piesa in configuratie_curenta['negre'].items():
        linie, coloana = piesa[1]['linie'], ord(piesa[1]['coloana']) - 65
        lista_adiacenta = list()
        # Un pas in fata
        if mutare_valida_inainte(matrice_configuratie_curenta, linie, linie - 1, coloana, -1):
            lista_adiacenta.append((linie - 1, coloana))

        # Doi pasi in fara
        if piesa[1]['pas2'] == True and mutare_valida_inainte(matrice_configuratie_curenta, linie, linie - 2, coloana,
                                                              -1):
            lista_adiacenta.append((linie - 2, coloana))

        # Diagonala
        if coloana - 1 >= 0:
            if mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, linie, linie - 1,
                                     coloana - 1, -1):
                lista_adiacenta.append((linie - 1, coloana - 1))

        if coloana + 1 <= 7:
            if mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, linie, linie - 1,
                                     coloana + 1, -1):
                lista_adiacenta.append((linie - 1, coloana + 1))

        dictionar_lista_adiacenta[piesa[0]] = lista_adiacenta

    # Am determinat toate miscarile posibile, in functie de o strategie trebuie sa aleg o miscare

    if len(dictionar_lista_adiacenta) == 0 or este_remiza(dictionar_lista_adiacenta):
        sys.exit("Remiza")

    pion_ales_pentru_mutare = random.choice(list(dictionar_lista_adiacenta.keys()))
    pozitie_veche_pion_ales = configuratie_curenta['negre'][pion_ales_pentru_mutare]['coloana'] + \
                              str(configuratie_curenta['negre'][pion_ales_pentru_mutare]['linie'])
    pozitie_noua = random.choice(list(dictionar_lista_adiacenta[pion_ales_pentru_mutare]))
    realizare_tranzitie(pozitie_veche_pion_ales, chr(pozitie_noua[1] + 65) + str(pozitie_noua[0]), 'N', 'negre')


def este_remiza(dictionar_lista_adiacenta: dict):
    for item in dictionar_lista_adiacenta.items():
        if len(item[1]) > 0:
            return False

    return True


def joaca(configuratie: dict, matrice: list):
    global configuratie_curenta, matrice_configuratie_anterioara, matrice_configuratie_curenta
    configuratie_curenta = configuratie
    matrice_configuratie_anterioara = list(matrice)
    matrice_configuratie_curenta = list(matrice)
    # rand_jucator = random.choice([False, True])
    rand_jucator = True
    while not stare_finala(matrice_configuratie_curenta):
        if rand_jucator:
            joaca_utilizatorul()
            rand_jucator = False
        else:
            joaca_calculatorul()
