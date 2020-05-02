import math




class vecteur:
    """class permettant de manipuler avec simplicité des vecteurs, seul les opérations mathématiques utiles au programme seront implémentées"""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
        
    def __repr__(self):
        return f"vecteur({self.x}, {self.y}, {self.z})"
    
    def norme(self):
        return math.sqrt((self.x)**2+(self.y)**2+(self.z)**2)
    
    def prod_scalaire(self,vect):
        return self.x*vect.x + self.y*vect.y + self.z*vect.z
        
    def normaliser(self):
        return self / abs(self)
    
    def __add__(self,vect):
        """surcharge de l'addition pour les vecteurs"""
        
        x = self.x + vect.x
        y = self.y + vect.y
        z = self.z + vect.z
        
        return vecteur(x,y,z)
        
    def __sub__(self,vect):
        """surcharge de la soustraction pour les vecteurs"""
        
        x = self.x - vect.x
        y = self.y - vect.y
        z = self.z - vect.z
        
        return vecteur(x,y,z)
    
    
    def __truediv__(self,valeur):
        """surcharge de la division pour les vecteurs"""
        
        if type(valeur) != vecteur:
            try:
                x = self.x / valeur
                y = self.y / valeur
                z = self.z / valeur
            except:
                x = y = z = 0
            return vecteur(x,y,z)
        
        else:
            raise TypeError("pas possible de diviser 2 vecteurs")

    def __mul__(self,valeur):
        """surcharge de la multiplication pour les vecteurs"""
        
        
        if type(valeur) != vecteur:

            x = self.x * valeur
            y = self.y * valeur
            z = self.z * valeur

            return vecteur(x,y,z)
        
        else:
            raise TypeError("pas possible de multiplier 2 vecteurs")
            
           
        
    def __rmul__(self,valeur):
        return self.__mul__(valeur)

    def __abs__(self):
        """moyen plus simple d'obtenir la norme"""

        
        return self.norme()













































