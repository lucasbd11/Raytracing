import math




class couleur:
    """class permettant de manipuler avec simplicité des couleurs"""
    
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b
    
    def __str__(self):
        return f"({self.r}r, {self.g}g, {self.b}b)"
        
    def __repr__(self):
        return f"couleur({self.r}r, {self.g}g, {self.b}b)"
    
    
    
    def __add__(self,autre):
        """surcharge de l'addition pour les couleurs"""
        
        r = self.r + autre.r
        g = self.g + autre.g
        b = self.b + autre.b
        
        return couleur(r,g,b)
        
    def __sub__(self,autre):
        """surcharge de la soustraction pour les couleurs"""
        
        r = self.r - autre.r
        g = self.g - autre.g
        b = self.b - autre.b
        
        return couleur(r,g,b)
    
    
    def __truediv__(self,valeur):
        """surcharge de la division pour les couleurs"""
        

        
        if type(valeur) == int or type(valeur) == float:
        
            r = self.r / valeur
            g = self.g / valeur
            b = self.b / valeur
            return couleur(r,g,b)
        
        else:
            raise TypeError("pas possible de multiplier une couleur avec autre chose qu'un entier ou flottant")


    def __mul__(self,valeur):
        """surcharge de la multiplication pour les couleurs"""
    
        if type(valeur) == int or type(valeur) == float:
        
            r = self.r * valeur
            g = self.g * valeur
            b = self.b * valeur
            return couleur(r,g,b)
        
        else:
            raise TypeError("pas possible de multiplier une couleur avec autre chose qu'un entier ou flottant'")
            
           
        
    def __rmul__(self,valeur):
        return self.__mul__(valeur)

























