from math import fabs


def obtine_culoare_dupa_sens(sens: int):
    if sens > 0:
        return 'A'
    return 'N'


def este_pe_tabla(linie: int, coloana: int):
    return 0 <= linie <= 7 and 0 <= coloana <= 7


def mutare_valida_inainte(tabla: list, ln_act: int, ln_urm: int, col: int, sens: int):
    return tabla[ln_urm][col] == '0' and tabla[ln_act + sens][col] == '0'


def mutare_valida_normala_in_diag(tabla: list, ln_urm: int, col_urm: int, sens: int):
    culoare_adv = obtine_culoare_dupa_sens(sens * -1)
    return tabla[ln_urm][col_urm] == culoare_adv


def mutare_en_passant_valida(tabla_prec: list, tabla_act: list, ln_act: int, ln_urm: int, col_urm: int, sens: int):
    culoare_adv = obtine_culoare_dupa_sens(sens * -1)
    ln_prec_piesa_adv = ln_act + 2 * sens
    col_prec_piesa_adv = col_urm
    ln_act_piesa_adv = ln_act
    col_act_piesa_adv = col_urm
    return (tabla_act[ln_urm][col_urm] == '0'
            and tabla_prec[ln_prec_piesa_adv][col_prec_piesa_adv] == culoare_adv
            and tabla_prec[ln_act_piesa_adv][col_act_piesa_adv] == '0'
            and tabla_prec[ln_prec_piesa_adv][col_prec_piesa_adv] == '0'
            and tabla_act[ln_act_piesa_adv][col_act_piesa_adv] == culoare_adv)


def mutare_valida_in_diag(tabla_prec: list, tabla_act: list, ln_act: int, ln_urm: int, col_urm: int, sens: int):
    return mutare_valida_normala_in_diag(tabla_act, ln_urm, col_urm, sens) \
           or mutare_en_passant_valida(tabla_prec, tabla_act, ln_act, ln_urm, col_urm, sens)


def mutare_valida_in_diag_jucator(tabla_prec: list, tabla_act: list, ln_act: int, col_act: int, ln_urm: int,
                                  col_urm: int, sens: int):
    return ln_urm == ln_act + sens and fabs(col_urm - col_act) == 1 \
           and mutare_valida_in_diag(tabla_prec, tabla_act, ln_act, ln_urm, col_urm, sens)


def mutare_valida_inainte_jucator(tabla: list, ln_act: int, col_act: int, ln_urm: int, col_urm, sens: int):
    return col_act == col_urm and 0 < fabs(ln_urm - ln_act) * sens < 3 \
           and mutare_valida_inainte(tabla, ln_act, ln_urm, col_act, sens)


def mutare_valida_jucator(tabla_prec: list, tabla_act: list, ln_act: int, col_act: int, ln_urm: int, col_urm: int,
                          sens: int):
    return este_pe_tabla(ln_urm, col_urm) \
           and (mutare_valida_inainte_jucator(tabla_act, ln_act, col_act, ln_urm, col_urm, sens)
                or mutare_valida_in_diag_jucator(tabla_prec, tabla_act, ln_act, col_act, ln_urm, col_urm, sens))
