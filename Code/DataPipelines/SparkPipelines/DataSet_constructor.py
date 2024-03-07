"""
This script processes annotated data and extracts prompts and corresponding code snippets.

"""

import csv
import os
# Path to the directory containng annotated data
data_path = '...'
# List of all subjects
subjects = os.listdir(data_path)

# This function extracts prompts and code snippets from a line of text
def extract_prompt_and_code(line):
    # Split the content by "', '"
    # parts = file_content.split("', '")
    if "<<UEFACL>>" in line:
       # The string is added when annotating the data in order to use it here to split prompts from code snippets
       parts = line.split("<<UEFACL>>")
       prompt, code  = parts[0], parts[1][4:]
    else:
      parts = line.split("', '") 
      if len(parts) == 1:
        parts = line.split("\", '")
      if len(parts) == 1:
        parts = line.split("\", \"")
      if (len(parts)== 1):
        parts = line.split("', \"")
    #if len(parts) > 1:
    #    prompt = parts[0].strip()
    #    code = "', '".join(parts[1:]).strip().strip("',")
      prompt, code  = parts[0], parts[1] 
    return prompt, code

# Iterate over each subject
for subject in subjects:
  if subject != "DSP_digital_signal_processing_embedded_systems":
    folders = os.listdir(f'{data_path}/{subject}')
    # Open a CSV file to write the extracted codes and prompts
    with open(f'/media/ielalout/Transcend/1GenAI/Prj_Lng/data/output_{subject}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create two columns, one for prompts and one for codes
        fieldnames = ['prompt', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Here we need to iterate over each folder as the annotated data, for each subject, is spread over different folders
        for folder in folders:
            folder_path = os.path.join(f'{data_path}/{subject}', folder)
            print(folder_path)
            # The Spark annotation job was executed on 4 nodes
            for i in range(4):
                file = open(f'{folder_path}/part-0000{i}', 'r')
                lines = file.readlines()
                #with open(f'{folder_path}/part-0000{i}', 'r') as file:
                # Extract prompts and code snippets from each line of the file content
                for line in lines:
                    #for line in file:    
                        
                    content = line[1:-2] #file.read()
                    #print(content)
                    prompt, code = extract_prompt_and_code(content)
                    writer.writerow({'prompt': prompt, 'code': code})
                        #print(f'prompt:  {prompt}')
                        #print(f'code: {code}')
                        #print("******************************************************************************************************")

print("CSV files created successfully!")
