import sys
from catkit import Gratoms
from catkit.build import molecule 
from catkit.gen.adsorption import Builder

def doped_surface(slabGratoms,dopantString,dopantType='add',surf_atoms=None):
    """ Add dopants to surface"""
    fin_surf_atoms_list = []
    dopant = molecule(dopantString)[0]

    if surf_atoms is not None:   
        slabGratoms.set_surface_atoms(surf_atoms)
    
    ini_surf_atoms = slabGratoms.get_surface_atoms().tolist()
    print(ini_surf_atoms)
    builder = Builder(slabGratoms)
    if dopantType=='add':
        fin_slabs = builder.add_adsorbate(dopant, bonds=[0], index=-1)
        for i, fin_slab in enumerate(fin_slabs):
            fin_surf_atoms = ini_surf_atoms.append(ini_surf_atoms[-1]+1) # Dopant becomes a surface atom
            fin_surf_atoms_list.append(fin_surf_atoms)
    elif dopantType=='replace':
        sys.exit('Working on this')
    else:
        sys.exit('Dopant type has to be either \'add\' or \'replace\'. Please choose one!')

    return(fin_slabs, fin_surf_atoms_list)
