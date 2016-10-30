from stari import *
from UtilitarTranzit import *
import sys

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()


def validare_sintaxa_miscare(miscare: str):
    if len(miscare) == 2 and miscare[0].isalpha() and 'A' <= miscare[0] <= 'H' and miscare[1].isdigit() and 0 <= int(
            miscare[1]) <= 8:
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
    global matrice_configuratie_anterioara, matrice_configuratie_curenta, configuratie_curenta
    ln_urm, col_urm = get_pozitie(miscare)
    ln_act, col_act = get_pozitie(pion)
    pozitie = get_piesa_din_dictionar(pion, 'albe')

    if abs(ln_urm - ln_act) == 2 and col_act == col_urm and configuratie_curenta['albe'][pozitie]['pas2'] == False:
        return False

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
    configuratie_curenta[culoare_jucator][pion]['pas2'] = False
    configuratie_curenta[culoare_jucator][pion]['linie'], configuratie_curenta[culoare_jucator][pion][
        'coloana'] = linie_noua, chr(coloana_noua + 65)


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


def incearca_k_pasi_inainte(ln_act: int, col_act: int, lista_adiacenta: set, strategie, nr_pasi: int):
    ln_urm = ln_act - nr_pasi
    col_urm = col_act
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_inainte(matrice_configuratie_curenta, ln_act, ln_urm, col_urm, -1) \
            and strategie(ln_urm, col_urm):
        lista_adiacenta.add((ln_urm, col_urm))


def incearca_deplasare_in_diag(ln_act: int, col_act: int, lista_adiacenta: set, strategie, deplasare):
    ln_urm = ln_act - 1
    col_urm = col_act + deplasare
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, ln_act, ln_urm,
                                      col_urm, -1) \
            and strategie(ln_urm, col_urm):
        lista_adiacenta.add((ln_urm, col_urm))


def calculeaza_lista_adiacenta(strategie):
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
        #lista_strategii.remove(strategie)
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
    return matrice_configuratie_curenta[ln_urm][col_urm] == 'A'


def strategie_defensiva(linie: int, coloana: int):
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
    global matrice_configuratie_curenta
    for i in range(7, -1, -1):
        print(i, matrice_configuratie_curenta[i])
    print()
    print(" ", ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])


def joaca(configuratie: dict, matrice: list):
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
