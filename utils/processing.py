from math import isclose
import pandas as pd

from copy import deepcopy
from typing import Dict, List

def remove_blocklist_addresses(df: pd.DataFrame, blocklist) -> pd.DataFrame:
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()
    # Drop rows from the DataFrame based on the indices specified in the blocklist
    df_copy.drop(index=blocklist, inplace=True)
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
    assert total_nft_supply == JUNE_19_TOTAL_NFT_SUPPLY, "The total NFT supply is not as expected."

    # Define the expected total number of token IDs
    TOTAL_TOKEN_IDS = 45
    # Calculate the total number of token IDs from the dataframe
    total_token_ids = len(df_copy.columns)
    assert total_token_ids == TOTAL_TOKEN_IDS, "The total number of token IDs is not as expected."

    # Define the expected number of token IDs with supply greater than 0
    TOKEN_IDS_WITH_SUPPLY = 37
    # Calculate the number of token IDs with supply greater than 0 from the dataframe
    token_ids_with_supply = len(df_copy[df_copy > 0].columns)
    assert token_ids_with_supply == TOKEN_IDS_WITH_SUPPLY, "The number of token IDs with supply > 0 is not as expected."

    # Check specific token IDs for a supply of zero
    assert df_copy.loc[12].sum() == 0, "Token ID 12 should have a supply of zero."
    assert df_copy.loc[24].sum() == 0, "Token ID 24 should have a supply of zero."
    assert df_copy.loc[31].sum() == 0, "Token ID 31 should have a supply of zero."
    assert df_copy.loc[41].sum() == 0, "Token ID 41 should have a supply of zero."
    # Check a range of token IDs for a supply of zero
    assert df_copy.loc[43:45].sum().sum() == 0, "Token IDs 43-45 should have a supply of zero."

        # Check for duplicate rows in the dataframe
    duplicate_rows = df_copy.duplicated()
    if duplicate_rows.any():
        print(f"Found {duplicate_rows.sum()} duplicate rows.")
        print(f"Dropping duplicate rows.")
        # Remove duplicate rows from the dataframe
        df_copy = df_copy[~duplicate_rows]

    # Remove duplicate rows from the dataframe to ensure data integrity
    df_copy.drop_duplicates(inplace=True)

    # Check if there are any duplicate rows left after dropping duplicates
    duplicate_count = df_copy.duplicated().sum()
    assert duplicate_count == 0, f"Duplicate count is not zero: {duplicate_count}"

     # Check if every entry in the dataframe is either 0 or 1
    for column in df_copy.columns:
        invalid_values_count = (~df_copy[column].isin([0, 1])).sum()
        if invalid_values_count > 0:
            print(f"Column {column} contains {invalid_values_count} values other than 0 or 1.");
            print(f"Setting these values to be in {0,1}")
            df_copy[column] = df_copy[column].apply(lambda x: 1 if x > 1 else 0 if x > 0 else x)


def preprocess_data(df: pd.DataFrame,
                    expert_tokenIds_list: list,
                    graduate_tokenIds_list: list):
    
    # Merge and clean up token ID columns. 
    # For each pair of token IDs (e.g., 'token Id 1' and 'token Id 2'), 
    # it selects the maximum value between the two and assigns it to the first token ID column. 
    # The second token ID column is then set to 0. This process is repeated for multiple pairs of token IDs.

    modified_df = df.copy()
    modified_df['token Id 1'] = modified_df[['token Id 1', 'token Id 2']].max(axis=1)
    modified_df['token Id 2'] = 0

    modified_df['token Id 5'] = modified_df[['token Id 5', 'token Id 6']].max(axis=1)
    modified_df['token Id 6'] = 0

    modified_df['token Id 7'] = modified_df[['token Id 7', 'token Id 8']].max(axis=1)
    modified_df['token Id 8'] = 0

    modified_df['token Id 9'] = modified_df[['token Id 9', 'token Id 10']].max(axis=1)
    modified_df['token Id 10'] = 0

    modified_df['token Id 20'] = modified_df[['token Id 20', 'token Id 21']].max(axis=1)
    modified_df['token Id 21'] = 0

    return modified_df

def add_tef_graduate_column(df: pd.DataFrame):
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()
    
    # Extract columns representing completion of each TEF module
    has_tef_module_1 = df_copy['tokenId 1']
    has_tef_module_2 = df_copy['tokenId 3']
    has_tef_module_3 = df_copy['tokenId 5']
    has_tef_module_4 = df_copy['tokenId 7']
    has_tef_module_5 = df_copy['tokenId 9']
    
    # Create a new column 'tef_graduate' that is True if all TEF modules are completed
    df_copy['tef_graduate'] = (has_tef_module_1 & has_tef_module_2 & has_tef_module_3 & has_tef_module_4 & has_tef_module_5)
    
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

    original_total_cweight = calculate_nft_weighted_sum(df = df,
                                                        weights = original_weights_dict)
    expert_only_df = df[expert_tokenIds_list]
    original_expert_cweight = calculate_nft_weighted_sum(df = expert_only_df, 
                               weights = original_weights_dict)

    # Create a DataFrame to include only rows where 'tef_graduate' is True
    tef_graduates = df[df['tef_graduate'] == True]

    # Restrict from graduates to only the TEF Modules
    tef_graduates_tef_modules = tef_graduates[graduate_tokenIds_list]

    # Find total combined cweight of graduate status (passing all TEF modules)
    total_tef_tokenIds_weight = sum([original_weights_dict.get(tokenId) for tokenId in expert_tokenIds_list])
    
    # Count the number of unique identities/wallets that match the TE Graduates criteria
    number_tef_graduates= df['tef_graduate'].sum()

    original_graduate_cweight = calculate_nft_weighted_sum(df = tef_graduates_tef_modules,
                                                           weights = original_weights_dict)

    # Reality check that the weights match up
    assert original_graduate_cweight == (number_tef_graduates * total_tef_tokenIds_weight), "Unexpected result with TEF graduates weight. "

    original_student_cweight = original_total_cweight - (original_expert_cweight + original_graduate_cweight)


    modified_weights_dict = deepcopy(original_weights_dict)

    if original_student_cweight > original_graduate_cweight:
        tef_graduate_boost = original_student_cweight/number_tef_graduates - total_tef_tokenIds_weight
        scaled_graduates_cweight = (total_tef_tokenIds_weight + tef_graduate_boost) * number_tef_graduates
        scaled_student_cweight = original_student_cweight
        assert isclose(scaled_graduates_cweight - scaled_student_cweight, 0)

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

    
    return modified_weights_dict

    













