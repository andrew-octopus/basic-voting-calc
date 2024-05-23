import numpy as np
from typing import Dict

def calc_voter_weights_from_NFT_weight(voters_dict: Dict[str, dict], 
                                      weights_dict: Dict[str, float]):
    """
    Calculate the weights for each voter based on their NFTs and corresponding weights.
    
    Parameters:
    - voters_dict (dict): A dictionary containing voters with NFTs.
    - weights_dict (dict): A dictionary containing weights for each NFT.
    
    Returns:
    - dict: A dictionary of weights for each voter.
    """


    first_voter = voters_dict.get(list(voters_dict.keys())[0])

    # Check if keys are in the same order
    if list(first_voter.keys()) != list(weights_dict.keys()):
        raise ValueError("Keys in voters_dict and weights_dict are not in the same order")

    new_dict = {}
    weights_values = np.array(list(weights_dict.values()))
    for voter in list(voters_dict.keys()):
        voter_values = np.array(list(voters_dict.get(voter).values()))
        dot_product_values = np.dot(weights_values, voter_values)
        new_dict[voter] = {"weight": dot_product_values}

    return new_dict