def sterge_din_configuratie_piesele_mancate(tabla: list,
                                            configuratie_jucator: dict):
    piesa_mancata = -1
    for piesa in configuratie_jucator.items():
        if tabla[piesa[1]['linie']][ord(piesa[1]['coloana']) - 65] != 'N':
            piesa_mancata = piesa[0]
            break
    if piesa_mancata is not -1:
        configuratie_jucator.pop(piesa_mancata)


def afiseaza_tabla_joc(matrice):
    """
        Metoda ce va afisa in consola tabla de sah
    :param matrice:
    :return:
    """
    for i in range(7, -1, -1):
        linie_tabla = str(i)
        for j in range(0, 8):
            linie_tabla = linie_tabla + "|" + matrice[i][j]
        linie_tabla += "|"
        print(linie_tabla)
    print(" ", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


def get_pozitie(pozitie: str) -> tuple:
    """
        Functie ce converteste A5 -> in coordonatele in matrice
    :param pozitie:
    :return:
    """
    return int(pozitie[1]), ord(pozitie[0]) - 65


def get_piesa_din_dictionar(piesa: str, configuratie_jucator: dict) -> int:
    """
        Returneaza piesa din dictionar ce se afla la o anumita pozitie
    :param piesa:
    :param culoare_jucator:
    :return:
    """
    linie, coloana = get_pozitie(piesa)
    for piesa in configuratie_jucator.keys():
        if configuratie_jucator[piesa]['linie'] == linie and \
                                ord(configuratie_jucator[piesa]['coloana']) -\
                                65 == coloana:
            return piesa
