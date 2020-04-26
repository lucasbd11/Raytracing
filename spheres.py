from vecteurs import vecteur

class sphere:
    
    def __init__(self,x,y,z,rayon):
        self.position = vecteur(x,y,z)
        self.rayon = rayon
    
    def intersection(self,rayon):
        a = rayon.ndirection.prod_scalaire(rayon.ndirection)
        #b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) on pose b = 2d on a donc une équation simplifiée
        d = rayon.ndirection.prod_scalaire(rayon.origine-self.position)
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-*a*c
        
        if discriminant >= 0:
            t = (-d-discriminant)/a
            return True,t
        
        else:
            return False,-1