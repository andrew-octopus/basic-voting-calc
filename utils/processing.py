from math import isclose
import pandas as pd

from copy import deepcopy
from typing import Dict, List

def remove_blocklist_addresses(df: pd.DataFrame, blocklist:List) -> pd.DataFrame:
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()
    # Drop rows from the DataFrame based on the indices specified in the blocklist
    # Conditional drop based on whether the addresses are in the list
    df_copy = df_copy[~df_copy.index.isin(blocklist)]
    # Return the modified DataFrame with the specified rows removed
    return df_copy


def validate_dataframe_june_19(df: pd.DataFrame) -> bool:
    # Make a copy of the dataframe to avoid modifying the original dataframe
    df_copy = df.copy()

    # Count the total number of missing values in the dataframe
    missing_values_count = df_copy.isnull().sum().sum()
    assert missing_values_count == 0, f"Missing values count is not zero: {missing_values_count}"

    # Define the expected total NFT supply for June 19
    JUNE_19_TOTAL_NFT_SUPPLY = 1537
    # Calculate the total NFT supply from the dataframe
    total_nft_supply = df_copy.sum().sum()
    assert total_nft_supply == JUNE_19_TOTAL_NFT_SUPPLY, "The total NFT supply is not as expected: {total_nft_supply}"

    # Define the expected total number of token IDs
    TOTAL_TOKEN_IDS = 45
    # Calculate the total number of token IDs from the dataframe
    total_token_ids = len(df_copy.columns)
    assert total_token_ids == TOTAL_TOKEN_IDS, "The total number of token IDs is not as expected: {total_token_ids}"

    # Define the expected number of token IDs with supply greater than 0
    TOKEN_IDS_WITH_SUPPLY = 37
    # Calculate the number of token IDs with supply greater than 0 from the dataframe
    token_ids_with_supply = df_copy.any(axis=0).sum()
    assert token_ids_with_supply == TOKEN_IDS_WITH_SUPPLY, "The number of token IDs with supply > 0 is not as expected."

    # Check specific token IDs for a supply of zero
    assert df_copy['tokenId 12'].sum() == 0, "Token ID 12 should have a supply of zero."
    assert df_copy['tokenId 24'].sum() == 0, "Token ID 24 should have a supply of zero."
    assert df_copy['tokenId 31'].sum() == 0, "Token ID 31 should have a supply of zero."
    assert df_copy['tokenId 37'].sum() == 0, "Token ID 31 should have a supply of zero."
    assert df_copy['tokenId 41'].sum() == 0, "Token ID 41 should have a supply of zero."
    # Check a range of token IDs for a supply of zero
    assert df_copy[['tokenId 43', 'tokenId 44', 'tokenId 45']].sum().sum() == 0, "Token IDs 43-45 should have a supply of zero."

    assert df_copy.index.is_unique, "There are duplicated wallet addresses."

     # Check if every entry in the dataframe is either 0 or 1
    for column in df_copy.columns:
        invalid_values_count = (~df_copy[column].isin([0, 1])).sum()
        if invalid_values_count > 0:
            print(f"Column {column} contains {invalid_values_count} values other than 0 or 1.");
            print(f"Setting these values to be in {0,1}")
            df_copy[column] = df_copy[column].apply(lambda x: 1 if x > 1 else 0 if x < 0 else x)

    return df_copy


def preprocess_data(df: pd.DataFrame):
    
    # Merge and clean up token ID columns. 
    # For each pair of token IDs (e.g., 'token Id 1' and 'token Id 2'), 
    # it selects the maximum value between the two and assigns it to the first token ID column. 
    # The second token ID column is then set to 0. This process is repeated for multiple pairs of token IDs.

    modified_df = df.copy()
    
    modified_df['tokenId 1'] = modified_df[['tokenId 1', 'tokenId 2']].max(axis=1)
    modified_df['tokenId 2'] = 0

    modified_df['tokenId 3'] = modified_df[['tokenId 3', 'tokenId 4']].max(axis=1)
    modified_df['tokenId 4'] = 0

    modified_df['tokenId 5'] = modified_df[['tokenId 5', 'tokenId 6']].max(axis=1)
    modified_df['tokenId 6'] = 0

    modified_df['tokenId 7'] = modified_df[['tokenId 7', 'tokenId 8']].max(axis=1)
    modified_df['tokenId 8'] = 0

    modified_df['tokenId 9'] = modified_df[['tokenId 9', 'tokenId 10']].max(axis=1)
    modified_df['tokenId 10'] = 0

    modified_df['tokenId 20'] = modified_df[['tokenId 20', 'tokenId 21']].max(axis=1)
    modified_df['tokenId 21'] = 0

    return modified_df

def add_tef_graduate_column(df: pd.DataFrame):
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()

    # Check that the sum of all correspondnig evenID entries is zero. 
    assert df_copy['tokenId 2'].sum() == 0, "There should be no tokenId 2 in this DataFrame. "
    assert df_copy['tokenId 4'].sum() == 0, "There should be no tokenId 4 in this DataFrame. "
    assert df_copy['tokenId 6'].sum() == 0, "There should be no tokenId 6 in this DataFrame. "
    assert df_copy['tokenId 8'].sum() == 0, "There should be no tokenId 8 in this DataFrame. "
    assert df_copy['tokenId 10'].sum() == 0, "There should be no tokenId 10 in this DataFrame. "

    # Extract columns representing completion of each TEF module
    has_tef_module_1 = df_copy['tokenId 1']
    has_tef_module_2 = df_copy['tokenId 3']
    has_tef_module_3 = df_copy['tokenId 5']
    has_tef_module_4 = df_copy['tokenId 7']
    has_tef_module_5 = df_copy['tokenId 9']
    
    # Create a new column 'tef_graduate' that is True if all TEF modules are completed
    df_copy['tef_graduate'] = df_copy[['tokenId 1', 
                                       'tokenId 3', 
                                       'tokenId 5',
                                        'tokenId 7',
                                        'tokenId 9']].all(axis = 1)
    
    # Return the modified DataFrame with the new 'tef_graduate' column
    return df_copy 

def calculate_nft_weighted_sum(df: pd.DataFrame,
                               weights: Dict):
    # Initialize the sum to zero
    total_sum = 0
    
    # Iterate over each column in the DataFrame
    for column in df.columns:
        # Multiply each entry in the column by the corresponding weight and add to the total sum
        weighted_column_sum = (df[column] * weights[column]).sum()
        total_sum += weighted_column_sum
    
    # Return the total sum
    return total_sum


def create_dict_for_equal_cweights(df: pd.DataFrame,
                            original_weights_dict: dict,
                            expert_tokenIds_list: List,
                            graduate_tokenIds_list: List):
    
    ###########################################
    ## Calculate the original total weight.  ##
    ###########################################

    original_total_cweight = calculate_nft_weighted_sum(df = df,
                                                        weights = original_weights_dict)
    print(f"The original total cweight is: {original_total_cweight}.")
    
    ###############################################
    ## Calculate the original expert c_weight.   ##
    ###############################################

    expert_only_df = df[expert_tokenIds_list]
    original_expert_cweight = calculate_nft_weighted_sum(df = expert_only_df, 
                               weights = original_weights_dict)
    print(f"The original expert cweight is: {original_expert_cweight}.")
    

    #################################################
    ## Calculate the original graduate c_weight.   ##
    #################################################
    # Create a DataFrame to include only rows where 'tef_graduate' is True
    tef_graduates = df[df['tef_graduate'] == True]

    # Restrict from graduates to only the TEF Modules
    tef_graduates_tef_modules = tef_graduates[graduate_tokenIds_list]

    original_graduate_cweight = calculate_nft_weighted_sum(df = tef_graduates_tef_modules,
                                                           weights = original_weights_dict)
    print(f"The original graduate cweight is: {original_graduate_cweight}.")

   ###################################################################
   ## Do a reality check, that the graduate_cweight makes sense.    ##
   ## It should be equal to the product of the weight from passing  ##
   ## all five NFTs, times the number of TEF graduates who have     ##
   ## passed all five.                                              ##
   ###################################################################

    # Find total combined cweight of graduate status (passing all TEF modules)
    total_tef_tokenIds_weight = sum([original_weights_dict.get(tokenId) 
                                     for tokenId
                                     in graduate_tokenIds_list])
    print(f"The total TEF tokenIDs weight (for passing all five TEF modules): is {total_tef_tokenIds_weight}.")
    
    # Count the number of unique identities/wallets that match the TE Graduates criteria
    number_tef_graduates= df['tef_graduate'].sum()
    print(f"There are {number_tef_graduates} TEF graduates.")

    assert len(tef_graduates == number_tef_graduates), print("The number of TEF graduates here has an issue. ")
    # Reality check that the weights match up
    assert original_graduate_cweight == (number_tef_graduates * total_tef_tokenIds_weight), "Unexpected result with TEF graduates weight. "

    ####################################################################
    ## The remaining amount of weight must be the student cweight.    ##
    ####################################################################

    original_student_cweight = original_total_cweight - (original_expert_cweight + original_graduate_cweight)
    print(f"The original student cweight is: {original_student_cweight}.")

    ####################################################################
    ## Create a copy of the weights dictionary, to change specific    ##
    ## entries.                                                       ##
    ####################################################################

    modified_weights_dict = deepcopy(original_weights_dict)

    ####################################################################
    ## If tef_student_boost is greater than tef_graduate_boost,       ##
    ## we solve for the amount of `tef_graduate_boost` that would be  ##
    ## needed to make the scaled_graduate_weight equal to the         ##
    ## scaled_student_weight.                                         ##
    ####################################################################

    if original_student_cweight > original_graduate_cweight:
        print("Original student cweight is greater than original graduate cweight.")
        print("Scaling graduate cweight.")

        tef_graduate_boost = original_student_cweight/number_tef_graduates - total_tef_tokenIds_weight
        scaled_graduate_cweight = (total_tef_tokenIds_weight + tef_graduate_boost) * number_tef_graduates
        scaled_student_cweight = original_student_cweight
        assert isclose(scaled_graduate_cweight - scaled_student_cweight, 0)

        print(f"The TEF graduate boost to make the two cweights equal is: {tef_graduate_boost}.")
        print(f"After calculation, final student cweight should be: {scaled_student_cweight}.")
        print(f"After calculation, final graduate cweight should be: {scaled_graduate_cweight}.")

        modified_weights_dict['tef_graduate'] = tef_graduate_boost

    else:
        print("Original graduate cweight already greater than original student cweight.")
        scaled_graduate_cweight = original_graduate_cweight
        scaled_student_cweight = original_student_cweight
        modified_weights_dict['tef_graduate'] = 0

    
    if scaled_graduate_cweight > original_expert_cweight:
        grad_expert_weight_ratio = scaled_graduate_cweight/original_expert_cweight
        for tokenId in expert_tokenIds_list:
            original_tokenId_weight = original_weights_dict.get(tokenId)
            modified_tokenId_weight = grad_expert_weight_ratio * original_tokenId_weight
            modified_weights_dict[tokenId] = modified_tokenId_weight

        scaled_expert_cweight = calculate_nft_weighted_sum(df = expert_only_df,
                                                          weights = modified_weights_dict)

        assert isclose(scaled_expert_cweight - scaled_graduate_cweight, 0)

    else:
        print("Original expert cweight already greater than original graduate cweight.")
        scaled_expert_cweight = original_expert_cweight

    ##########################################################
    ## We need to get a new DataFrame for TEF graduates     ##
    ## that incorporates the `tef_graduate` column.         ##
    ##########################################################
    
    if not('tef_graduate') in graduate_tokenIds_list:
        new_graduate_tokenIds_list = graduate_tokenIds_list + ['tef_graduate']
    else:
        new_graduate_tokenIds_list = deepcopy(graduate_tokenIds_list)

    new_tef_graduate_df = tef_graduates[new_graduate_tokenIds_list] 
    print("The columns of this new TEF graduate df are: \n")
    for col in new_tef_graduate_df:
        print(col)

    print(f"There are {len(new_tef_graduate_df)} graduates in this DataFrame.")
    print(f"The weight of TEF graduate is: {modified_weights_dict.get('tef_graduate')}")

    print("\n Final Check: \n")

    actual_final_total_cweight = calculate_nft_weighted_sum(df = df, 
                               weights = modified_weights_dict)
    actual_final_expert_cweight = calculate_nft_weighted_sum(df = expert_only_df, 
                               weights = modified_weights_dict)
    actual_final_graduate_cweight = calculate_nft_weighted_sum(df = new_tef_graduate_df,
                                     weights = modified_weights_dict)
    actual_final_student_cweight = actual_final_total_cweight - (actual_final_expert_cweight + actual_final_graduate_cweight)


    print(f"Actual final total cweight is {actual_final_total_cweight}.")
    print(f"Actual final expert cweight is {actual_final_expert_cweight}.")
    print(f"Actual final graduate cweight is {actual_final_graduate_cweight}.")
    print(f"Actual final student cweight is: {actual_final_student_cweight}.")

    assert isclose(actual_final_expert_cweight - actual_final_graduate_cweight, 0, abs_tol=1e-5), "Final expert cweight and graduate cweight are not close enough."
    assert isclose(actual_final_graduate_cweight - actual_final_student_cweight, 0, abs_tol=1e-5), "Final graduate cweight and final student cweight are not close enough."

    return modified_weights_dict

    













