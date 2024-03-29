def obtine_culoare_dupa_sens(sens: int):
    """
    Functie de returneaza culoarea pioanelor in functie de sensul in care merg
    :param sens:
    :return: Sensul pionului primit ca parametru
    """
    if sens > 0:
        return 'A'
    return 'N'


def este_pe_tabla(linie: int, coloana: int) -> bool:
    """
    Functie ce verifica date coordonatele primite ca parametru sunt in interiorul tablei
    :param linie:
    :param coloana:
    :return:  True -> Daca pozitia este in interiorul table
              False -> Altfel
    """
    return 0 <= linie <= 7 and 0 <= coloana <= 7


def mutare_valida_inainte(tabla: list, ln_act: int, ln_urm: int, col: int,
                          sens: int) -> bool:
    """
        Metoda ce valideaza daca o miscare inainte este valida
    :param tabla:
    :param ln_act:
    :param ln_urm:
    :param col:
    :param sens:
    :return:
    """
    return tabla[ln_urm][col] == '0' and tabla[ln_act + sens][col] == '0'


def mutare_valida_normala_in_diag(tabla: list, ln_urm: int, col_urm: int,
                                  sens: int) -> bool:
    """
        Functie ce valideaza daca miscarea pe care se doreste sa se realizeze in diagonala este valida
    :param tabla: Matricea actuala ( Configuratia matricei , inainte sa fac miscarea pe care o doresc sa o fac)
    :param ln_urm: Linia urmatoare (Linia pe care doresc sa mut pionul)
    :param col_urm: Coloana urmatoare (Coloana pe care doressc sa mut pionul)
    :param sens: Sensul in care trebuie sa se mute pionul
    :return:
    """
    culoare_adv = obtine_culoare_dupa_sens(sens * -1)
    return tabla[ln_urm][col_urm] == culoare_adv


def pion_mutat_cu_2_poz(tabla_prec: list, tabla_act: list, ln_prec_pion: int,
                        col_prec_pion: int, ln_act_pion: int,
                        col_act_pion: int, culoare: str) -> bool:
    return tabla_prec[ln_prec_pion][col_prec_pion] == culoare \
           and tabla_prec[ln_act_pion][col_act_pion] == '0' \
           and tabla_act[ln_prec_pion][col_prec_pion] == '0' \
           and tabla_act[ln_act_pion][col_act_pion] == culoare


def mutare_en_passant_valida(tabla_prec: list, tabla_act: list, ln_act: int,
                             ln_urm: int, col_urm: int, sens: int) \
        -> bool:
    """
        Functia ce valideaza o miscare en_passant
    :param tabla_prec: Matrice anterioara ( Configuratia matricei , inainte sa fac miscarea pe care o doresc sa o fac)
    :param tabla_act: Matricea actuala ( Configuratia matricei , dupa ce am facut miscarea pe care doresc sa o fac)
    :param ln_act: Linia actuala (Linia pe care se afla pionul pe care vreau sa il mut)
    :param ln_urm: Linia urmatoare (Linia pe care doresc sa mut pionul)
    :param col_urm: Coloana urmatoare (Coloana pe care doressc sa mut pionul)
    :param sens: Sensul in care trebuie sa se mute pionul
    :return:
    """
    culoare_adv = obtine_culoare_dupa_sens(sens * -1)
    ln_prec_pion_adv = ln_act + 2 * sens
    col_prec_pion_adv = col_urm
    ln_act_pion_adv = ln_act
    col_act_pion_adv = col_urm
    return tabla_act[ln_urm][col_urm] == '0' \
           and pion_mutat_cu_2_poz(tabla_prec, tabla_act, ln_prec_pion_adv,
                                   col_prec_pion_adv, ln_act_pion_adv,
                                   col_act_pion_adv, culoare_adv)


def mutare_valida_in_diag(tabla_prec: list, tabla_act: list, ln_act: int,
                          ln_urm: int, col_urm: int, sens: int) -> bool:
    """
        Functia ce valideaza daca o miscare in diagonala este valida
    :param tabla_prec: Matrice anterioara ( Configuratia matricei , inainte sa fac miscarea pe care o doresc sa o fac)
    :param tabla_act: Matricea actuala ( Configuratia matricei , dupa ce am facut miscarea pe care doresc sa o fac)
    :param ln_act:  Linia actuala (Linia pe care se afla pionul pe care vreau sa il mut)
    :param ln_urm: Linia urmatoare (Linia pe care doresc sa mut pionul)
    :param col_urm: Coloana urmatoare (Coloana pe care doressc sa mut pionul)
    :param sens: Sensul in care trebuie sa se mute pionul
    :return:
    """
    return mutare_valida_normala_in_diag(tabla_act, ln_urm, col_urm, sens) \
           or mutare_en_passant_valida(tabla_prec, tabla_act, ln_act, ln_urm,
                                       col_urm, sens)


def mutare_valida_in_diag_jucator(tabla_prec: list, tabla_act: list,
                                  ln_act: int, col_act: int, ln_urm: int,
                                  col_urm: int, sens: int) -> bool:
    """
        Functie ce valideaza o miscare pe care utilizatorul doreste sa o realizeze inainte
    :param tabla_prec: Matricea precedenta
    :param tabla_act:  Matricea actuala
    :param ln_act:  Linia actuala (Linia pe care se afla pionul pe care vreau sa il mut)
    :param col_act:  Coloana actuala (Coloana pe care se afla pionul pe care vreau sa il mut)
    :param ln_urm:  Linia urmatoare (Linia pe care doresc sa mut pionul)
    :param col_urm: Coloana urmatoare (Coloana pe care doressc sa mut pionul)
    :param sens: Sensul in care trebuie sa se mute pionul
    :return:
    """
    return ln_urm == ln_act + sens and abs(col_urm - col_act) == 1 \
           and mutare_valida_in_diag(tabla_prec, tabla_act, ln_act, ln_urm,
                                     col_urm, sens)


def mutare_valida_inainte_jucator(tabla: list, ln_act: int, col_act: int,
                                  ln_urm: int, col_urm, sens: int) -> bool:
    """
        Functie ce valideaza o miscare pe care utilizatorul doreste sa o realizeze inainte
    :param tabla: Matricea actuala
    :param ln_act:  Linia actuala
    :param col_act: Coloana actuala
    :param ln_urm:  Linia urmatoarea
    :param col_urm: Coloana urmatoare
    :param sens: Sensul in care trebuie sa se mute pionul
    :return:
    """
    return col_act == col_urm and 0 < (ln_urm - ln_act) * sens < 3 \
           and mutare_valida_inainte(tabla, ln_act, ln_urm, col_act, sens)


def mutare_valida_jucator(tabla_prec: list, tabla_act: list, ln_act: int,
                          col_act: int, ln_urm: int, col_urm: int,
                          sens: int) -> bool:
    """
        Functie ce valideaza daca miscarea pe care utilizatorul doreste sa o realizeze este valida
    :param tabla_prec: Matricea precedenta
    :param tabla_act: Matricea actuala
    :param ln_act:  Linia actuala
    :param col_act:  Coloana actuala
    :param ln_urm:  Linia urmatoarea
    :param col_urm: Coloana urmatoare
    :param sens: Sensul in care trebuie sa se mute pionul
    :return: True -> Daca tranzitia dorita este una valida
            False -> Altfel
    """
    return este_pe_tabla(ln_urm, col_urm) \
           and (mutare_valida_inainte_jucator(tabla_act, ln_act, col_act,
                                              ln_urm, col_urm, sens)
                or mutare_valida_in_diag_jucator(tabla_prec, tabla_act,
                                                 ln_act, col_act, ln_urm,
                                                 col_urm, sens))
