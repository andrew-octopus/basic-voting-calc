"""GroupHug.py

Implements a group based calculation method, where each stakeholder group has 
a weight and rules by which points are distributed. 
"""
from typing import Any, Dict, List

from custom_types import Voter
from mechanisms.voting_mechanism import VotingMechanism

#Set default amounts for each NFT to contribute to individual 
DEFAULT_NFT_WEIGHTS = {
    "FUND_MOD_1": 3.0,
    "FUND_MOD_2": 3.0,
    "FUND_MOD_3": 3.0,
    "FUND_MOD_4": 3.0,
    "FUND_MOD_5": 3.0,
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


# Set the default weights for each group. 
DEFAULT_EXPERTS_GROUP_WEIGHT = 1
DEFAULT_INTELLECTUALS_GROUP_WEIGHT = 1
DEFAULT_PARTICIPANTS_GROUP_WEIGHT = 1
DEFAULT_COMMUNITY_GROUP_WEIGHT = 1


DEFAULT_EXPERTS_NFT_LIST = ["FELLOWSHIP_COMM", 
                        "FUND_AUTHOR",
                        "STUDY_SEASON_SPEAKER", 
                        "SPEAKER_ETHCC_PARIS23", 
#TODO:double-check      NFT.ETHCC_SPEAKER_2,
                        "SPEAKER_BARCAMP_PARIS_23"]

DEFAULT_INTELLECTUALS_NFT_LIST = ["FUND_MOD_1",
                                 "FUND_MOD_2",
                                 "FUND_MOD_3",
                                 "FUND_MOD_4",
                                 "FUND_MOD_5",
                                 "BARCAMP_PARIS_23"
                                 "NFTREP_V1"
                                  ]


DEFAULT_PARTICIPANTS_NFT_LIST = [
                                "STUDY_GROUP_HOST_C2_22_23",
                                "STUDY_GROUP_HOST_360_22",
                                "STUDY_GROUP_HOST_FUND_22_23",
                                "ETHCC_23",
                                "LIVE_TRACK_1",
                                 "LIVE_TRACK_2",
                                 "LIVE_TRACK_3",
                                 "LIVE_TRACK_4",
                                 "LIVE_TRACK_5",
                                 "LIVE_TRACK_6",
                                 "LIVE_TRACK_7",
                                 "LIVE_TRACK_8"
                                ]

DEFAULT_COMMUNITY_NFT_LIST = [ ]

class GroupHug(VotingMechanism):
    """
    A voting system class that implements a stakeholder group based voting mechanism.

    Attributes:
        voters (Dict[str, Dict[str, Any]]): A dictionary where each key is a voter ID and the value
            is a dictionary of (NFT ID, boolean) pairs.
        voter_choices (Dict[str, str]): A dictionary where each key is a voter ID and the value is
            the candidate chosen by that voter.
    """

    def __init__(self, 
                 nft_weights: Dict[str, float] = DEFAULT_NFT_WEIGHTS,
                 experts_group_weight: float = DEFAULT_EXPERTS_GROUP_WEIGHT,
                 intellectuals_group_weight: float = DEFAULT_INTELLECTUALS_GROUP_WEIGHT,
                 participants_group_weight: float = DEFAULT_PARTICIPANTS_GROUP_WEIGHT,
                 community_group_weight: float = DEFAULT_COMMUNITY_GROUP_WEIGHT,
                 experts_nft_list: List[str] = DEFAULT_EXPERTS_NFT_LIST,
                 intellectuals_nft_list: List[str] = DEFAULT_INTELLECTUALS_NFT_LIST,
                 participants_nft_list: List[str] = DEFAULT_PARTICIPANTS_NFT_LIST,
                 community_nft_list: List[str] = DEFAULT_COMMUNITY_NFT_LIST):

        # Set the default NFT weights for each NFT
        self.nft_weights = nft_weights

        # Set the group weights to constructor inputs, or default values if not set 
        self.experts_group_weight = experts_group_weight
        self.intellectuals_group_weight = intellectuals_group_weight
        self.participants_group_weight = participants_group_weight
        self.community_group_weight = community_group_weight

        # Set the qualifications required to belong to each group
        self.experts_nft_list = experts_nft_list
        self.intellectuals_nft_list = intellectuals_nft_list 
        self.participants_nft_list = participants_nft_list 
        self.community_nft_list = community_nft_list 

    def calculate(self, voters: Dict[str, Dict[str, Any]], 
                  voter_choices: Dict[str, str]):
        """
        Implements the group hug voting mechanism.

        Parameters:
        - voters: A dictionary where each key is a voter ID and the value is a dictionary 
            of (NFT, boolean) pairs to signify if the voter holds this NFT. 
        - voter_choices: A dictionary where each key is a voter ID and the value is the chosen candidate.

        Returns:
        - str: The winning candidate.
        - dict: The result of each candidate.

        Basic Idea of GroupHug:
        Step 0. Based on NFT criteria, voters are given multiple labels corresponding to different groups.
        Step 1. For each group, the criteria are scored corresponding to a mechanism.
        Step 2. The group results are combined, according to weight for each group.
        Step 3. The winner is determined by combining group results. 
        """

        # Extract and convert input to internal format
        extracted_candidates = set(voter_choices.values())
        extracted_voters = []
        for v in voters:
            choice = voter_choices[v]
            nfts = [nft for nft in voters[v] if voters[v][nft]]
            extracted_voters.append(Voter(choice, nfts))
        
        # Analyze election results
        (aggregate_vote, e, i, p, c) = self.vote(extracted_candidates, extracted_voters, verbose = True)
        winner = self.declare_winner(aggregate_vote, e, c)

        return (winner, aggregate_vote)

    
    ##################################
    ## Begin expert section.        ##
    ##################################

    def is_expert(self, voter):
        for nft in voter.nfts:
            if nft in self.experts_nft_list:
                return True

    # The experts are highly qualified peers.
    # They are fellowship committee members, TE Fundamentals course authors, 
    # or TE Study Season / ETHCC / Barcamp speakers.
    # They follow a principle of one person, one vote.

    def ask_the_experts(self, candidates, voters):

        experts = set([voter for voter in voters if self.is_expert(voter)])
                    
        return self.ask_the_community(candidates, experts)

    ##################################
    ## End expert section.          ##
    ##################################

    ####################################
    ## Begin intellectual section.    ##
    ####################################

    def weight_intellectual(self, voter):
            w = 0             
            for nft in voter.nfts:
                if nft in self.intellectuals_nft_list:
                    w += self.nft_weights[nft]

            return w

    # The intellectuals are students who hold one or more NFTs as proof-of-knowledge,
    # either from TE Fundamentals, the NFT-based reputation course, or Barcamp.
    # The weights for each NFT are set in the `nft_weights` dictionary. 

    def ask_the_intellectuals(self, candidates, voters):
        
        cpoints = {c: 0 for c in candidates}

        for voter in voters:
            cpoints[voter.vote] += self.weight_intellectual(voter)

        return cpoints

    ####################################
    ## End intellectual section.      ##
    ####################################

    
    ###########################################
    ## Begin active participants section.    ##
    ###########################################

    def weight_active_participant(self, voter):

        w = 0
        for nft in voter.nfts:
            if nft in self.participants_nft_list:
                w += self.nft_weights.get(nft, 0)

        return w

    
    def ask_the_active_participants(self, candidates, voters):

        cpoints = {c: 0 for c in candidates}

        for voter in voters:
            cpoints[voter.vote] += self.weight_active_participant(voter)

        return cpoints

    ###########################################
    ## End active participants section.     ##
    ###########################################

   ###########################################
   ## Begin community  section.             ##
   ###########################################

    # The community is a large and very diverse group of people.
    # All voters are treated equally: One person > one vote. No weights are applied.
    # NOTE: This is also called for other groups, after they have been weighted. 
    def ask_the_community(self, candidates, voters):

        votecount = {}
        for c in candidates:
            votecount[c] = len([voter for voter in voters if voter.vote == c])
        
        return votecount
    
   ###########################################
   ## End community  section.               ##
   ###########################################

   ############################################
   ## Begin vote-counting mechanics session. ##
   ############################################

    #  Helper function to convert a set of points into percentages to allow aggregation across several sets of points.
    def normalize(self, points):

        total = sum(points.values())

        if total == 0: return {c: 0 for c in points}
        else: return {c: round(100 * points[c] / total, 1) for c in points}
    
    # Helper function to convert a dicitionary to a more readable form. 
    def str_dict(self, d):
        return str(dict(sorted(d.items())))


    # Main vote-counting mechanics
    def vote(self, candidates, voters, verbose = False):
        eligible = [v for v in voters if not v.isCandidate]   # Candidates are not allowed to vote!

        experts = self.normalize(self.ask_the_experts(candidates, eligible))
        intellectuals = self.normalize(self.ask_the_intellectuals(candidates, eligible))
        participants = self.normalize(self.ask_the_active_participants(candidates, eligible))
        community = self.normalize(self.ask_the_community(candidates, eligible))
        
        if verbose:
            print("\nExperts: " + self.str_dict(experts))
            print("Intellectuals: " + self.str_dict(intellectuals))
            print("Participants: " + self.str_dict(participants))
            print("Community: " + self.str_dict(community))

        aggregate = {c: 0 for c in candidates}

        for c in experts:
            aggregate[c] += (experts[c]*self.experts_group_weight)

        for c in intellectuals:
            aggregate[c] += (intellectuals[c]*self.intellectuals_group_weight)

        for c in participants:
            aggregate[c] += (participants[c]*self.participants_group_weight)

        for c in community:
            aggregate[c] += (community[c]*self.community_group_weight)

        result = self.normalize(aggregate)

        return (result, experts, intellectuals, participants, community)


    def declare_winner(self, aggregate_vote, experts_vote, community_vote):

        m = max(aggregate_vote.values())
        winners = [k for k in aggregate_vote if aggregate_vote[k] == m]

        if len(winners) == 1:       # There is a unique winner
            return winners[0]
        
        print("Tie. We'll ask the experts to resolve it.")
        e_filtered = {k: v for k,v in experts_vote.items() if k in winners}
        m_e = max(e_filtered.values())
        winners_e = [k for k in e_filtered if e_filtered[k] == m_e]

        if len(winners_e) == 1:     # The experts prefer one winner over the other(s)
            return winners_e[0]

        print("Experts could not resolve tie. We'll ask the community.")
        c_filtered = {k: v for k,v in community_vote.items() if k in winners}
        m_c = max(c_filtered.values())
        winners_c = [k for k in c_filtered if c_filtered[k] == m_c]

        if len(winners_c) == 1:     # The community prefers one winner over the other(s)
            return winners_c[0]
        
        raise Exception("A unique winner could not be found!")

   ############################################
   ## End vote-counting mechanics session.   ##
   ############################################

