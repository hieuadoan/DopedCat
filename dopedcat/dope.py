import sys
from catkit import Gratoms
from catkit.build import molecule 
from catkit.gen.adsorption import Builder
from copy import copy
from ase.utils import natural_cutoffs
from ase.neighborlist import NeighborList

def OverlappedAtoms(atoms,mult=0.9,skin=0.):
    nc = natural_cutoffs(atoms,mult=mult)
    nl = NeighborList(nc,skin=skin,self_interaction=False,bothways=False)
    nl.update(atoms)
    indicesList = []
    for i, atom in enumerate(atoms):
        indices, offset = nl.get_neighbors(i)
        if indices.size!=0:
            indicesList.append(indices.tolist())
    return indicesList 

def doped_surface(slabGratoms,dopantString,dopantType='add',ini_surf_atoms=None):
    """ Add dopants to surface"""
    fin_surf_atoms_list = []
    dopant = molecule(dopantString)[0]

    if ini_surf_atoms is not None:   
        slabGratoms.set_surface_atoms(ini_surf_atoms)
    
    surf_atoms = slabGratoms.get_surface_atoms().tolist()
    builder = Builder(slabGratoms)
    if dopantType=='add':
        overlappedList = []
        fin_slabs = builder.add_adsorbate(dopant, bonds=[0], index=-1)
        for i, fin_slab in enumerate(fin_slabs):
            overlapped = OverlappedAtoms(fin_slab)
            if overlapped:
                overlappedList.append(i) 
            new_surf_atoms = copy(surf_atoms)
            new_surf_atoms.append(new_surf_atoms[-1]+1) # Dopant becomes a surface atom
            fin_slabs[i].set_surface_atoms(new_surf_atoms)
        
        for i in reversed(overlappedList):
            del(fin_slabs[i])

    elif dopantType=='replace':
        sys.exit('Working on this')
    else:
        sys.exit('Dopant type has to be either \'add\' or \'replace\'. Please choose one!')

    return(fin_slabs)


"""
TODO: - Remove overlapped atoms configs
      - Doped surface by replacement 
"""


