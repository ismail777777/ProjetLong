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

# Custom accumulator to increment the global counter
class CounterAccumulatorParam(AccumulatorParam):
    def zero(self, initialValue):
        return initialValue

    def addInPlace(self, v1, v2):
        return v1 + v2

# Define the path to the data directory
data_path = '/media/ielalout/Transcend/1GenAI/Prj_Lng/data'
# Define input and output folder paths
input_folders_path = data_path + '/cleaned/assembeled'
output_folders_path = data_path + '/annotated'

# Set Spark application configurations (here you will need to replace ... with you own OpenAI API key)
conf = SparkConf().setAppName("FolderTextFilesLoader").setMaster("local[*]")\
    .set("spark.executorEnv.OPENAI_API_KEY", '...')\
    .set("spark.driver.extraJavaOptions", "-Djava.home=/usr/lib/jvm/java-11-openjdk-amd64/")\
    .set("spark.executor.extraJavaOptions", "-Djava.home=/usr/lib/jvm/java-11-openjdk-amd64/")
sc = SparkContext(conf=conf)

counter = sc.accumulator(0, CounterAccumulatorParam())
# Get list of subjects in the input folder
subjects = os.listdir(input_folders_path)
print('**********************Beginning annotating**************************')
# Iterate over each subject 
for subject in subjects[1:2]:
    print(f"**************************{subject}********************************")
    #os.makedirs(output_folders_path+'/'+subject+'/prompts')
    #os.makedirs(output_folders_path+'/'+subject+'/codes')
    # Load codes as RDD and map them to Python objects
    codes = sc.textFile(input_folders_path+'/'+subject).map(lambda line: ast.literal_eval(line))
    # Function to annotate codes using OpenAI's API
    def annotate(list_of_codes):
        #timestamp = (time.time())
        #global counter
        #counter += 1
        #new_file_name = f"file_{counter}.txt"

        # List to store the obtained prompts and codes
        ret = []
        # Set OpenAI key
        openai.api_key = '...'
        for code in list_of_codes:
            #rqst = "For the following embedded systems code, give me the prompt i could have given you\
#for you to give me that code as a response, in this prompt detail the scenario with respect to embedded systems:" + "\n" + code
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
            ret.append((prompt+ "<<UEFACL>>", code))
            #ret.append(prompt + "<<UEFACL>>" + code)

            # We add this in order to prevent errors,
            # linked to exceeding the limit of maximum requests per minute
            time.sleep(10)
            #with open(output_folders_path+'/'+subject+'/prompts/'+new_file_name, 'w') as f:
                #f.write(prompt)
                #f.close() 
            #with open(output_folders_path+'/'+subject+'/codes/'+new_file_name, 'w') as f:
                #f.write(code)
                #f.close() 
        return ret
    #print(codes.count())
    full_length = codes.count()
    #codes = sc.parallelize(codes.take(50)) #"560 to 580 dsp prob max_tokens"
    # indexing 
    
    indexed_codes = codes.zipWithIndex()
    codes = indexed_codes.filter(lambda x: 10<=  x[1] < 14).map(lambda x: x[0]) #25 to 30 grpahics, 100 to 105, 180 to 185, networking: 40 to 60, 120 to 150, 170 to 180
    codes = sc.parallelize(codes.collect())
    print(f"{codes.count()}/{full_length}")
    # Apply the annotate function to each code
    prpt_code = codes.flatMap(lambda lst: annotate(lst))
    hostname = socket.gethostname()
    # output_path = output_folders_path+'/'+subject+'/'+subject+'_backup'
    # coalesce(1).
    # Define the output path for the annotated codes
    output_path = f"{output_folders_path}/{subject}/{subject}_backup_2"
    # Save the annotated prompts and codes as text files
    prpt_code.saveAsTextFile(output_path)


sc.stop()

