from itertools import count
import os
import ast
from code_assembler import *
from extraction_tools import *
from pyspark import SparkContext, SparkConf

'''
This code applies the assembling on all selected father codes and their associated extracted functions.
'''
# Define the path to the data directory 
data_path  = '...'
# Obtain list of subjects from the hashing directory
subjects = os.listdir(data_path+'/cleaned/hashing')
# Path to raw subjects
raw_subjects  = data_path + '/from_source'

# Set Spark application configurations
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")
sc = SparkContext(conf=conf)
print('**********************Beginning assembling**************************')
# Iterate over each subject for assembling
for subject in subjects:
        print(f"**************************{subject}********************************")
        # Load the hashing information from RDDs 
        codes = sc.textFile(data_path+'/cleaned/hashing/'+subject+'/'+subject+'_assembeled_by_key')\
            .map(lambda line: ast.literal_eval(line))
        hashmap = sc.textFile(data_path+'/cleaned/hashing/'+subject+'/'+subject+'_hashing')\
            .map(lambda line: ast.literal_eval(line))
        # Convert the hashmap RDD to dictionary
        hashmap = dict(hashmap.collect())
        # This function applies the assembler indirectly through the hashing key
        def code_assembler_by_key(key,lst):
            original_code_file_name = hashmap[key]
            return code_assembler(raw_subjects, subject, original_code_file_name, lst)
        
        # Apply code assembler function to each pair in RDD
        long_strings = codes.map(lambda pair: code_assembler_by_key(pair[0], pair[1]))#.flatMap(lambda x: x)
        # Define output path for assembled codes
        output_path = f"{data_path}/cleaned/assembeled/{subject}"
        # Save assembled codes as text files
        long_strings.saveAsTextFile(output_path)
        print(f"{subject} assembling is finalized!!")
# Stop the Spark context
sc.stop()
    

    

    