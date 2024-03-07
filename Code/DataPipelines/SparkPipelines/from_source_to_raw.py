from similarity_tools import *
import os
from pyspark import SparkContext, SparkConf
'''
This code selects the representative codes from the whole dataset.
Deduplicates the data using the function defined in "similarity_tools.py" and references the codes to be used in the "raw" folder.
'''
# Set Spark application configurations
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")    
sc = SparkContext(conf=conf)

# Define the path to the data directory
data_path = '...'

# Define input and output folder paths
input_folders_path = data_path + '/from_source'
output_folder_path = data_path + '/raw'

# List subjects in the input folder
subjects = os.listdir(input_folders_path)

# Iterate over subjects
for subject in subjects:
    print(f'=====> subject: {subject} <=====')
    # Define the path to the subject's folder
    subject_path = input_folders_path + '/' + subject
    # Select c files
    files_names = [fl for fl in os.listdir(subject_path) if fl.endswith('.c')]
    # Read the content of selected files
    corresponding_codes = [open(subject_path + '/' + file, 'r').read() for file in files_names]
    # Perform hierarchical clustering on the codes to classify them
    classification = hierarchical_clustering(corresponding_codes)
    # Create a list of file names based on the classification
    classification_list = [files_names[i] for i in classification]
    # Parallelize the classification list using Spark
    sc.parallelize(classification_list).coalesce(1).saveAsTextFile(output_folder_path + '/' +'RDDs/'+ subject+'3')
    print('********end of subject*********')
sc.stop()