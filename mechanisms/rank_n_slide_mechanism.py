"""rank_n_slide.py

Implements a weighted calculation method, where 
each voter has a score (based on their achievments) and assigns a proportion of that score to candidates.
"""

from typing import Any, Callable, Dict, Literal
from mechanisms.voting_mechanism import VotingMechanism

# Deprecated: original default values
# DEFAULT_NFT_SCORES = {
#     "FUND_MOD1": 3.0,
#     "FUND_MOD2": 3.0,
#     "FUND_MOD3": 3.0,
#     "FUND_MOD4": 3.0,
#     "FUND_MOD5": 3.0,
#     "BARCAMP_PARIS_23": 2.0,
#     "NFTREP_V1": 1.0,
#     "STUDY_GROUP_HOST_C2_22_23": 1.0,
#     "STUDY_GROUP_HOST_360_22": 1.0,
#     "STUDY_GROUP_HOST_FUND_22_23": 1.0,
#     "LIVE_TRACK_1": 1.0,
#     "LIVE_TRACK_2": 1.0,
#     "LIVE_TRACK_3": 1.0,
#     "LIVE_TRACK_4": 1.0,
#     "LIVE_TRACK_5": 3.0,
#     "LIVE_TRACK_6": 3.0,
#     "LIVE_TRACK_7": 3.0,
#     "LIVE_TRACK_8": 3.0
# }

# Set default NFT values suggested by TEA 
DEFAULT_NFT_WEIGHTS = {'FUND_AUTHOR': 20.0,
 'SPEAKER_ETHCC_PARIS23': 16.0,
 'FUND_MOD_1': 7.0,
 'FUND_MOD_2': 7.0,
 'FUND_MOD_3': 7.0,
 'FUND_MOD_4': 7.0,
 'FUND_MOD_5': 7.0,
 'NFTREP_V1': 3.0,
 'ETHCC_23': 1.0,
 'SPEAKER_BARCAMP_PARIS_23': 12.0,
 'BARCAMP_PARIS_23': 5.0,
 'TEAM_BARCAMP_PARIS_23': 1.0,
 'STUDY_GROUP_HOST_FUND_22_23': 10.0,
 'STUDY_GROUP_HOST_C2_22_23': 10.0,
 'STUDY_GROUP_HOST_360_22': 10.0,
 'STUDY_SEASON_REGISTRATION': 1.0,
 'LIVE_TRACK_1': 10.0,
 'LIVE_TRACK_3': 10.0,
 'LIVE_TRACK_4': 10.0,
 'LIVE_TRACK_5': 10.0,
 'LIVE_TRACK_6': 10.0,
 'LIVE_TRACK_7': 10.0,
 'LIVE_TRACK_8': 10.0,
 'FELLOWSHIP_COMM': 16.0,
 'STUDY_SEASON_SPEAKER': 16.0,
 'FUND_WE_MADE_IT': 10.0,
 'FUND_MOD_3_AND_4': 5.0,
 'FUND_ALL': 10.0}

class RankAndSlide(VotingMechanism):
    """
    A voting system class that implements a score voting mechanism.
    In this system, each voter has a predefined score based on their achievments (NFTs).
    Each voter gives each candidate a proportion of their score. 
    The scores are added up for each candidate, the candidate with the highest total score is declared the winner.

    Attributes:
        voters (Dict[str, Dict[str, Any]]): A dictionary where each key is a voter ID and the value
            is another dictionary containing voter-specific attributes such as "weight".
        voter_choices (Dict[str, Dict[str, float]]): A dictionary where each key is a voter ID and the value is
            a dictionary of a candidate and a proportion of how much of the voter's score to assign to that candidate.
            The proportion can be any number, all proportions will be normalized to sum to 1.
    """

    def __init__(self, 
                 credential_info: Dict[str, float] = DEFAULT_NFT_WEIGHTS):
        super().__init__()
        # self.weighing_mechanism = self.get_default_weighing_mechanism(credential_info_to_use = DEFAULT_NFT_WEIGHTS)

    def calculate(self, voters: Dict[str, Dict[str, int]],
                  voter_choices: Dict[str, Dict[str, float]]):
        """
        Implements a score voting system.

        Parameters:
        - voters: A dictionary where each key is a voter ID 
            and the value is a dictionary with the name of an NFT and int for how many of these NFTs the voter has. Usually 0 or 1. 
        - voter_choices: A dictionary where each key is a voter ID and the value is a dictionary of 
            a candidate and a proportion of how much of the voter's score to assign to that candidate

        Returns:
        - SortedDict[str, float]: A sorted dictionary with the candidates along with their score, sorted by highest score.
        """
        # Initialize a dictionary to keep track of the total weighted votes for each candidate
        candidate_scores = {}

        for voter_id, choice in voter_choices.items():
            normalised_choice = self.normalize_proportions(choice)

            for candidate, proportion in normalised_choice.items():
                if candidate in candidate_scores:
                    candidate_scores[candidate] += proportion * voters.get(voter_id).get("points",0)
                else:
                    candidate_scores[candidate] = proportion *  voters.get(voter_id).get("points",0)
        
        # Sort candidates by their score, and return the winner (along with the detailed scores)
        sorted_candidates = dict(sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True))
        winner = max(candidate_scores, key=candidate_scores.get)

        return winner, candidate_scores
    
    def allocate_points_from_credentials(self,
                                        voter_credentials: Dict[str, Dict[str,
                                                Literal[0,1,None]]],
                        credential_weights: Dict[str, float]):
        """
        Takes a dictionary of voter credentials, with weights for each credential, 
        and applies the points available. 

        In the TEA Reputation-Weighted example, the credentials are NFTs.
        We set total_amount_to_allocate to 10_000 to avoid issues with small errors. 

        NOTE: All voter_credentials should have values. 
        """ 
        # Create a blank dictionary to keep information
        raw_voter_amounts = {}
        total_amount_all_voters = 0 

        # For each voter and their list of credentials
        for voter, individual_voter_credentials in voter_credentials.items():
            # Create an entry in the dictionary for their total weight
            raw_voter_amounts[voter] = {"points": 0}
            # Loop over their credentials and add the total amount 
            for credential in individual_voter_credentials.keys():
                    voter_has_credential = voter_credentials.get(voter).get(credential,0)
                    individual_credential_weight = credential_weights.get(credential, 0) 
                    weight_to_add_to_voter = voter_has_credential * individual_credential_weight
                    raw_voter_amounts[voter]["points"] += weight_to_add_to_voter

        return raw_voter_amounts


    def normalize_proportions(self, choice: Dict[str, float]):
        # So that if a vote is passed in that doesn't add up to 1 the numbers get adjusted.
        # E.g. 0.1 & 3 & 0.4 & 5 -> 0.1/8.5 ~ 0.011 & 3/8.5 = 0.035 & 0.4/8.5 = 0.047 & 5/8.5 = 0.59
        normalized_choices = {}
        total = sum(choice.values())
        for candidate, proportion in choice.items():
            normalized_choices[candidate] = proportion / total
        return normalized_choices
    
    def get_default_weighing_mechanism(self, 
                                       voter: Dict[str, int],
                                       credential_info_to_use = None):
        score = 0
        for nft, amount in voter.items():
            if amount > 0:
                # Take the score of the default NFT list, or 1 if it's not defined.
                # If a user holds multiple (attended a session multiple times?), then add them up
                score += amount * credential_info_to_use.get(nft, 0)
        return score
        

    def set_weighing_mechanism(self, weighing_mechanism: Callable[[Dict[str, int]], int]):
        # This is here just for the convenience of being able to test different weighings for NFTs
        self.weighing_mechanism = weighing_mechanism

    def calculate_score(self, voter):
        return self.weighing_mechanism(voter)
    
