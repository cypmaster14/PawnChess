from joc import *

nume_fisier = 'configuratie.json'
configuratie = dict()
configuratie['albe'], configuratie['negre'], matrice = stare_initiala()
print(configuratie)
joaca(configuratie, matrice)
print('Jocul s-a terminat')
