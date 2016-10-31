from stari import *
from UtilitarTranzit import *
import sys

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()
miscare_en_passant = (0, 0)


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
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, configuratie_curenta
    ln_urm, col_urm = get_pozitie(miscare)
    ln_act, col_act = get_pozitie(pion)
    pozitie = get_piesa_din_dictionar(pion, 'albe')

    if abs(ln_urm - ln_act) == 2 and col_act == col_urm and configuratie_curenta['albe'][pozitie]['pas2'] == False:
        return False

    mutarea_este_valida = mutare_valida_jucator(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act,
                                                col_act, ln_urm,
                                                col_urm, 1)

    if mutarea_este_valida:
        if mutare_valida_en_passant(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act, ln_urm,
                                    col_urm, 1):
            global miscare_en_passant
            miscare_en_passant = (ln_urm, col_urm)

    return mutare_valida_jucator(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act, col_act, ln_urm,
                                 col_urm, 1)


def realizare_tranzitie(piesa_mutata: str, noua_pozitie: str, jucator: str, culoare_jucator: str):
    """
        Functie ce realizeaza operatiile necesare realizarii unei tranzitii
    :param piesa_mutata:
    :param noua_pozitie:
    :param jucator:
    :param culoare_jucator:
    :return:
    """
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, configuratie_curenta, miscare_en_passant
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    matrice_configuratie_anterioara = [list(x) for x in matrice_configuratie_curenta]
    matrice_configuratie_curenta[linie_veche][coloana_veche] = '0'
    matrice_configuratie_curenta[linie_noua][coloana_noua] = jucator
    pion = get_piesa_din_dictionar(piesa_mutata, culoare_jucator)
    configuratie_curenta[culoare_jucator][pion]['pas2'] = False
    configuratie_curenta[culoare_jucator][pion]['linie'], configuratie_curenta[culoare_jucator][pion][
        'coloana'] = linie_noua, chr(coloana_noua + 65)

    if miscare_en_passant[0] == linie_noua and miscare_en_passant[1] == coloana_noua:
        # Am ales sa fac miscarea en-passant
        # Trebuie sa mananc piesa
        # Determin ce jucator a realizat en_passant
        if jucator == 'A':
            matrice_configuratie_curenta[linie_noua - 1][coloana_noua] = '0'
        else:
            matrice_configuratie_curenta[linie_noua + 1][coloana_noua] = '0'

    # Resetez valoare miscarii empasant
    miscare_en_passant = (0, 0)


def joaca_utilizatorul():
    """
        Functie ce reprezenta actiunea realizata de utilizator
    :return:
    """
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

    if este_pe_tabla(ln_urm, col_urm) and \
            mutare_valida_en_passant(matrice_configuratie_anterioara,
                                     matrice_configuratie_curenta, ln_act, ln_urm, col_urm,
                                     -1):
        global miscare_en_passant
        miscare_en_passant = (ln_urm, col_urm)
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
    # dam drop la piesa recent mancata
    piesa_mancata = -1
    for piesa in configuratie_curenta['negre'].items():
        if matrice_configuratie_curenta[piesa[1]['linie']][ord(piesa[1]['coloana']) - 65] != 'N':
            piesa_mancata = piesa[0]
            break
    if piesa_mancata is not -1:
        configuratie_curenta['negre'].pop(piesa_mancata)

    dictionar_strategie_ofensiva = calculeaza_lista_adiacenta(strategie_ofensiva)
    dictionar_strategie_defensiva = calculeaza_lista_adiacenta(strategie_defensiva)
    dictionar_combinat = combina_dictionare(dictionar_strategie_defensiva, dictionar_strategie_ofensiva)

    dictionar_lista_adiacenta = dict()

    for item in dictionar_combinat.items():
        item_set = set(filter(lambda tup: culoar_liber_pana_la_capat(matrice_configuratie_curenta, tup[0], tup[1]),
                              item[1]))

        if len(item_set) > 0:
            dictionar_lista_adiacenta[item[0]] = item_set

    if len(dictionar_lista_adiacenta) == 0:
        dictionar_lista_adiacenta = dict(filter(lambda itemy: len(itemy[1]) > 0, dictionar_combinat.items()))

    lista_strategii = [strategie_defensiva, strategie_ofensiva]
    index = -1

    while len(dictionar_lista_adiacenta) == 0 and len(lista_strategii) > 0:
        print(dictionar_lista_adiacenta)
        index += 1
        strategie = lista_strategii[index]
        # lista_strategii.remove(strategie)
        if strategie is strategie_defensiva:
            dictionar_lista_adiacenta = dictionar_strategie_defensiva
        elif strategie is strategie_ofensiva:
            dictionar_lista_adiacenta = dictionar_strategie_ofensiva

    print(dictionar_lista_adiacenta)
    if len(dictionar_lista_adiacenta) == 0:
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
            linie_tabla = linie_tabla + " " + matrice_configuratie_curenta[i][j]
        print(linie_tabla)
    print(" ", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


def joaca(configuratie: dict, matrice: list):
    """
          Functie ce consta in desfasurarea jocului de sah
    :param configuratie:
    :param matrice:
    :return:
    """
    global configuratie_curenta, matrice_configuratie_anterioara, matrice_configuratie_curenta
    configuratie_curenta = configuratie
    matrice_configuratie_anterioara = list(matrice)
    matrice_configuratie_curenta = list(matrice)
    # rand_jucator = random.choice([False, True])
    rand_jucator = True
    lista_strategii = [strategie_ofensiva, strategie_defensiva]
    while not stare_finala(matrice_configuratie_curenta):
        afiseaza_tabla_joc()
        if rand_jucator:
            joaca_utilizatorul()
            rand_jucator = False
        else:
            joaca_calculatorul()
            rand_jucator = True
        print()
        print()
