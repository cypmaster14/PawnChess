from math import fabs


def este_pe_tabla(linie: int, coloana: int):
    if 0 <= linie <= 7 and 0 <= coloana <= 7:
        return True
    return False


def mutare_valida_inainte(tabla: list, ln_init: int, ln_fin: int, col: int):
    if fabs(ln_init - ln_fin) > 2 or fabs(ln_init - ln_fin) < 1:
        return False
    for ln in range(ln_init, ln_fin + 1):
        if tabla[ln][col] is not 0:
            return False
    return True


def mutare_valida_in_diag(tabla: list, ln_init: int, col_init: int, ln_fin: int, col_fin: int):
    if not este_pe_tabla(ln_fin, col_fin):
        return False
    if fabs(ln_init - ln_fin) is not 1 or fabs(col_init - col_fin) is not 1:
        return False
    if tabla[ln_fin][ln_init] is 0:
        return False
    return True


def mutare_in_fata_cu_2_poz(table: list, ln_init: int, ln_fin: int, coloana: int, semn: int):
    # Verific daca merg cum trebuie, unde ajung este liber si nu sar peste o piesa
    if (ln_fin - ln_init) * semn < 0 or table[ln_fin][coloana] != 0 or table[ln_init + semn][coloana] != 0:
        return False

    return True
