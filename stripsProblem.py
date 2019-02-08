# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python3 code Version 0.7.6 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Strips(object):
    def __init__(self, preconditions, effects, cost=1):
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost

class STRIPS_domain(object):
    def __init__(self, feats_vals, strips_map):
        self.actions = set(strips_map)  
        self.feats_vals = feats_vals
        self.strips_map = strips_map

boolean = {True, False}
sandwich_domain = STRIPS_domain(
    {'DLoc':{'fri', 'drw', 'pan', 'ben'}, 'DHB':boolean, 'DHC':boolean, 'DHK':boolean, 'CBN':boolean, 
    'DWS':boolean, 'DNB':boolean, 'DNC':boolean, 'DNK':boolean, 'CNS':boolean, 'BOB':boolean, 'COB':boolean},
    # Move clockwise from fridge Davids location now drawers.
    {'mc_fri': Strips({'DLoc':'fri'}, {'DLoc':'drw'}),
    # Move clockwise from drawers Davids location now pantry.
    'mc_drw': Strips({'DLoc':'drw'}, {'DLoc':'pan'}),
    # Move clockwise from pantry Davids location now bench.
    'mc_pan': Strips({'DLoc':'pan'}, {'DLoc':'ben'}),
    # Move clockwise from bench Davids location now fridge.
    'mc_ben': Strips({'DLoc':'ben'}, {'DLoc':'fri'}),
    # Move counter-clockwise from fridge Davids location now bench.
    'mcc_fri': Strips({'DLoc':'fri'}, {'DLoc':'ben'}),
    # Move counter-clockwise from drawers Davids location now fridge.
    'mcc_drw': Strips({'DLoc':'drw'}, {'DLoc':'fri'}),
    # Move counter-clockwise from pantry Davids location now drawers.
    'mcc_pan': Strips({'DLoc':'pan'}, {'DLoc':'drw'}),
    # Move counter-clockwise from bench Davids location now pantry.
    'mcc_ben': Strips({'DLoc':'ben'}, {'DLoc':'pan'}),
    # Pick up cheese - David must be at the fridge and not have cheese but need it, 
    # after action David has cheese.
    'puc' : Strips({'DLoc': 'fri', 'DNC':True , 'DHC':False}, {'DHC':True}),
    # Cheese to bench - David must be at the bench and have cheese, 
    # after action David does not have cheese but also does not need cheese and cheese is on bench.
    'ctb' : Strips({'DLoc': 'ben', 'DHC':True}, {'DHC':False, 'DNC':False, 'CBN':True}),
    # Pick up bread - David must be at pantry and not have bread but need it, after action David has bread.
    'pub' : Strips({'DLoc': 'pan', 'DHB':False, 'DNB':True}, {'DHB':True}),
    # Bread to bench - David must be at bench and have bread, 
    # after action David does not have bread but also does not need bread and bread is on bench.
    'btb' : Strips({'DLoc': 'ben', 'DHB':True}, {'DHB':False, 'DNB':False, 'BOB':True}),
    # Pick up knife - David must be at drawer and not have knife, after action David has knife.
    'puk' : Strips({'DLoc': 'drw', 'DHK':False, 'DNK':True}, {'DHK':True}),
    # Knife to bench - David must be at bench with the knife, after action David does not need knife.
    'ktb' : Strips({'DLoc': 'ben', 'DHK':True}, {'DNK':False}),
    # Slice cheese - David must be at bench with cheese and knife and cheese need slicing, after action cheese does not need slicing.
    'slc' : Strips({'DLoc': 'ben', 'CBN':True, 'DHK':True, 'CNS':True, 'BOB':True}, {'CNS':False, 'DHK':False}),
    # Put cheese on bread - David must be at bench with bread and cheese with it sliced and bread needs cheese, 
    # after action cheese is no longer on bench but on bread and David does not need sandwich!
    'pcb' : Strips({'DLoc': 'ben', 'BOB':True, 'CNS':False, 'COB':False, 'CBN':True }, {'DWS':False, 'COB':True, 'CBN':False})
    })

boolean = {True, False}
shed_domain = STRIPS_domain({'BHF':boolean, 'BHC':boolean, 'BHT':boolean, 'BHS':boolean, 'BHD':boolean, 'BHP':boolean,
                            'SHF':boolean, 'FHC':boolean, 'FHT':boolean, 'THS':boolean, 'SHD':boolean, 'SHP':boolean, 
                            'SNF':boolean, 'FNC':boolean, 'FNT':boolean, 'TNS':boolean, 'SND':boolean, 'SNP':boolean,
                            'SIC':boolean}, {
                            # Pick up frame - Builder has frame is false and slab needs frame is true, 
                            # afterwards builder has frame is true (slab needs frame is still true)
                            'puf' : Strips({'BHF':False, 'SNF':True}, {'BHF':True}),
                            # Fasten frame to slab - Slab needs frame is true and the builder has the frame,
                            # afterwards the builder no longer has the frame and the slab doesn't need it and slab has it, now the frame needs cladding.
                            'ffs' : Strips({'BHF':True, 'SNF':True, 'SHF':False},{'BHF':False, 'SNF':False, 'SHF':True, 'FNC':True}),
                            # Pick up cladding - Builder doesn't have cladding and the frame needs it,
                            # afterwards builder has cladding is true.
                            'puc' : Strips({'BHC':False, 'FNC':True}, {'BHC':True}),
                            # Fasten cladding to frame - Builder must have the cladding and the frame must needs cladding.
                            # Afterwards the builder no longer has cladding and the frame no longer needs it because it has it, now the frame needs trusses.
                            'fcf' : Strips({'BHC':True, 'FNC':True, 'FHC':False}, {'BHC':False, 'FNC':False, 'FHC':True, 'FNT':True}),
                            # Pick up trusses -  Builder doesn't have trusses but the frame needs them.
                            # Afterwards the builder has the trusses
                            'put' : Strips({'BHT':False, 'FNT':True},{'BHT':True}),
                            # Fasten trusses to frame - Builder has the trusses and the frame needs them.
                            # Afterwards the builder no longer had them, the frame doesn't need them because it has them already, now the trusses need shingles.
                            'ftf' : Strips({'BHT':True, 'FNT':True, 'FHT':False},{'BHT':False, 'FNT':False, 'FHT':True, 'TNS':True}),
                            # Pick up shingles - the trusses needs shingles and builder doesn't have them.
                            # afterwards the builder has the shingles.
                            'pus' : Strips({'BHS':False, 'TNS':True},{'BHS':True}),
                            # Fasten shingles to trusses - builder has the shingles and the trusses need them. 
                            # Afterwards builder no longer has shingles and the trusses do not need them because they have them, now the shed needs a door.
                            'fst' : Strips({'BHS':True, 'TNS':True, 'THS':False},{'BHS':False, 'TNS':False, 'THS':True, 'SND':True}),
                            # Pick up door - builder doesn't have the door but the shed needs it.
                            # Afterwards the builder has the door.
                            'pub' : Strips({'BHD':False, 'SND':True},{'BHD':True}),
                            # Fasten door to shed - the builder has the door and the shed needs it.
                            # Afterwards the builder no longer has door, the shed doesn't need it because it has it, now the shed needs a paint.
                            'fds' : Strips({'BHD':True, 'SND':True, 'SHD':False},{'BHD':False, 'SND':False, 'SHD':True, 'SNP':True}),
                            # Time for a paint! - builder doesn't have paint but shed needs it.
                            # Afterwards the builder has the paint.
                            'pup' : Strips({'BHP':False, 'SNP':True},{'BHP':True}),
                            # Apply paint to shed - the builder has the paint and the shed needs it.
                            # Afterwards the shed has been painted, the builder no longer needs paint neither does 
                            # the shed because it is already painted. The shed is complete!!
                            'aps' : Strips({'BHP':False, 'SNP':True, 'SHP':False},{'BHP':True, 'SNP':False, 'SIC': True, 'SHP':True})                
                            })

class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal):
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal

problem0 = Planning_problem(sandwich_domain, 
                            # Initial state - David at bench with no bread, cheese or knife and wanting a sandwich.
                            {'DLoc': 'ben', 'DHB':False, 'DHC':False, 'DHK':False, 'DWS':True, 'DNB':True,
                            'DNC':True, 'DNK':True, 'BOB':False, 'CBN':False, 'COB':False, 'CNS':True},
                            # The goal is to not want a sandwhich (because i've had one)
                            {'DWS':False})

problem1 = Planning_problem(shed_domain,
                            # Initial state - Builder does not have any of the items, shed needs all items.
                            {'BHF':False, 'BHC':False, 'BHT':False, 'BHS':False, 'BHD':False, 'BHP':False,
                            'SHF':False, 'FHC':False, 'FHT':False, 'THS':False, 'SHD':False, 'SHP':False, 
                            'SNF':True, 'FNC':False, 'FNT':False, 'TNS':False, 'SND':False, 'SNP':False,
                            'SIC':False},
                            # Goal is for shed to be complete
                            {'SIC':True})
