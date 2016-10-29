from stari import *
from UtilitarTranzit import *

configuratie_curenta = dict()
matrice_configuratie_curenta = list()
matrice_configuratie_anterioara = list()


def validare_sintaxa_miscare(miscare: str):
    if miscare[0].isalpha() and miscare[1].isdigit():
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
                        configuratie_curenta[culoare_jucator][piesa]['coloana'] == coloana:
            return piesa


def miscare_valida(conf_curente: dict, matrice_curent: list, pion: str, miscare: str):
    linie, coloana = get_pozitie(miscare)


def realizare_tranzitie(piesa_mutata: str, noua_pozitie: str, jucator: str, culoare_jucator: str):
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    matrice_configuratie_anterioara = matrice_configuratie_curenta
    matrice_configuratie_curenta[linie_veche][coloana_veche] = '0'
    matrice_configuratie_curenta[linie_noua][coloana_noua] = jucator
    pion = get_piesa_din_dictionar(piesa_mutata, culoare_jucator)
    configuratie_curenta[culoare_jucator][pion]['linie'] = linie_noua
    configuratie_curenta[culoare_jucator][pion]['coloana'] = coloana_noua


def joaca_utilizatorul():
    while True:
        try:
            piesa_mutata = input('Introduce-ti piesa pe care doriti sa o mutati(Ex:a2')
            if validare_sintaxa_miscare(piesa_mutata):
                if not mut_piesa_mea(matrice_configuratie_curenta, piesa_mutata, 'A'):
                    raise Exception('Nu a-ti mutat o piesa care va apartine')
            else:
                raise Exception('Eroare la sintaxa mutarii')
            pozitie_viitoare = input('Introduce-ti noua pozitie a piesei(Ex:a4')
            if validare_sintaxa_miscare(pozitie_viitoare):
                if miscare_valida(configuratie_curenta, matrice_configuratie_curenta, piesa_mutata,
                                  pozitie_viitoare.lower()):
                    realizare_tranzitie(piesa_mutata.lower(), pozitie_viitoare.lower(), 'A', 'albe')
                    rand_jucator = False
                    break
                else:
                    raise Exception('Miscare invalida , incercati din nou')

            else:
                raise Exception('Eroare la sintaxa noi pozitii')
        except Exception as e:
            print(e)


def joaca_calculatorul():
    # Calculatorul va juca mereu cu piesele negre

    dictionar_lista_adiacenta = dict()

    for piesa in configuratie_curenta['negre'].items():
        linie, coloana = piesa[1]['linie'], piesa[1]['coloana']
        lista_adiacenta = list()
        # Un pas in fata
        if mutare_valida_inainte(matrice_configuratie_curenta, linie, linie - 1, coloana, -1):
            lista_adiacenta.append((linie - 1, coloana))

        # Doi pasi in fara
        if piesa[1]['pas2'] == True and mutare_valida_inainte(matrice_configuratie_curenta, linie, linie - 2, coloana,
                                                              -1):
            lista_adiacenta.append((linie - 2, coloana))

        # Diagonala
        if coloana - 1 >= 0:
            if mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, linie, linie - 1,
                                     coloana - 1, -1):
                lista_adiacenta.append(linie - 1, coloana - 1)

        if coloana + 1 <= 7:
            if mutare_valida_in_diag(matrice_configuratie_anterioara, matrice_configuratie_curenta, linie, linie - 1,
                                     coloana + 1, -1):
                lista_adiacenta.append(linie - 1, coloana + 1)

        dictionar_lista_adiacenta[piesa[0]] = lista_adiacenta

        # Am determinat toate miscarile posibile, in functie de o strategie trebuie sa aleg o miscare


def joaca(configuratie: dict, matrice: list):
    global configuratie_curenta, matrice_configuratie_anterioara, matrice_configuratie_curenta
    configuratie_curenta = configuratie
    matrice_configuratie_anterioara = matrice
    matrice_configuratie_curenta = matrice
    rand_jucator = random.choice([False, True])
    while not stare_finala(configuratie):
        if rand_jucator:
            joaca_utilizatorul()
        else:
            joaca_calculatorul()
