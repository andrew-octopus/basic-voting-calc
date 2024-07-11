class SimpleCredentialWeightingMechanism:
    """
    This is a simple mechanism that weights individual voters according to their credentials.
    It needs: 
    - the possible credentials (list)
    - the weights for each credential (dictionary)
    """

    def __init__(self,
                 credentials: List[str],
                 credential_weights: Dict[str, float]):
        self.credentials = credentials
        self.credential_weights = credential_weights

    def calc_cred_list_weight(self,
                              credential_list: List[str]) -> float:
        weight = sum([cred * self.credential_weights.get(cred) for cred in credential_list])
        return weight
         

    def calculate_voter_weights(self, 
                                voters: Dict[str, List[str]]) -> Dict[str, float]:
        voter_weights_dict = {} # Create new dictionary to hold voter weights

        for voter, voter_cred_list in voters.items(): # Going over each voter
            voter_weight = self.calc_cred_list_weight(voter_cred_list)
            voter_weights_dict[voter] = voter_weight

        return voter_weights_dict

