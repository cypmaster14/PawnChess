import json
from stari import *

nume_fisier = 'configuratie.json'
configuratie = dict()
configuratie['albe'], configuratie['negre'], matrice = stare_initiala()
print(configuratie)
