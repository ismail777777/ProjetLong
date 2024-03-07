import ast
import os
import openai
import json 
import io
import time
from pyspark import SparkContext, SparkConf
from pyspark.accumulators import AccumulatorParam
import socket
import time


# Define the path to the data directory
data_path = '...'
# Define input and output folder paths
input_folders_path = data_path + '/cleaned/assembeled'
output_folders_path = data_path + '/annotated'

# Set Spark application configurations (here you will need to replace ... with you own OpenAI API key)
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")\
    .set("spark.executorEnv.OPENAI_API_KEY", '...')\
    .set("spark.driver.extraJavaOptions", "-Djava.home=/usr/lib/jvm/java-11-openjdk-amd64/")\
    .set("spark.executor.extraJavaOptions", "-Djava.home=/usr/lib/jvm/java-11-openjdk-amd64/")
sc = SparkContext(conf=conf)

# Get list of subjects in the input folder
subjects = os.listdir(input_folders_path)
print('**********************Beginning annotating**************************')
# Iterate over each subject 
for subject in subjects:
    print(f"**************************{subject}********************************")

    # Load codes as RDD and map them to Python objects
    codes = sc.textFile(input_folders_path+'/'+subject).map(lambda line: ast.literal_eval(line))
    # Function to annotate codes using OpenAI's API
    def annotate(list_of_codes):
        # List to store the obtained prompts and codes
        ret = []
        # Set OpenAI key
        openai.api_key = '...'
        for code in list_of_codes:
            # The request given to the API to obtain the annotation
            rqst = "For the following code, give me the prompt i could have given you\
for you to give me that code as a response, in this prompt detail the technical scenario:" + "\n" + code
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model to automatically annotate each code of the subject
                messages=[
                    {"role": "user", "content": rqst}
                ],
                max_tokens=200  # Specify the maximum length of the generated text
            )
            # Extract the generated response
            prompt = response.choices[0].message['content']
            prompt = '. '.join(prompt.split('\n'))
            ret.append((prompt+ "<<UEFACL>>", code)) # special token used for splitting prompts from codes later
            # We add this in order to prevent errors,
            # linked to exceeding the limit of maximum requests per minute
            time.sleep(10)
        return ret
    full_length = codes.count()

    # indexing     
    indexed_codes = codes.zipWithIndex()
    # These variables are used to set the chunk of the data which will be annotated (need to be set)
    # This is crucial, because some codes in the RDD cannot be annotated by the OpenAI API and in the case the spark job fails 
    # (their token length exceeds the maximum number of tokens per request)
    min_extr = 10
    max_extr = 14
    codes = indexed_codes.filter(lambda x: 10<=  x[1] < 14).map(lambda x: x[0])
    codes = sc.parallelize(codes.collect())
    print(f"{codes.count()}/{full_length}")
    # Apply the annotate function to each code
    prpt_code = codes.flatMap(lambda lst: annotate(lst))
    hostname = socket.gethostname()

    # Define the output path for the annotated codes
    output_path = f"{output_folders_path}/{subject}/{subject}"
    # Save the annotated prompts and codes as text files
    prpt_code.saveAsTextFile(output_path)


sc.stop()

