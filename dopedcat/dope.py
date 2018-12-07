import sys
from catkit import Gratoms
from catkit.build import molecule 
from catkit.gen.adsorption import Builder

def doped_surface(slab,dopantString,dopantType='add',ini_surf_atoms=[]):
    """ Add dopants to surface"""
    slabs = []
    surf_atoms = []
    slab = Gratoms(slab)
    dopant = molecule(dopantString)[0]
    ini_slab = Builder(slab) 
    if not ini_surf_atoms:
        ini_slab.set_surface_atoms(ini_surf_atoms)
    
    if dopantType=='add':
        fin_slab = ini_slab.add_adsorbate(dopant, bonds=[0], index=-1)
        fin_surf_atoms = ini_surf_atoms.append(ini_surf_atoms[-1]+1) # Dopant becomes a surface atom
        slabs.append(fin_slab)
        surf_atoms.append(fin_surf_atoms)
    elif dopantType=='replace':
        sys.exit('Working on this')
    else:
        sys.exit('Dopant type has to be either \'add\' or \'replace\'. Please choose one!')
    
    return(slabs, surf_atoms)
