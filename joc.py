from stari import *
from UtilitarTranzit import *
import sys

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()


def validare_sintaxa_miscare(miscare: str):
    """
        Functie ce valideaza daca miscarea introdusa de utilizator este una valida din punct de vedere sintaxic
    :param miscare:
    :return:
    """
    if len(miscare) == 2 and miscare[0].isalpha() and 'A' <= miscare[0] <= 'H' and miscare[1].isdigit() and 0 <= int(
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


def get_pozitie(pozitie: str) -> tuple:
    """
        Functie ce converteste A5 -> in coordonatele in matrice
    :param pozitie:
    :return:
    """
    return int(pozitie[1]), ord(pozitie[0]) - 65


def get_piesa_din_dictionar(piesa: str, culoare_jucator: str) -> int:
    """
        Returneaza piesa ce din dictionar ce o afla la o anumita pozitie
    :param piesa:
    :param culoare_jucator:
    :return:
    """
    linie, coloana = get_pozitie(piesa)
    for piesa in configuratie_curenta[culoare_jucator].keys():
        if configuratie_curenta[culoare_jucator][piesa]['linie'] == linie and \
                                ord(configuratie_curenta[culoare_jucator][piesa]['coloana']) - 65 == coloana:
            return piesa


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
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, configuratie_curenta
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    matrice_configuratie_anterioara = [list(x) for x in matrice_configuratie_curenta]
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
                if not mut_piesa_mea(matrice_configuratie_curenta, piesa_mutata, 'A'):
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


def incearca_k_pasi_inainte(ln_act: int, col_act: int, lista_adiacenta: set, strategie, nr_pasi: int):
    """
        Functie ce determina posibilele miscari cu k pasi inainte
    :param ln_act:
    :param col_act:
    :param lista_adiacenta:
    :param strategie:
    :param nr_pasi:
    :return:
    """
    ln_urm = ln_act - nr_pasi
    col_urm = col_act
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_inainte(matrice_configuratie_curenta, ln_act, ln_urm, col_urm, -1) \
            and strategie(ln_urm, col_urm):
        lista_adiacenta.add((ln_urm, col_urm))


def incearca_deplasare_in_diag(ln_act: int, col_act: int, lista_adiacenta: set, strategie, deplasare):
    """
        Functie ce determina posibilele miscare in diagonala
    :param ln_act:
    :param col_act:
    :param lista_adiacenta:
    :param strategie:
    :param deplasare:
    :return:
    """
    ln_urm = ln_act - 1
    col_urm = col_act + deplasare
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act, ln_urm,
                                      col_urm, -1) \
            and strategie(ln_urm, col_urm):
        lista_adiacenta.add((ln_urm, col_urm))


def calculeaza_lista_adiacenta(strategie):
    """
        Functie ce determina lista de adicaenta a fiecarui pion , un functie de strategie primita ca parematru
    :param strategie: Strategia in functie de care trebuie sa determinam listele de adiacenta
    :return:
    """
    dictionar_lista_adiacenta = dict()
    for piesa in configuratie_curenta['negre'].items():
        linie, coloana = piesa[1]['linie'], ord(piesa[1]['coloana']) - 65
        lista_adiacenta = set()

        incearca_k_pasi_inainte(linie, coloana, lista_adiacenta, strategie, 1)
        if piesa[1]['pas2']:
            incearca_k_pasi_inainte(linie, coloana, lista_adiacenta, strategie, 2)

        incearca_deplasare_in_diag(linie, coloana, lista_adiacenta, strategie, -1)
        incearca_deplasare_in_diag(linie, coloana, lista_adiacenta, strategie, +1)

        if len(lista_adiacenta) is not 0:
            dictionar_lista_adiacenta[piesa[0]] = lista_adiacenta
    return dictionar_lista_adiacenta


def combina_dictionare(dict1: dict, dict2: dict):
    dict_to_return = dict()
    for key in dict1.keys():
        dict_to_return[key] = dict1[key]
    for key in dict2.keys():
        if key in dict_to_return.keys():
            dict_to_return[key] &= dict2[key]
        else:
            dict_to_return[key] = dict2[key]
    return dict_to_return


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

    dictionar_lista_adiacenta = dict()

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

    pion_ales_pentru_mutare = random.choice(list(dictionar_lista_adiacenta.keys()))
    pozitie_veche_pion_ales = configuratie_curenta['negre'][pion_ales_pentru_mutare]['coloana'] + \
                              str(configuratie_curenta['negre'][pion_ales_pentru_mutare]['linie'])
    pozitie_noua = random.choice(list(dictionar_lista_adiacenta[pion_ales_pentru_mutare]))
    realizare_tranzitie(pozitie_veche_pion_ales, chr(pozitie_noua[1] + 65) + str(pozitie_noua[0]), 'N', 'negre')


def strategie_ofensiva(ln_urm: int, col_urm: int):
    """
        Functie ce va verifica daca o posibila miscare este una ofensiva
    :param ln_urm: O posibila linie pe care pot sa ma duc
    :param col_urm:  O posibili coloana pe care pot sa ma duc
    :return:
    """
    return matrice_configuratie_curenta[ln_urm][col_urm] == 'A'


def strategie_defensiva(linie: int, coloana: int):
    """
        Functie ce va verifica daca o posibile miscare este una defensiva
    :param linie: O posibila linie pe care pot sa ma duc
    :param coloana: O posibila coloana pe care pot sa ma duc
    :return:
    """
    stare_stanga_coloana = coloana - 1
    stare_jos_linie = linie - 1
    stare_dreapta_coloana = coloana + 1

    flag_stanga = False
    flag_drepta = False

    if este_pe_tabla(stare_jos_linie, stare_stanga_coloana):
        if matrice_configuratie_curenta[stare_jos_linie][stare_stanga_coloana] != 'A':
            flag_stanga = True
    else:
        flag_stanga = True

    if este_pe_tabla(stare_jos_linie, stare_dreapta_coloana):
        if matrice_configuratie_curenta[stare_jos_linie][stare_dreapta_coloana] != 'A':
            flag_drepta = True
    else:
        flag_drepta = True

    return flag_stanga and flag_drepta


def afiseaza_tabla_joc():
    """
        Metoda ce va afisa in consola tabla de has
    :return:
    """
    global matrice_configuratie_curenta
    for i in range(7, -1, -1):
        linie_tabla = str(i)
        for j in range(0, 8):
            linie_tabla = linie_tabla + " " +matrice_configuratie_curenta[i][j]
        print(linie_tabla)
    print(" ", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


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
