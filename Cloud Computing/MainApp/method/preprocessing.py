import json
import numpy as np
import pandas as pd 

from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

COLUMNS_FOR_MODELLING = ['rating', 'reviews_one_star', 'reviews_two_star', 
            'reviews_three_star', 'reviews_four_star', 
            'reviews_five_star', 'average_hour', 'std_hour', 
            'avg_popularity', 'top_hour_popularity', 'top_average_popularity']

def impute(df, COLUMNS_FOR_MODELLING=COLUMNS_FOR_MODELLING):
    # Mengubah kolom yang bersangkutan menjadi tipe data float
    df[COLUMNS_FOR_MODELLING] = df[COLUMNS_FOR_MODELLING].astype(float)

    # Inisialisasi KNNImputer
    imputer = KNNImputer(n_neighbors=5)

    # Menerapkan KNNImputer hanya pada kolom yang bersangkutan
    df[COLUMNS_FOR_MODELLING] = imputer.fit_transform(df[COLUMNS_FOR_MODELLING])

    return df

def pca(df, n_components=3, COLUMNS_FOR_MODELLING=COLUMNS_FOR_MODELLING):
    
    # Initiate MinMaxScaler and PCA
    scaler = MinMaxScaler()
    pca = PCA(n_components=n_components)
    
    # Normalization and PCA
    matrix_columns = df[COLUMNS_FOR_MODELLING].values
    normalized_matrix = scaler.fit_transform(matrix_columns)
    norm_df = df[COLUMNS_FOR_MODELLING].copy()
    norm_df[COLUMNS_FOR_MODELLING] = normalized_matrix
    principal_components = pca.fit_transform(norm_df[COLUMNS_FOR_MODELLING])
    
    # Convert PCA to pandas dataframe
    pca_columns = [f'PC{i+1}' for i in range(n_components)]
    matrix_df = pd.DataFrame(data=principal_components, columns=pca_columns)
    
    # Formatting columns names
    pca_df = pd.concat([df[['place_id', 'name', 'coordinates', 'main_category', 'nearest_competitor_place_id', 'nearest_competitor_distance', 'featured_image'] + COLUMNS_FOR_MODELLING], matrix_df], axis=1)

    return pca_df

def split_reviews_per_rating(df):
    # Ensure 'reviews_per_rating' is a dictionary
    if isinstance(df['reviews_per_rating'].iloc[0], dict):
        # Split the dictionary values into new columns
        df = pd.concat([df.drop(['reviews_per_rating'], axis=1), df['reviews_per_rating'].apply(pd.Series)], axis=1)

        # Rename columns for clarity
        df.rename(columns={'1': 'reviews_one_star', '2': 'reviews_two_star', '3': 'reviews_three_star',
                            '4': 'reviews_four_star', '5': 'reviews_five_star'}, inplace=True)

    return df 