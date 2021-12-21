'''
Holds all the dustbin objects and is used for
creation of chromosomes by jumbling their sequence
'''
from dustbin import *

class DustbinManager:

    dustbins = []
    dustbinsPos = []
    
    @classmethod
    def addDustbin (self, db):
        self.dustbins.append(db)
        self.dustbinsPos.append([db.x, db.y])

    @classmethod
    def getDustbin (self, index):
        return self.dustbins[index]

    @classmethod
    def numberOfDustbins(self):
        return len(self.dustbins)

    @classmethod
    def getAllDustbins(self):
        return self.dustbins

    @classmethod
    def getAllDustbinsPos(self):
        return self.dustbinsPos

