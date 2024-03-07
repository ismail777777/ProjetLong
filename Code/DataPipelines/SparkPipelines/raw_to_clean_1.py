# Define the path to the data directory
data_path  = '...'
import os
from pyspark import SparkContext, SparkConf

'''
To each file that contains a representative father code, we attribute a hashing key that references 
all the extracted functions, so we can link each father and child code through this hashing key.
The point is to avoid the file system's naming.  
'''
# Obtain the list of subjects
raw_subj_list = os.listdir(data_path+'/raw/RDDs')

# Set up Spark application configurations
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Iterate over each subject in the raw data directory
for subject in raw_subj_list:
    
        print(f'*****************************{subject}******************************')
        code_files_rdd = sc.textFile(data_path+'/raw/RDDs/'+subject)
        code_files = code_files_rdd.collect()
        
        hashmap = {}
        for k in range(len(code_files)):
            hashmap[k] = code_files[k].rsplit('.',1)[0]
        hashmap_listed = list(hashmap.items())
        # This function references the extracted functions codes.
        def load_text_files(key):
            folder_name = hashmap[key]+'_ext'
            directory = data_path+'/from_source/'+subject+'/'+folder_name
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('_code.txt')]
            sub_codes = []
            for file in files:
                with open(file, 'r') as f:
                    sub_codes.append(f.read())
                    f.close()
            return (key, sub_codes)
        # Create an RDD for hashing
        hashing_rdd = sc.parallelize(hashmap_listed)
        # Create an RDD for loading text files (assembled)
        text_files_rdd = sc.parallelize([h for h in range(len(hashmap_listed))]).map(load_text_files)

        # Save the assembled text files and the hashing results
        text_files_rdd.coalesce(1).saveAsTextFile(data_path+'/cleaned/hashing/'+('_'.join((subject.split('_'))[0:-1]))+'/'+('_'.join((subject.split('_'))[0:-1]))+'_assembeled_by_key')
        hashing_rdd.coalesce(1).saveAsTextFile(data_path+'/cleaned/hashing/'+('_'.join((subject.split('_'))[0:-1]))+'/'+('_'.join((subject.split('_'))[0:-1]))+'_hashing')

        print(f"{' '.join((subject.split('_'))[1:-1])} codes have been hashed key_assembled!!")

# Stop the spark context
sc.stop()
    