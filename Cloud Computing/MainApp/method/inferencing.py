import numpy as np
import pandas as pd 

BASE_PROMPT = """
Anda telah menetapkan titik lokasi di Maps Interface untuk mendirikan bisnis. Sistem kemudian memberikan output clustering dengan statistik sebagai berikut. Clustering kompetitif menghasilkan tiga kelompok (kelompok A, B, dan C) dengan statistik sebagai berikut:
"""

NEGATIVE_PROMPT = """
Tidak perlu berikan langkah selanjutnya, atau saran, atau bahkan penutup. Jelaskanlah dalam paragraf saja, tanpa subjudul seperti ##, tanpa menggunakan bahasa terlalu teknis, dan tidak menjelaskan dengan angka.
"""

SMALL_BASE_PROMPT = """
Itu adalah hasil inferensi dari hasil segmentasi kompetitif terhadap titik lokasi yang Anda tetapkan. Hasil clustering berakhir dengan proporsi masing-masing cluster adalah sebagai berikut.
"""

INSTRUCTION_SMALL_PROMPT = """
Jelaskanlah dalam paragraf 350 karakter kondisi dominasi menuju mengapa hasil inferensinya sedemikian dalam paragraf saja, tanpa subjudul seperti ##, tanpa menggunakan bahasa terlalu teknis, dan tidak menjelaskan dengan angka.
"""

# Fungsi untuk menghitung modus (nilai yang paling sering muncul)
def mode(series):
    return series.mode().iloc[0]

# Fungsi untuk menghitung statistik deskriptif
def calculate_descriptive_stats(df):

    # Menambahkan kolom baru untuk jumlah rating 1-3 dan 4-5
    df['rating_1_3'] = df['reviews_one_star'] + df['reviews_two_star'] + df['reviews_three_star']
    df['rating_4_5'] = df['reviews_four_star'] + df['reviews_five_star']

    # Menghitung statistik deskriptif
    descriptive_stats = df.groupby('cluster').agg({
        'place_id': 'count',
        'main_category': [mode],
        # 'rating': ['mean'],
        # 'zero_review': 'sum',  
        'rating_1_3': ['mean'],  
        'rating_4_5': ['mean'],  
        'top_average_popularity': ['mean'],
        'nearest_competitor_distance': ['mean']
    }).reset_index()
        
    return descriptive_stats

# Function to generate details for each cluster
def generate_cluster_summary(df):
    summaries = []
    for index, row in df.iterrows():
        summary = (f"kelompok {row[('cluster', '')]} memiliki {row[('place_id', 'count')]} tempat, "
                   f"dengan kategori utama: {row[('main_category', 'mode')]}. "
                   f"Rata-rata rating (1-3): {row[('rating_1_3', 'mean')]:.2f}, "
                   f"rata-rata rating (4-5): {row[('rating_4_5', 'mean')]:.2f}, "
                   f"popularitas rata-rata: {row[('top_average_popularity', 'mean')]:.2f}, "
                   f"jarak rata-rata ke kompetitor terdekat: {row[('nearest_competitor_distance', 'mean')]:.2f} meter.")
        summaries.append(summary)
    return "\n".join(summaries)

def generate_cluster_proportion_summary(cluster_counts):
        
    # Calculate total number of elements
    total_count = cluster_counts.sum()
    
    # Calculate the proportion of each cluster
    proportions = cluster_counts / total_count * 100

    summary = "Proporsi setiap kelompok adalah sebagai berikut:\n"
    
    for cluster, proportion in proportions.items():
        summary += f"kelompok {cluster}: {proportion:.2f}% dari total\n"
    
    return summary

# Function to generate summary
def generate_cluster_meaning(df):
    summaries = {}
    max_popularity = df[('top_average_popularity', 'mean')].max()
    min_popularity = df[('top_average_popularity', 'mean')].min()

    for index, row in df.iterrows():
        if row[('top_average_popularity', 'mean')] == max_popularity:
            popularity_comment = "popularitas tertinggi."
        elif row[('top_average_popularity', 'mean')] == min_popularity:
            popularity_comment = "popularitas terendah."
        else:
            popularity_comment = "popularitas sedang."

        summary = (f"{row[('cluster', '')]} "
                   f"didominasi oleh {row[('main_category', 'mode')]}, "
                   f"{popularity_comment}")
        summaries[row[('cluster', '')]] = summary
    
    return summaries

def small_text_modelling(clustering_result, stats_prompt, BASE_PROMPT=SMALL_BASE_PROMPT, INSTRUCTION_PROMPT=INSTRUCTION_SMALL_PROMPT):

    prompt = "Tingkat persaingan di area ini termasuk " + clustering_result + SMALL_BASE_PROMPT + stats_prompt + INSTRUCTION_PROMPT
    
    return prompt

def summary_heading(cluster_counts):

    # Calculate total number of elements
    total_count = cluster_counts.sum()
    
    # Calculate the proportion of each cluster
    proportions = cluster_counts / total_count * 100
    
    # Identify the two largest proportions
    largest_proportions = proportions.nlargest(2)
    
    # Check if both largest proportions are within 25-45%
    is_fairly_competitive = all((largest_proportions >= 33) & (largest_proportions <= 50))

    if is_fairly_competitive:
        summary_header = "fairly competitive"
    else:
        summary_header = "highly competitive"
    
    return summary_header 

def text_modelling(stats_prompt, BASE_PROMPT=BASE_PROMPT, NEGATIVE_PROMPT=NEGATIVE_PROMPT):
    
    prompt = BASE_PROMPT + stats_prompt + NEGATIVE_PROMPT
    
    return prompt


