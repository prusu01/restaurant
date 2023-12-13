#!/usr/bin/env python
class Solve:
    def __init__(self,locatie,buget):
        self.locatie=locatie
        self.buget=buget
        print(locatie + " " + buget)

    ##def querry(self):



    #def functie(self):
        #..... v ati prins de aici, ca sa ruleze aveti nevoie sa fie self in fiecare functie trimis ca parametru
        #alea puse in iniit se apeleaza mereu cu self.<nume variabila> si se considera variabile globale
        #va recomand sa nu folositi variabile globale
        #daca vreti sa folositi orice functie din clasa asta aveti nevoie sa o apelati asa self.<nume_functie>(parametrii)
