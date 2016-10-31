from stari import *
import random
from UtilitarListeAdiacenta import *
import sys
from UtilitarJoc import *

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()


def validare_sintaxa_miscare(miscare: str):
    """
        Functie ce valideaza daca miscarea introdusa de utilizator este una valida din punct de vedere sintaxic
    :param miscare:
    :return:
    """
    if len(miscare) == 2 and miscare[0].isalpha() and 'A' <= miscare[
        0] <= 'H' and miscare[1].isdigit() and 0 <= int(
        miscare[1]) <= 8:
        return True

    return False


def mut_piesa_mea(matrice: list, miscare: str, jucator: str):
    """
        Functie ce verifica daca piesa pe care doreste sa o multe utilizatorul este o piesa a asa
    :param matrice: Matricea cureanta
    :param miscare: Miscarea pe care coreste sa o realizeze jucatorul
    :param jucator:
    :return:
    """
    linie, coloana = get_pozitie(miscare)
    if matrice[linie][coloana] == jucator:
        return True
    return False


def miscare_valida(pion: str, miscare: str):
    """
        Validez miscarea ce se doreste sa se realizeze
    :param pion:
    :param miscare:
    :return:
    """
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, \
        configuratie_curenta
    ln_urm, col_urm = get_pozitie(miscare)
    ln_act, col_act = get_pozitie(pion)
    pozitie = get_piesa_din_dictionar(pion, configuratie_curenta['albe'])

    if abs(ln_urm - ln_act) == 2 and col_act == col_urm and \
                    configuratie_curenta['albe'][pozitie]['pas2'] is False:
        return False

    return mutare_valida_jucator(matrice_configuratie_anterioara,
                                 matrice_configuratie_curenta, ln_act, col_act,
                                 ln_urm,
                                 col_urm, 1)


def realizare_tranzitie(piesa_mutata: str, noua_pozitie: str,
                        configuratie_jucator: dict, sens: int):
    """
        Functie ce realizeaza operatiile necesare realizarii unei tranzitii
    :param piesa_mutata:
    :param noua_pozitie:
    :param configuratie_jucator:
    :param sens:
    :return:
    """
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, \
        configuratie_curenta
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    culoare = obtine_culoare_dupa_sens(sens)
    matrice_configuratie_curenta[linie_veche][coloana_veche] = '0'
    matrice_configuratie_curenta[linie_noua][coloana_noua] = culoare
    if este_pozitie_en_passant(matrice_configuratie_anterioara,
                               matrice_configuratie_curenta, linie_noua,
                               coloana_noua, sens):
        matrice_configuratie_curenta[linie_noua - sens][coloana_noua] = '0'

    matrice_configuratie_anterioara = [list(x) for x in
                                       matrice_configuratie_curenta]

    pion = get_piesa_din_dictionar(piesa_mutata, configuratie_jucator)
    configuratie_jucator[pion]['pas2'] = False
    configuratie_jucator[pion]['linie'], configuratie_jucator[pion][
        'coloana'] = linie_noua, chr(coloana_noua + 65)


def joaca_utilizatorul():
    """
        Functie ce reprezenta actiunea realizata de utilizator
    :return:
    """
    while True:
        try:
            piesa_mutata = input(
                'Introduce-ti piesa pe care doriti sa o mutati(Ex:a2):')
            piesa_mutata = piesa_mutata.upper()
            if validare_sintaxa_miscare(piesa_mutata):
                if not mut_piesa_mea(matrice_configuratie_curenta,
                                     piesa_mutata, 'A'):
                    raise Exception('Nu a-ti mutat o piesa care va apartine')
            else:
                raise Exception('Eroare la sintaxa mutarii')
            pozitie_viitoare = input(
                'Introduce-ti noua pozitie a piesei(Ex:a4):')
            pozitie_viitoare = pozitie_viitoare.upper()
            if validare_sintaxa_miscare(pozitie_viitoare):
                if miscare_valida(piesa_mutata, pozitie_viitoare):
                    realizare_tranzitie(piesa_mutata, pozitie_viitoare,
                                        configuratie_curenta['albe'], +1)
                    break
                else:
                    raise Exception('Miscare invalida, incercati din nou')

            else:
                raise Exception('Eroare la sintaxa noi pozitii')
        except Exception as e:
            print(e)


def joaca_calculatorul():
    """
        Functie ce reprezenta actiunea realizata de calculator
    :return:
    """
    # Calculatorul va juca mereu cu piesele negre
    sterge_din_configuratie_piesele_mancate(matrice_configuratie_curenta,
                                            configuratie_curenta['negre'])

    liste_adiacenta = calculeaza_liste_adiacenta(
        matrice_configuratie_anterioara, matrice_configuratie_curenta,
        configuratie_curenta['negre'])

    liste_adiacenta_defensive = obtine_liste_adiacenta_defensive(
        matrice_configuratie_curenta, liste_adiacenta)
    liste_adiacenta_ofensive = obtine_liste_adiacenta_ofensive(
        matrice_configuratie_anterioara,
        matrice_configuratie_curenta, liste_adiacenta)
    liste_adiacenta_culoar = obtine_liste_adiacenta_culoar_liber(
        matrice_configuratie_curenta,
        liste_adiacenta_defensive)
    liste_adiacenta_ofensive_sigure = obtine_liste_adiacenta_ofensive_sigure(
        liste_adiacenta_defensive,
        liste_adiacenta_ofensive)
    liste_adiacenta_en_passant = obtine_liste_adiacenta_en_passant(
        matrice_configuratie_anterioara,
        matrice_configuratie_curenta,
        liste_adiacenta_ofensive_sigure)  # sa facem en-passant din ofensive simplu, sau din alea sigure?
    lista_liste_adiacenta = [liste_adiacenta_en_passant,
                             liste_adiacenta_culoar,
                             liste_adiacenta_ofensive_sigure,
                             liste_adiacenta_defensive,
                             liste_adiacenta_ofensive,
                             liste_adiacenta]
    dictionar_posibilitati_nume = ["en_passant", "culoar", "ofensiva sigura",
                                   "defensiva", "ofensiva", "all"]

    for i in range(len(lista_liste_adiacenta)):
        print(dictionar_posibilitati_nume[i], lista_liste_adiacenta[i])

    dictionar_posibilitati_mutare = lista_liste_adiacenta.pop(0)
    nume_lista = dictionar_posibilitati_nume.pop(0)

    while len(dictionar_posibilitati_mutare) == 0 and len(
            lista_liste_adiacenta) > 0:
        dictionar_posibilitati_mutare = lista_liste_adiacenta.pop(0)
        nume_lista = dictionar_posibilitati_nume.pop(0)

    print("Calculatorul a ales", nume_lista, "si poate alege din:")
    print(dictionar_posibilitati_mutare)

    if len(dictionar_posibilitati_mutare) == 0:
        sys.exit("Remiza")

    pion_ales_pentru_mutare = random.choice(
        list(dictionar_posibilitati_mutare.keys()))
    pozitie_veche_pion_ales = \
        configuratie_curenta['negre'][pion_ales_pentru_mutare]['coloana'] + \
        str(configuratie_curenta['negre'][pion_ales_pentru_mutare]['linie'])
    pozitie_noua = random.choice(
        list(dictionar_posibilitati_mutare[pion_ales_pentru_mutare]))
    pozitie_noua_str = chr(pozitie_noua[1] + 65) + str(pozitie_noua[0])
    print("Calculatorul a mutat pionul", pion_ales_pentru_mutare, "la pozitia",
          pozitie_noua_str)
    realizare_tranzitie(pozitie_veche_pion_ales, pozitie_noua_str,
                        configuratie_curenta['negre'], -1)


def joaca(configuratie: dict, matrice: list):
    """
        Functie ce consta in desfasurarea jocului de sah
    :param configuratie:
    :param matrice:
    :return:
    """
    global configuratie_curenta, matrice_configuratie_anterioara, \
        matrice_configuratie_curenta
    configuratie_curenta = configuratie
    matrice_configuratie_anterioara = list(matrice)
    matrice_configuratie_curenta = list(matrice)
    # rand_jucator = random.choice([False, True])
    rand_jucator = True
    while not stare_finala(matrice_configuratie_curenta):
        afiseaza_tabla_joc(matrice_configuratie_curenta)
        if rand_jucator:
            joaca_utilizatorul()
            rand_jucator = False
        else:
            joaca_calculatorul()
            rand_jucator = True
        print()
        print()
    afiseaza_tabla_joc(matrice_configuratie_curenta)
