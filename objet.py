from vecteurs import vecteur
from couleurs import couleur
import copy

class sphere:
    
    def __init__(self,x,y,z,rayon):
        self.position = vecteur(x,y,z)
        self.rayon = rayon
    
    def intersection(self,rayon,CAMERA):
        a = rayon.ndirection.prod_scalaire(rayon.ndirection)
        #b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) on pose b = 2d on a donc une équation simplifiée
        d = rayon.ndirection.prod_scalaire(rayon.origine-self.position)
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-a*c

        if discriminant >= 0:
            t1 = (-d-discriminant)/a
            t2 = (-d+discriminant)/a
            
            if t1*rayon.ndirection.z <= CAMERA[2]:
                if abs(t1)>1e3 or abs(t1)<0.001:
                    return False,None,None
                return True,t1,"DANS"
            
            elif t2*rayon.ndirection.z <= CAMERA[2]:
                if abs(t2)>1e3 or abs(t2)<0.001:
                    return False,None,None
                return True,t2,"HORS"
            
            else:
                return False,None
        else:
            return False,None
    
    
    def normale(self,ray,CAMERA):

        p = ray.origine + ray.direction*self.intersection(ray,CAMERA)[1]
        normale = (p-self.position).normaliser()
        return normale
    
    def couleur_inter(self,ray):
        return couleur(1,0,0)
    
class surface:
    def __init__(self,type,val):
        self.type = type
        self.val = val
    
    def intersection(self,rayon,CAMERA):
        
        def test_position(rayon,CAMERA):
                position = rayon.ndirection.prod_scalaire(self.normale(rayon,CAMERA))
                if position < 0:
                    return "HORS"
                else:
                    return "DANS"
        
        if self.type == "x" and rayon.ndirection.x != 0:
            t = (self.val-rayon.origine.x)/rayon.ndirection.x
            
            if abs(t)>1e3 or t<0.001:
                return False,None,None
            
            if t*rayon.ndirection.z <= CAMERA[2]:
                return True,t,test_position(rayon,CAMERA)

        
        if self.type == "y" and rayon.ndirection.y != 0:
            
            t = (self.val-rayon.origine.y)/rayon.ndirection.y
            
            if abs(t)>1e3 or t<0.001:
                
                return False,None,None
            
            if t*rayon.ndirection.z <= CAMERA[2]:
                return True,t,test_position(rayon,CAMERA)

        
        if self.type == "z" and rayon.ndirection.z != 0:
            
            t = (self.val-rayon.origine.z)/rayon.ndirection.z
            
            if abs(t)>1e3 or t<0.001:
                return False,None,None
            
            if t*rayon.ndirection.z <= CAMERA[2]:
                

                return True,t,test_position(rayon,CAMERA)
        
        return False,None,None

    def normale(self,ray,CAMERA):
        if self.type == "x":
            return vecteur(1,0,0)
        if self.type == "y":
            return vecteur(0,1,0)
        if self.type == "z":
            return vecteur(0,0,1)
    
    def couleur_inter(self,ray):

        r = 0.8
        g = 0.8
        b = 0
    
        
        return couleur(r,g,b)



def test_intersection(ray,scene,CAMERA):
    scene_obj = copy.copy(scene)
    list_t = [None for i in scene]
    list_posi = [None for i in scene]
    inter = False

    
    for objet_scene_index in range(len(scene_obj)):
        intersect = scene_obj[objet_scene_index].intersection(ray,CAMERA)
        

        if intersect[0]:
            inter = True

            list_t[objet_scene_index] = intersect[1]
            list_posi[objet_scene_index] = intersect[2]
    
    if not(inter):
        return False,None
    
    while None in list_t:
        index = list_t.index(None)
        scene_obj.pop(index)
        list_t.pop(index)
        list_posi.pop(index)
        
    return True,scene_obj[list_t.index(min(list_t))],min(list_t),list_posi[list_t.index(min(list_t))]
    

























    









