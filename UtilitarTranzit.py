from math import fabs

def este_pe_tabla(linie: int, coloana: int):
    if 0 <= linie <= 7 and 0 <= coloana <= 7:
        return True
    return False


def mutare_valida_inainte(tabla: list(list), ln_init: int, ln_fin: int, col: int):
    if fabs(ln_init - ln_fin) > 2 or fabs(ln_init - ln_fin) < 1:
        return False
    for ln in range(ln_init, ln_fin + 1):
        if tabla[ln][col] is not 0:
            return False
    return True


def mutare_valida_in_diag(tabla: list(list), ln_init: int, col_init: int, ln_fin: int, col_fin: int):
    if not este_pe_tabla(ln_fin, col_fin):
        return False
    if fabs(ln_init - ln_fin) is not 1 or fabs(col_init - col_fin) is not 1:
        return False
    if tabla[ln_fin][ln_init] is 0:
        return False
    return True


def mutare_in_fata_cu_2_poz(ln_init: int, ln_fin: int, col: int):



def mutare_en_passant_valida(tab)


