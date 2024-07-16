class SimpleCredentialWeightingMechanism:
    """
    This is a simple mechanism that weights individual voters according to their credentials.
    It needs: 
    - the possible credentials (list)
    - the weights for each credential (dictionary)
    """
    
    import pandas as pd
    from copy import deepcopy
    from typing import Dict, List

    def __init__(self,
                 credentials: List[str] = None,
                 credential_weights: Dict[str, float] = None):
        self.credentials = credentials
        self.credential_weights = credential_weights

    def calc_total_cred_weights(self,
                              cred_list: List[str],
                              cred_weights_list: Dict[str, float] = None) -> float:
        """
        Calculates the total weight of a list of credentials based on their weights.
        
        This method takes a list of credentials and calculates the total weight by summing up the weights of each credential.
        If a credential is not found in the credential_weights dictionary, its weight is considered 0.
        
        Parameters:
        credential_list (List[str]): A list of credentials to calculate the total weight for.
        
        Returns:
        float: The total weight of the credential list.
        """

        # Determine if custom credential weights were provided
        if cred_weights_list is None:
            cred_weights_to_use = deepcopy(cred_weights_list)
        else:
            cred_weights_to_use = deepcopy(self.credential_weights)

        # Initialize weight to 0
        weight = 0
        
        # Iterate over each credential in the credential list
        for cred in cred_weights_to_use:
            # Add the weight of the current credential to the total weight
            # If the credential is not found in credential_weights, get() returns 0 by default
            weight += cred_weights_to_use.get(cred, 0)
        
        return weight
         

    def calc_voter_weights(self, 
                           voters: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Calculates the weight of each voter based on their credentials.
        
        This method takes a dictionary of voters and their credentials and calculates the weight of each voter.
        The weight of a voter is calculated by summing up the weights of their credentials.
        If a credential is not found in the credential_weights dictionary, its weight is considered 0.
        
        Parameters:
        voters (Dict[str, List[str]]): A dictionary of voters and their credentials.
        
        Returns:
        Dict[str, float]: A dictionary of voters and their weights.
        """
        voter_weights_dict = {} # Create new dictionary to hold voter weights

        for voter, voter_cred_list in voters.items(): # Going over each voter
            voter_weight = self.calc_cred_list_weight(voter_cred_list) # Get total weight of voter's credentials
            voter_weights_dict[voter] = {"weight": voter_weight} # Set that voter weight

        return voter_weights_dict

        
    



