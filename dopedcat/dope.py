import sys
from catkit import Gratoms
from catkit.build import molecule 
from catkit.gen.adsorption import Builder
from copy import copy
from ase.utils import natural_cutoffs
from ase.neighborlist import NeighborList

def offsetAdatoms(atoms,tol=1.):
    """ Check for off surface adatoms"""
    z_sum = 0
    offsetIdList = []
    tagList = atoms.get_tags()
    dopantList = [i for i,tag in enumerate(tagList) if tag==0]
    for i in dopantList:
        z_sum += atoms[i].position[2]
    avg_z = z_sum/len(dopantList)
    for i in dopantList:
        offset = atoms[i].position[2] - avg_z
        if offset > tol:
            offsetIdList.append(i)
    return offsetIdList

def overlappedAdatoms(atoms,mult=0.9,skin=0.):
    """ Check for overlapped dopants """
    nc = natural_cutoffs(atoms,mult=mult)
    nl = NeighborList(nc,skin=skin,self_interaction=False,bothways=False)
    nl.update(atoms)
    overlappedIdList = []
    for i, atom in enumerate(atoms):
        indices, offset = nl.get_neighbors(i)
        if indices.size!=0:
            overlappedIdList.append(indices.tolist())
    return overlappedIdList 

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
        offsetList = []
        fin_slabs = builder.add_adsorbate(dopant, bonds=[0], index=-1)
        for i, fin_slab in enumerate(fin_slabs):
            overlapped = overlappedAdatoms(fin_slab) # Check for ovelapped adatoms
            offset = offsetAdatoms(fin_slab) # Check for off surface adatoms
            if overlapped:
                overlappedList.append(i)
            if offset:
                offsetList.append(i) 
            new_surf_atoms = copy(surf_atoms)
            new_surf_atoms.append(new_surf_atoms[-1]+1) # Add dopant to list of surface atoms
            fin_slabs[i].set_surface_atoms(new_surf_atoms)

            tagList = fin_slab.get_tags()
            tagList[-1]=0   # Set tag of dopant to 0
            fin_slabs[i].set_tags(tagList)

        delList = overlappedList + offsetList
        delList = list(set(delList))
        delList.sort()
        if delList:
            for i in reversed(delList):
                del(fin_slabs[i])                   #Remove sturctures with overlapped dopants

    elif dopantType=='replace':
        sys.exit('Working on this')
    else:
        sys.exit('Dopant type has to be either \'add\' or \'replace\'. Please choose one!')

    return(fin_slabs)


"""
TODO:  - Doped surface by replacement 
"""

