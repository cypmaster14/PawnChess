from UtilitarTranzit import *


def pozitii_laterale_sigure(tabla: list, linie: int, coloana: int):
    """
        Functie ce va verifica daca pozitiile laterale a pozitiei date sunt sigure
    :param tabla: Starea actuala a tablei de joc
    :param linie: Linia pozitiei
    :param coloana: Coloana pozitiei
    :return:
    """
    coloana_stanga = coloana - 1
    coloana_dreapta = coloana + 1

    flag_stanga = False
    flag_drepta = False

    if este_pe_tabla(linie, coloana_stanga):
        if tabla[linie][coloana_stanga] != 'A':
            flag_stanga = True
    else:
        flag_stanga = True

    if este_pe_tabla(linie, coloana_dreapta):
        if tabla[linie][coloana_dreapta] != 'A':
            flag_drepta = True
    else:
        flag_drepta = True

    return flag_drepta and flag_stanga


def este_pozitie_defensiva(tabla_act: list, linie: int,
                           coloana: int):
    ln_din_fata_mea = linie - 1
    if pozitii_laterale_sigure(tabla_act, ln_din_fata_mea, coloana):
        ln_prec_pion = linie - 2
        col_prec_pion = coloana
        # ma pozitionez temporar in pozitia in care as putea ajunge pt a vedea daca e avans cu 2 pasi
        posib_tabla_viit = [list(x) for x in tabla_act]
        posib_tabla_viit[ln_prec_pion][col_prec_pion] = '0'
        posib_tabla_viit[linie][coloana] = 'N'
        if mutare_en_passant_valida(tabla_act, posib_tabla_viit, ln_prec_pion,
                                    linie, coloana, -1):
            return pozitii_laterale_sigure(tabla_act, linie, coloana)
        else:
            return True
    else:
        return False


def obtine_liste_adiacenta_defensive(tabla_act: list, liste_adiacenta: dict):
    return dict(filter(lambda good_item: len(good_item[1]) > 0,
                       map(lambda item: [item[0], set(
                           filter(
                               lambda tuplu: este_pozitie_defensiva(tabla_act,
                                                                    tuplu[0],
                                                                    tuplu[1]),
                               item[1]))],
                           liste_adiacenta.items())))


def este_pozitie_ofensiva(tabla_prec: list, tabla_act: list, linie: int,
                          coloana: int):
    """
        Functie ce va verifica daca o posibila miscare este una ofensiva
    :param tabla_prec: Starea anterioara a tablei de joc
    :param tabla_act: Starea actuala a tablei de joc
    :param linie: O posibila linie pe care pot sa ma duc
    :param coloana: O posibila coloana pe care pot sa ma duc
    :return:
    """
    return tabla_act[linie][coloana] == 'A' or este_pozitie_en_passant(
        tabla_prec, tabla_act, linie, coloana, -1)


def obtine_liste_adiacenta_ofensive(tabla_prec: list, tabla_act: list,
                                    liste_adiacenta: dict):
    return dict(filter(lambda good_item: len(good_item[1]) > 0,
                       map(lambda item: [item[0], set(
                           filter(
                               lambda tuplu: este_pozitie_ofensiva(tabla_prec,
                                                                   tabla_act,
                                                                   tuplu[0],
                                                                   tuplu[1]),
                               item[1]))], liste_adiacenta.items())))


def este_culoar_liber(tabla: list, ln_act: int, col_act: int):
    """
        Functie ce determina daca pe o anumita coloana , incepand da la o anumita linie , am culoar liber
        ( pot inainta un numar de pasi fara sa risc sa fiu mancat)

    :param tabla:
    :param ln_act:
    :param col_act:
    :return: True -> Daca pe coloana actuala am culoar
             False -> Altfel
    """
    for i in range(ln_act, -1, -1):
        if tabla[i][col_act] != '0':
            return False
    return True


def obtine_liste_adiacenta_culoar_liber(tabla: list, liste_adiacenta: dict):
    return dict(filter(lambda good_item: len(good_item[1]) > 0,
                       map(lambda item: [item[0], set(
                           filter(
                               lambda tuplu: este_culoar_liber(tabla, tuplu[0],
                                                               tuplu[1]),
                               item[1]))],
                           liste_adiacenta.items())))


def obtine_liste_adiacenta_ofensive_sigure(lista_defensive: dict,
                                           lista_ofensive: dict):
    set_vid = set()  # multimea vida
    return dict(filter(lambda good_item: len(good_item[1]) > 0,
                       map(lambda item: [item[0],
                                         item[1] & lista_defensive.get(item[0],
                                                                       set_vid)],
                           lista_ofensive.items())))


def este_pozitie_en_passant(tabla_prec: list, tabla_act: list, ln_act: int,
                            col_act: int, sens: int):
    culoare_adv = obtine_culoare_dupa_sens(sens * -1)
    ln_prec_pion_adv = ln_act + sens
    col_prec_pion_adv = col_act
    ln_act_pion_adv = ln_act - sens
    col_act_pion_adv = col_act
    return este_pe_tabla(ln_prec_pion_adv, col_prec_pion_adv) and \
           este_pe_tabla(ln_act_pion_adv, col_act_pion_adv) and \
           pion_mutat_cu_2_poz(tabla_prec, tabla_act, ln_prec_pion_adv,
                               col_prec_pion_adv, ln_act_pion_adv,
                               col_act_pion_adv, culoare_adv)


def obtine_liste_adiacenta_en_passant(tabla_prec: list, tabla_act: list,
                                      liste_adiacenta_ofensive: dict):
    return dict(filter(lambda good_item: len(good_item[1]) > 0,
                       map(lambda item: [item[0], set(
                           filter(lambda tuplu: este_pozitie_en_passant(
                               tabla_prec, tabla_act, tuplu[0], tuplu[1], -1),
                                  item[1]))],
                           liste_adiacenta_ofensive.items())))


def obtine_liste_adiacenta_pericol(lista_defensive: dict,
                                   list_ofensive_nesigure: dict):
    return dict(filter(lambda item: item[0] in list_ofensive_nesigure.keys(),
                       lista_defensive.items()))
