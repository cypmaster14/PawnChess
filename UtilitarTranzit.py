from math import fabs


def este_pe_tabla(linie: int, coloana: int):
    if 0 <= linie <= 7 and 0 <= coloana <= 7:
        return True
    return False


def mutare_valida_inainte(tabla: list, ln_act: int, ln_urm: int, col: int, sens: int):
    if tabla[ln_urm][col] != 0 or tabla[ln_act + sens][col] != 0:
        return False
    return True


def mutare_valida_normala_in_diag(tabla: list, ln_urm: int, col_urm: int):
    if tabla[ln_urm][col_urm] != 0:
        return False
    return True


def mutare_en_passant_valida(tabla_prec: list, tabla_act: list, ln_act: int, col_urm: int, sens: int):
    ln_prec_piesa_adv = ln_act + 2 * sens
    col_prec_piesa_adv = col_urm
    ln_act_piesa_adv = ln_act
    col_act_piesa_adv = col_urm
    if tabla_prec[ln_prec_piesa_adv][col_prec_piesa_adv] != 0 \
            and tabla_prec[ln_act_piesa_adv][col_act_piesa_adv] == 0 \
            and tabla_prec[ln_prec_piesa_adv][col_prec_piesa_adv] == 0 \
            and tabla_act[ln_act_piesa_adv][col_act_piesa_adv] != 0:
        return True
    return False


def mutare_valida_in_diag(tabla_prec: list, tabla_act: list, ln_act: int, ln_urm: int, col_urm: int, sens: int):
    return mutare_valida_normala_in_diag(tabla_act, ln_urm, col_urm) \
           or mutare_en_passant_valida(tabla_prec, tabla_act, ln_act, col_urm, sens)
