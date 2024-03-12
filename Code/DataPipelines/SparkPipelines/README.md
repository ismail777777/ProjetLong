# Content
This an implementation of Spark jobs that perform the cleaning, assembling, hashing and annotation of code snippets related to embedded programming in C
# Steps
## Step 1: from Source to Raw
In this step, deduplication is performed on the code snippets.
The output data is stored in the "raw" folder. 
Corresponding file: "from_source_to_raw.py"

## Step 2: from Raw to Clean
### Assembling: 
This Spark job .... 
The output data is stored in the "cleaned/ " folder. 
Corresponding file: "raw_to_clean_1.py"
### Hashing:
This Spark job assembles every extracted function with its corresponding father code through the hashing key.
The output data is stored in the "cleaned/assembeled" folder. 
Corresponding file: "raw_to_clean_2.py"
## Step 3: from Clean to Annotated
In thi step, a request is sent for each code snippet to the OpenAI API in order to provide its annotation.
The output data is stored in the "annotated" folder.
Corresponding file: "clean_to_anno.py"

# Usage
- The path to the data directory must be set in all Spark jobs.
- For the third step, an OpenAI API key needs to be set in the Spark configuration.
