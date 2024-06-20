import pandas as pd

def sample_cluster(group, top_competitors_ids):
    # Filter out the top competitors from the group
    group = group[~group['place_id'].isin(top_competitors_ids)]
    
    # Sample the remaining places
    sampled_group = group.sample(n=min(len(group), 12))
    
    return sampled_group

def show_on_map(df):
    
    # Create a new column for reviews*rating
    df['reviews'] = df['reviews_one_star'] + df['reviews_two_star'] + df['reviews_three_star'] + df['reviews_four_star'] + df['reviews_five_star']
    df['reviews*rating'] = df['reviews'] * df['rating']

    # Identify the top three competitors overall
    top_competitors_df = df.nlargest(3, 'reviews*rating')
    top_competitors_ids = top_competitors_df['place_id'].tolist()

    # Add a new column 'top' to indicate rank
    top_competitors_df = top_competitors_df.reset_index(drop=True)
    top_competitors_df['top'] = top_competitors_df.index + 1

    # Convert 'top' column to int32
    top_competitors_df['top'] = top_competitors_df['top'].astype('int32')

    # Group by cluster and apply the sampling function, excluding the top competitors
    sampled_list = []
    
    for _, group in df.groupby('cluster'):
        sampled_group = sample_cluster(group, top_competitors_ids)
        sampled_list.append(sampled_group)

    sampled_df = pd.concat(sampled_list).reset_index(drop=True)

    # Always add top competitors on map interface
    result_df = pd.concat([sampled_df, top_competitors_df]).reset_index(drop=True)
    
    # Select the required columns for sampled data
    result_df = result_df[['place_id', 'name', 'coordinates', 'main_category', 'featured_image', 'reviews', 'rating', 'cluster', 'top']]

    # Fill 'top' column with null for non-top competitors
    result_df['top'] = result_df['top'].fillna(0).astype('int32')
    
    return result_df