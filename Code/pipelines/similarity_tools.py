# %%
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
similarity_threshold = 0.9

# %%
def hierarchical_clustering(code_list):
    """
    Perform hierarchical clustering on a list of code snippets represented as strings.

    Parameters:
    - code_list (list of str): List of code snippets to be clustered.

    Returns:
    - indexes_to_take (list of int): Sorted list of minimum indices representing clusters.
    """
    # Convert codes into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(code_list)
    
    # Apply the Agglomerative Hierarchical Grouping Algorithm
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.4, linkage='average')
    labels = clustering.fit_predict(X.toarray())
    
    # classify files based on grouping labels
    classes = {} # Dictionary to store the classes
    for i, label in enumerate(labels):
        if label not in classes:
            # Initialize empty list for each new label
            classes[label] = []
        classes[label].append(i)  # Add the index of the file instead of the path

    # Convert the dictionary of classes into a list of classes
    classes_list = [file_indices for label, file_indices in classes.items()]
    # Get a min index from each class and sort them
    indexes_to_take_r = map(min,classes_list)
    indexes_to_take = sorted(indexes_to_take_r)
    return indexes_to_take