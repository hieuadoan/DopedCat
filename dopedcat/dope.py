import sys
from catkit import Gratoms
from catkit.build import molecule 
from catkit.gen.adsorption import Builder
from copy import copy

def doped_surface(slabGratoms,dopantString,dopantType='add',ini_surf_atoms=None):
    """ Add dopants to surface"""
    fin_surf_atoms_list = []
    dopant = molecule(dopantString)[0]

    if ini_surf_atoms is not None:   
        slabGratoms.set_surface_atoms(ini_surf_atoms)
    
    surf_atoms = slabGratoms.get_surface_atoms().tolist()
    builder = Builder(slabGratoms)
    if dopantType=='add':
        fin_slabs = builder.add_adsorbate(dopant, bonds=[0], index=-1)
        for i, fin_slab in enumerate(fin_slabs):
            new_surf_atoms = copy(surf_atoms)
            new_surf_atoms.append(new_surf_atoms[-1]+1) # Dopant becomes a surface atom
            fin_slabs[i].set_surface_atoms(new_surf_atoms)
    elif dopantType=='replace':
        sys.exit('Working on this')
    else:
        sys.exit('Dopant type has to be either \'add\' or \'replace\'. Please choose one!')

    return(fin_slabs)


"""
TODO: - Remove overlaped atoms configs
      - Doped surface by replacement 
"""


