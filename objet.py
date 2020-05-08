from vecteurs import vecteur
from couleurs import couleur
import copy
import math
import matplotlib.pyplot as plt
import numpy as np
from rayons import rayon
import random


class materiel:
    def __init__(self,**kwargs):

        """matériaux possibles: verre ; mat ; métal"""
        """args: couleur_obj, type_obj, indice_reflextion (0 à 1), indice_refraction"""
        
        
        type_obj =  kwargs["type_obj"]
        
        
        if not(type_obj in ["verre","mat","métal"]):
            raise TypeError("matériel non connu")
        
        self.type_obj = type_obj
        try:
            self.couleur_obj = kwargs["couleur_obj"]
        except:
            self.couleur_obj = couleur(0,0,0)
        try:
            self.indice_reflexion = kwargs["indice_reflexion"]
        except:
            self.indice_reflexion = 0
        try:
            self.indice_refraction = kwargs["indice_refraction"]
        except:
            self.indice_refraction = 1

class sphere:
    
    def __init__(self,x,y,z,rayon,texture):
        self.position = vecteur(x,y,z)
        self.rayon = rayon
        
        self.texture = texture
    
    def intersection(self,rayon, debug = False):
        a = rayon.ndirection_decale.prod_scalaire(rayon.ndirection_decale)
        #b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) on pose b = 2d on a donc une équation simplifiée
        d = rayon.ndirection_decale.prod_scalaire(rayon.origine-self.position)
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-a*c
        
        if debug:
            print(a,d,c)
            print(discriminant)
            
        if discriminant >= 0:
            t1 = (-d-math.sqrt(discriminant))/a
            t2 = (-d+math.sqrt(discriminant))/a
        
            if debug:
                print(t1,t2)
                print("---")
                print(t2)
            
        
            if t1 >= 0:
                if abs(t1)>1e3:

                    return False,None,None
                return True,t1,"HORS"
            
            elif t2 >=0:
                if abs(t2)>1e3 or abs(t2)<0.01:

                    return False,None,None
                return True,t2,"DANS"
            
            else:
                return False,None
        else:
            return False,None
    
    
    def normale(self,ray):
        
        try:
            p = ray.origine + ray.ndirection_decale*self.intersection(ray)[1]
        except:
            print(ray)
            print(self.intersection(ray,True))
            raise TimeoutError
        normale = (p-self.position).normaliser()
        return normale
    
    def couleur_inter(self,ray,scene,*texture):
        
        if len(texture) == 1:
            texture = texture[0]
        else:
            texture = None
        
        couleur_coef = abs(ray.ndirection_decale.prod_scalaire(self.normale(ray)))
        
        if self.texture.type_obj == "mat" or texture == "mat":
            couleur_base = self.texture.couleur_obj         
            return (couleur_base+couleur_base*couleur_coef*2)/3
        
        if self.texture.type_obj == "métal" or texture == "métal":
            point_contact = ray.origine+ray.ndirection_decale*test_intersection(ray,scene)[2]
            
            normale_obj = self.normale(ray)
            ray.origine = point_contact
            ray.ndirection_decale = ray.ndirection_decale+2*normale_obj
            

            dx = random.uniform(-self.texture.indice_reflexion,self.texture.indice_reflexion)
            dy = random.uniform(-self.texture.indice_reflexion,self.texture.indice_reflexion)
            dz = random.uniform(-self.texture.indice_reflexion,self.texture.indice_reflexion)
            
            ray.ndirection_decale.x += dx
            ray.ndirection_decale.y += dy
            ray.ndirection_decale.z += dz
            
            
            inter = test_intersection(ray,scene)
            
            
            if inter[0]:
                
                if inter[1].texture.type_obj == "métal" or inter[1].texture.type_obj == "verre":
                    val_lum = 1
                else:
                    val_lum = test_lumiere(ray,scene,inter[1],inter[2])
                
                return (inter[1].couleur_inter(ray,scene)*val_lum+self.texture.couleur_obj*couleur_coef*2)/3
            
            else:
                return (couleur(0.7,0.7,1)+self.texture.couleur_obj)/2
            
        
        if self.texture.type_obj == "verre" or texture == "verre":
            
            normale_obj = self.normale(ray)
            
            inter = test_intersection(ray,scene)
            type_inter = inter[3]
            point_contact = ray.origine+ray.ndirection_decale*inter[2]
            

            
            if type_inter =="HORS":
                
                rapport_indice = 1/self.texture.indice_refraction
                
            
            else:
                normale_obj = -1*normale_obj
                rapport_indice = self.texture.indice_refraction
                
            
            #r2 = rapport_indice*(ray.ndirection_decale+(-1*(ray.ndirection_decale.prod_scalaire(normale_obj))*normale_obj))
            
            r = (-1*ray.ndirection_decale).prod_scalaire(normale_obj)*normale_obj
            r2 = rapport_indice*(ray.ndirection_decale+r)
            
            
            try:
                r1 = -1*math.sqrt(1-abs(r2)**2)*normale_obj

            
            except:
                
                #return self.couleur_inter(ray,scene,"métal")
                return couleur(0,1,0)

            
            ray.ndirection_decale = (r1+r2).normaliser()
            ray.origine = point_contact
            
            inter = test_intersection(ray,scene)
            ray.origine = ray.origine + ray.ndirection_decale*0.0001
            
            inter = test_intersection(ray,scene)
            
            if inter[0]:
                
                if inter[1].texture.type_obj == "métal" or inter[1].texture.type_obj == "verre":
                    val_lum = 1
                else:
                    val_lum = test_lumiere(ray,scene,inter[1],inter[2])
                

                return inter[1].couleur_inter(ray,scene)*val_lum

                
            
            else:
                return couleur(0.7,0.7,1)
            

            
            
            
            
            
    
    def debug_graf(self,rayon,type="DEUX"):
        distance = []
        t = list(np.linspace(-20,20,2000))
        
        for i in t:
            point = rayon.origine+i*rayon.ndirection
            d_temps = math.sqrt((point.x-self.position.x)**2 + (point.y-self.position.y)**2 + (point.z-self.position.z)**2)
            distance += [d_temps-self.rayon]
            #distance += [d_temps]
        
        
        a = rayon.ndirection.prod_scalaire(rayon.ndirection)
        d = rayon.ndirection.prod_scalaire(rayon.origine-self.position)
        
        
        b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) #on pose b = 2d on a donc une équation simplifiée
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-a*c

        if discriminant >= 0:
            t1 = (-d-math.sqrt(discriminant))/a
            t2 = (-d+math.sqrt(discriminant))/a
            plt.scatter(t1,0)
            plt.scatter(t2,0)
        
        
        x = np.linspace(-20,20,2000)
        y = a*x**2+b*x+c
        
        if type == "Deux":
            plt.plot(x,y,color="Red")
            plt.plot(t,distance,color="Blue")
        if type == "Bleu":
            plt.plot(t,distance,color="Blue")
        if type == "Rouge":
            plt.plot(x,y,color="Red")          
        plt.show()
    
    
class surface:
    def __init__(self,type,val,texture):
        self.type = type
        self.val = val
        self.texture = texture
    
    def intersection(self,ray):
        
        def test_position(ray):
                position = ray.ndirection_decale.prod_scalaire(self.normale(ray))
                if position < 0:
                    return "HORS"
                else:
                    return "DANS"
        
        if self.type == "x" and ray.ndirection_decale.x != 0:
            t = (self.val-ray.origine.x)/ray.ndirection_decale.x
            
            if abs(t)>1e3 or t<0.01:
                return False,None,None

            if t >= 0:
                return True,t,test_position(ray)

        
        if self.type == "y" and ray.ndirection_decale.y != 0:
            
            t = (self.val-ray.origine.y)/ray.ndirection_decale.y
            
            if abs(t)>1e3 or t<0.01:
                
                return False,None,None
            
            if t >= 0:
                return True,t,test_position(ray)

        
        if self.type == "z" and ray.ndirection_decale.z != 0:
            
            t = (self.val-ray.origine.z)/ray.ndirection_decale.z
            
            if abs(t)>1e3 or t<0.01:
                return False,None,None
            
            if t >= 0:
                return True,t,test_position(ray)
        
        return False,None,None

    def normale(self,ray):
        if self.type == "x":
            return vecteur(1,0,0)
        if self.type == "y":
            return vecteur(0,1,0)
        if self.type == "z":
            return vecteur(0,0,1)
    
    def couleur_inter(self,ray,scene):
        
        t = self.intersection(ray)[1]
        
        if ((ray.origine.x+ray.ndirection_decale.x*t)%1 <=0.5) ^ ((ray.origine.z+ray.ndirection_decale.z*t)%1 <=0.5):
            r = 0.8
            g = 0.8
            b = 0
        else:
            r = 0
            g = 0.8
            b = 0.8
    
       
        

        
        return couleur(r,g,b)




class lumiere:
    def __init__(self,x,y,z,intensite):
        self.position = vecteur(x,y,z)
        self.intensite = intensite
    
    def illumine(self,ray,scene):
        
        inter = test_intersection(ray,scene)
        
        if inter[0]:
            return 0.2
        else:
            return self.intensite
    
    def intersection(self,ray):
        return False,None,None



def test_lumiere(ray,scene,objet_origine,t):
    
    list_val = []
    for objet in scene:
        if type(objet) == lumiere:
            rayon_lum = rayon((ray.ndirection_decale.x*t+ray.origine.x,ray.ndirection_decale.y*t+ray.origine.y,ray.ndirection_decale.z*t+ray.origine.z),objet.position)
            val = objet.illumine(rayon_lum,scene)
            if val != "Global":
                val = abs(val*ray.ndirection_decale.prod_scalaire(objet_origine.normale(ray)))
            elif val == "Global":
                val = 1
            list_val += [val]
        
    return max(list_val)
        
            
            



def test_intersection(ray,scene):
    scene_obj = copy.copy(scene)
    list_t = [None for i in scene]
    list_posi = [None for i in scene]
    inter = False

    
    for objet_scene_index in range(len(scene_obj)):
        intersect = scene_obj[objet_scene_index].intersection(ray)
        

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
    

























    









