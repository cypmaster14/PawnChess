from UtilitarFiltrare import *


def incearca_k_pasi_inainte(tabla: list, ln_act: int, col_act: int,
                            lista_adiacenta: set, nr_pasi: int):
    """
        Functie ce determina posibilele miscari cu k pasi inainte
    :param tabla:
    :param ln_act:
    :param col_act:
    :param lista_adiacenta:
    :param nr_pasi:
    :return:
    """
    ln_urm = ln_act - nr_pasi
    col_urm = col_act
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_inainte(tabla, ln_act, ln_urm, col_urm, -1):
        lista_adiacenta.add((ln_urm, col_urm))


def incearca_deplasare_in_diag(tabla_prec: list, tabla_act: list, ln_act: int,
                               col_act: int, lista_adiacenta: set,
                               deplasare):
    """
        Functie ce determina posibilele miscare in diagonala
    :param tabla_prec:
    :param tabla_act:
    :param ln_act:
    :param col_act:
    :param lista_adiacenta:
    :param deplasare:
    :return:
    """
    ln_urm = ln_act - 1
    col_urm = col_act + deplasare
    if este_pe_tabla(ln_urm, col_urm) \
            and mutare_valida_in_diag(tabla_prec, tabla_act, ln_act, ln_urm,
                                      col_urm, -1):
        lista_adiacenta.add((ln_urm, col_urm))


def calculeaza_liste_adiacenta(tabla_prec: list, tabla_act: list, configuratie_jucator: dict):
    """
        Functie ce determina lista de adicaenta a fiecarui pion , un functie de strategie primita ca parematru
    :param tabla_prec: Starea anterioara a tablei de joc
    :param tabla_act: Starea actuala a tablei de joc
    :param configuratie_jucator: Poztiile tuturor piselor ramase pe tabla ale unui jucator pe baza carora se calculeaza
    listele de adiacenta
    :return:
    """
    dictionar_lista_adiacenta = dict()
    for piesa in configuratie_jucator.items():
        linie, coloana = piesa[1]['linie'], ord(piesa[1]['coloana']) - 65
        lista_adiacenta = set()

        incearca_k_pasi_inainte(tabla_act, linie, coloana, lista_adiacenta, 1)
        if piesa[1]['pas2']:
            incearca_k_pasi_inainte(tabla_act, linie, coloana, lista_adiacenta,
                                    2)

        incearca_deplasare_in_diag(tabla_prec, tabla_act, linie, coloana,
                                   lista_adiacenta, -1)
        incearca_deplasare_in_diag(tabla_prec, tabla_act, linie, coloana,
                                   lista_adiacenta, +1)

        if len(lista_adiacenta) is not 0:
            dictionar_lista_adiacenta[piesa[0]] = lista_adiacenta
    return dictionar_lista_adiacenta
