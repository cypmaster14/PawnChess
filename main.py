import json
from PawnChess.stari import *

nume_fisier = 'configuratie.json'
configuratie = dict()
configuratie['albe'], configuratie['negre'], matrice = stare_initiala()
print(configuratie)
