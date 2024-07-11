class SimpleCredentialWeightingMechanism:
    """
    This is a simple mechanism that weights individual voters according to their credentials.
    It needs: 
    - the possible credentials (list)
    - the weights for each credential (dictionary)
    """
    
    import pandas as pd
    from typing import Dict, List

    def __init__(self,
                 credentials: List[str] = None,
                 credential_weights: Dict[str, float] = None):
        self.credentials = credentials
        self.credential_weights = credential_weights

    def calc_cred_list_weight(self,
                              credential_list: List[str]) -> float:
        """
        Calculates the total weight of a list of credentials based on their weights.
        
        This method takes a list of credentials and calculates the total weight by summing up the weights of each credential.
        If a credential is not found in the credential_weights dictionary, its weight is considered 0.
        
        Parameters:
        credential_list (List[str]): A list of credentials to calculate the total weight for.
        
        Returns:
        float: The total weight of the credential list.
        """
        
        # Initialize weight to 0
        weight = 0
        
        # Iterate over each credential in the credential list
        for cred in credential_list:
            # Add the weight of the current credential to the total weight
            # If the credential is not found in credential_weights, get() returns 0 by default
            weight += self.credential_weights.get(cred, 0)
        
        return weight
         

    def calculate_voter_weights(self, 
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
            voter_weight = self.calc_cred_list_weight(voter_cred_list)
            voter_weights_dict[voter] = {"weight": voter_weight}

        return voter_weights_dict

        
    



