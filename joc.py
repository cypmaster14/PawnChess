from stari import *

configuratie_curenta = dict()
configutie_anterioara = dict()
matrice_configuratie = list()


def validare_sintaxa_miscare(miscare: str):
    if miscare[0].isalpha() and miscare[1].isdigit():
        return True
    return False


def mut_piesa_mea(matrice: list, linie: int, coloana: int, jucator: str):
    if matrice[linie][coloana] == jucator:
        return True
    return False


def get_pozitie(pozitie: str) -> tuple:
    return pozitie[1], ord(pozitie[0]) - 65


def get_piesa_in_dictionar(piesa: str) -> int:
    linie, coloana = get_pozitie(piesa)
    for piesa in configuratie_curenta.keys():
        if configuratie_curenta[piesa]['linie'] == linie and configuratie_curenta[piesa]['coloana'] == coloana:
            return piesa


def miscare_valida(conf_curente: dict, matrice_curent: list, pion, miscare):
    linie, coloana = get_pozitie(miscare)


def realizare_tranzitie(piesa_mutata: str, noua_pozitie: str, jucator: str):
    linie_noua, coloana_noua = get_pozitie(noua_pozitie)
    linie_veche, coloana_veche = get_pozitie(piesa_mutata)
    configutie_anterioara = configuratie_curenta
    matrice_configuratie[linie_veche][coloana_veche] = '0'
    matrice_configuratie[linie_noua][coloana_noua] = jucator
    pion = get_piesa_in_dictionar(piesa_mutata)
    configuratie_curenta[pion['linie']] = linie_noua
    configuratie_curenta[pion['coloana']] = coloana_noua


def joaca_utilizatorul():
    while True:
        try:
            piesa_mutata = input('Introduce-ti piesa pe care doriti sa o mutati(Ex:a2')
            if validare_sintaxa_miscare(piesa_mutata):
                if not mut_piesa_mea(matrice_configuratie, int(piesa_mutata[1]), ord(piesa_mutata) - 65, 'A'):
                    raise Exception('Nu a-ti mutat o piesa care va apartine')
            else:
                raise Exception('Eroare la sintaxa mutarii')
            pozitie_viitoare = input('Introduce-ti noua pozitie a piesei(Ex:a4')
            if validare_sintaxa_miscare(pozitie_viitoare):
                if miscare_valida(configuratie_curenta, matrice_configuratie, piesa_mutata, pozitie_viitoare.lower()):
                    realizare_tranzitie(piesa_mutata.lower(), pozitie_viitoare.lower(), 'A')
                    rand_jucator = False
                    break
                else:
                    raise Exception('Miscare invalida , incercati din nou')

            else:
                raise Exception('Eroare la sintaxa noi pozitii')
        except Exception as e:
            print(e)


def joaca_calculatorul():
    pass


def joaca(configuratie: dict, matrice: list):
    global configuratie_curenta, configuratie_curenta, matrice_configuratie
    configuratie_curenta = configuratie
    matrice_configuratie = matrice
    rand_jucator = random.choice([False, True])
    while not stare_finala(configuratie):
        if rand_jucator:
            joaca_utilizatorul()
        else:
            joaca_calculatorul()
