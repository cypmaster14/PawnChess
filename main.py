from joc import *

nume_fisier = 'config_init.json'
configuratie = dict()
configuratie['albe'], configuratie['negre'], matrice = incarca_stare(nume_fisier)
print(configuratie)
joaca(configuratie, matrice)
print('Jocul s-a terminat')

# print(dict(filter(lambda good_item: len(good_item[1]) > 0,
#                   map(lambda item: [item[0], set(
#                       filter(lambda tuplu: tuplu[0] * tuplu[1] > 0, item[1]))],
#                       {'1': {(1, 2), (2, 3), (-1, 2)}, '2': {(2, -3)}, '3': {(0, -4), (0, 8), (-2, -3)}, '4': {}}.items()))))