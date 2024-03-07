from itertools import count
import os
import ast
from code_assembler import *
from extraction_tools import *
from pyspark import SparkContext, SparkConf

# Define the path to the data directory 
data_path  = '/media/ielalout/Transcend/1GenAI/Prj_Lng/data'
# Obtain list of subjects from the hashing directory
subjects = os.listdir(data_path+'/cleaned/hashing')
# Path to raw subjects
raw_subjects  = '/media/ielalout/Transcend/1GenAI/Prj_Lng/data/from_source'

# Set Spark application configurations
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")
sc = SparkContext(conf=conf)
#subjects = os.listdir(codes_and_keys_folders)
print('**********************Beginning assembling**************************')
# Iterate over each subject for assembling
for subject in subjects:
    if subject != 'DSP_digital_signal_processing_embedded_systems':
        print(f"**************************{subject}********************************")
        # Load the hashing information from RDDs 
        codes = sc.textFile(data_path+'/cleaned/hashing/'+subject+'/'+subject+'_assembeled_by_key')\
            .map(lambda line: ast.literal_eval(line))
        hashmap = sc.textFile(data_path+'/cleaned/hashing/'+subject+'/'+subject+'_hashing')\
            .map(lambda line: ast.literal_eval(line))
        # Convert the hashmap RDD to dictionary
        hashmap = dict(hashmap.collect())
        #function to apply the flat map (to assemble code by key)
        def code_assembler_by_key(key,lst):
            original_code_file_name = hashmap[key]
            #original_code_file_name = hashmap.lookup(key)[0]
            return code_assembler(raw_subjects, subject, original_code_file_name, lst)
        
        # Apply code assembler function to each pair in RDD
        long_strings = codes.map(lambda pair: code_assembler_by_key(pair[0], pair[1]))#.flatMap(lambda x: x)

        #long_strings = (long_strings.collect())
        #long_strings = [item for sublist in long_strings for item in sublist]
        
        #new_rdd = sc.parallelize(long_strings)

        # Define output path for assembled codes
        output_path = f"{data_path}/cleaned/assembeled/{subject}"
        #formatted_rdd.coalesce(1).saveAsTextFile(output_path)

        # Save assembled codes as text files
        long_strings.saveAsTextFile(output_path)


        #counter = 0
        #for c in long_strings:
        #    counter +=1
        #    path = f"{data_path}/cleaned/assembeled/{subject}/code_{counter}.txt"
        #    with open(path, 'w') as f:
        #        f.write(str(c) + '\n')
        #        f.close()

        print(f"{subject} assembling is finalized!!")
# Stop the Spark context
sc.stop()
    

    

    