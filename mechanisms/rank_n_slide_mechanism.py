"""rank_n_slide.py

Implements a weighted calculation method, where 
each voter has a score (based on their achievments) and assigns a proportion of that score to candidates.
"""

from typing import Any, Dict, Callable
from mechanisms.voting_mechanism import VotingMechanism



#Set default amounts for each NFT to contribute to individual 
DEFAULT_NFT_SCORES = {
    "FUND_MOD1": 3.0,
    "FUND_MOD2": 3.0,
    "FUND_MOD3": 3.0,
    "FUND_MOD4": 3.0,
    "FUND_MOD5": 3.0,
    "BARCAMP_PARIS_23": 2.0,
    "NFTREP_V1": 1.0,
    "STUDY_GROUP_HOST_C2_22_23": 1.0,
    "STUDY_GROUP_HOST_360_22": 1.0,
    "STUDY_GROUP_HOST_FUND_22_23": 1.0,
    "LIVE_TRACK_1": 1.0,
    "LIVE_TRACK_2": 1.0,
    "LIVE_TRACK_3": 1.0,
    "LIVE_TRACK_4": 1.0,
    "LIVE_TRACK_5": 3.0,
    "LIVE_TRACK_6": 3.0,
    "LIVE_TRACK_7": 3.0,
    "LIVE_TRACK_8": 3.0
}

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

    def __init__(self):
        super().__init__()
        self.weighing_mechanism = self.get_default_weighing_mechanism

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
                    candidate_scores[candidate] += proportion * self.calculate_score(voters.get(voter_id))
                else:
                    candidate_scores[candidate] = proportion * self.calculate_score(voters.get(voter_id))

        # Sort candidates by their score, and return the winner (along with the detailed scores)
        sorted_candidates = dict(sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True))
        winner = max(candidate_scores, key=candidate_scores.get)

        return winner, candidate_scores

    def normalize_proportions(self, choice: Dict[str, float]):
        # So that if a vote is passed in that doesn't add up to 1 the numbers get adjusted.
        # E.g. 0.1 & 3 & 0.4 & 5 -> 0.1/8.5 ~ 0.011 & 3/8.5 = 0.035 & 0.4/8.5 = 0.047 & 5/8.5 = 0.59
        total = sum(choice.values())
        for candidate, proportion in choice.items():
            choice[candidate] = proportion / total
        return choice

    def get_default_weighing_mechanism(self, 
                                       voter: Dict[str, int],
                                       credential_info: Dict = DEFAULT_NFT_SCORES):
        score = 0
        for nft, amount in voter.items():
            if amount > 0:
                # Take the score of the default NFT list, or 1 if it's not defined.
                # If a user holds multiple (attended a session multiple times?), then add them up
                score += amount * credential_info.get(nft, 0)
        return score
        

    def set_weighing_mechanism(self, weighing_mechanism: Callable[[Dict[str, int]], int]):
        # This is here just for the convenience of being able to test different weighings for NFTs
        self.weighing_mechanism = weighing_mechanism

    def calculate_score(self, voter):
        return self.weighing_mechanism(voter)

