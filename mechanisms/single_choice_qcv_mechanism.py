import math
import numpy as np

from typing import Literal 

"""single_choice_qcv.py

Implements single choice quadratic credibility voting. 
"""

from typing import Any, Dict
from mechanisms.voting_mechanism import VotingMechanism

class SingleChoiceQuadraticCredibility(VotingMechanism):
        def calculate(self,
                  voters: Dict[str, Dict[str, Any]],
                  voter_choices: Dict[str, Any]):
            """
            Implements a single winner Quadratic Credibility mechanism, as authored by @flocke and Jade. 

            Step 0. Elsewhere, voters have been assigned points. 
            STep 1. Voters allocate points to candidates.
            Step 2. For each candidate, we apply the standard quadratic voting approach, 
            i.e. square root each point amount given by a voter, then add all values, then square.
            Step 3. The maximum value for a candidate is the single winner. 

            Parameters:
            - voters: A dictionary with each a voter ID, and each value is another dictionary
                    containing details about the voter (such as which NFTs they hold).
            - voter_choices: A dictionary where each key is a voter ID and the value represents the
                            voter's choices or votes in the voting process.

            Returns:
                Result(s) of the voting calculation, of any type depending on the
                specific implementation (e.g., winner, ranked list of candidates, etc.).
            """

            # Extract all candidates from dictionary of voter preferences
            # There will be repeats at this stage
            all_candidates_with_multiples = []
            for voter, choices in voter_choices.items():
                potential_new_candidates = list(choices.keys())
                all_candidates_with_multiples += potential_new_candidates

            # Remove duplicate candidates
            candidates = list(set(all_candidates_with_multiples)) 

            # Create dictionary where all candidates have 0
            candidate_allocations = {candidate : 0 
                                    for candidate 
                                    in candidates}
            
            # See who voted for a candidate
            for candidate in candidates:
                 allocation = np.array([voter_choices.get(voter).get(candidate, 0)
                                for voter in voters])
                 qv_processed_candidate_allocation = np.square(np.sum(np.sqrt(allocation)))
                 candidate_allocations[candidate] = qv_processed_candidate_allocation

            # Determine winner
            # NOTE: Ties are broken by arbitrarily selecting first candidate. 
            winner  = max(candidate_allocations, key=candidate_allocations.get)

            return winner, candidate_allocations
        
        def allocate_points_from_credentials(self,
                                             voter_credentials: Dict[str, Dict[str,
                                                     Literal[0,1,None]]],
                                credential_weights: Dict[str, float],
                                total_amount_to_allocate: float = 10_000):
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
                raw_voter_amounts[voter] = 0
                # Loop over their credentials and add the total amount 
                for credential in individual_voter_credentials.keys():
                     voter_has_credential = voter_credentials.get(voter).get(credential,0)
                     individual_credential_weight = credential_weights.get(credential, 0) 
                     weight_to_add_to_voter = voter_has_credential * individual_credential_weight
                     raw_voter_amounts[voter] += weight_to_add_to_voter
                     total_amount_all_voters += weight_to_add_to_voter

            normalized_voter_amounts = {voter: raw_voter_amounts.get(voter)/total_amount_all_voters
                                        for voter in voter_credentials.keys()}
            final_voter_points = {voter: {"points" : total_amount_to_allocate * normalized_voter_amounts.get(voter)}
                                  for voter in voter_credentials.keys()}

            return final_voter_points

        
        



             
             
   

                 



                    

                  

            # 


