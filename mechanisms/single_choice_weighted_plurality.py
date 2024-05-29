"""single_choice_weighted_plurality.py

Implements a basic weighted plurality calculation method, where 
each voter has a weight and the total plurality calculation is used. 
"""

from typing import Any, Dict
from mechanisms.voting_mechanism import VotingMechanism

class SingleChoiceWeightedPlurality(VotingMechanism):
    """
    A voting system class that implements a single-choice weighted plurality voting mechanism.
    In this system, each voter assigns their vote to a single candidate, and the votes are weighted
    according to predefined weights for each voter. The candidate with the highest total weighted
    votes is declared the winner.

    Attributes:
        voters (Dict[str, Dict[str, Any]]): A dictionary where each key is a voter ID and the value
            is another dictionary containing voter-specific attributes such as "weight".
        voter_choices (Dict[str, str]): A dictionary where each key is a voter ID and the value is
            the candidate chosen by that voter.
    """
    def calculate(self, voters: Dict[str, Dict[str, Any]], 
                  voter_choices: Dict[str, str]):
        """
        Implements a simple weighted plurality voting system.

        Parameters:
        - voters: A dictionary where each key is a voter ID and the value is a dictionary with "weight" as the only key. 
        - voter_choices: A dictionary where each key is a voter ID and the value is the candidate chosen by the voter.

        Returns:
        - str: The candidate with the highest total weighted votes.
        """
        # Initialize a dictionary to keep track of the total weighted votes for each candidate
        candidate_scores = {}

        # Calculate the weighted vote for each candidate based on voter choices and voter weights
        for voter_id, choice in voter_choices.items():
            if choice in candidate_scores:
                candidate_scores[choice] += voters.get(voter_id).get("weight", 0)
            else:
                candidate_scores[choice] = voters.get(voter_id).get("weight", 0)

        # Determine the candidate with the highest score
        winner = max(candidate_scores, key=candidate_scores.get)

        return winner, candidate_scores

