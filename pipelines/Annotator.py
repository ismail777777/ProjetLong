import json
import os
import tokenize
import io
import re

# //topic
# //specifics
# //task


class Annotator:
    #static variable for topic names
    #of the following form:
    #Full_Name
    #Acronym_FullName

    # List to store topic names
    topics = []
    # Number of topics
    n_topics = 0
    # Workspace directory path
    workspace = "C:/Users/hlilo/Downloads/Prj_Lng"
    

    # Initialize the annotator 
    # For this, we only need the acronyms
    # if they don't exist we use the full name
    def __init__(self, new_topics):
        new_topics_search = []
        for acro in new_topics:
            inter = len(new_topics_search)
            for fold_name in os.listdir(self.workspace):
                if fold_name.startswith(acro):
                    new_topics_search.append(fold_name)
            if inter == len(new_topics_search):
                print(f'acronym {acro} non existant')
        self.topics = new_topics_search
        self.n_topics = len(new_topics_search)
        os.chdir(self.workspace)

    # This method is responsible for cleaning the code files. 
    # It removes comments, extracts the first three comments, and removes empty lines from the code.
    def cleaning(self,folder_name):
        cleaned = [] # List to store the cleaned content of the code files
        prompts = [] # List to store the first three comments
        #removes all comments
        def remove_comments(code):
            return re.sub(r'\/\/.*|\/\*[\s\S]*?\*\/', '', code)
        #removes all comments and extracts the first three
        def extract_first_three_comments_and_clean(file_content):
            # Regular expression pattern to match single-line comments
            single_line_comment_pattern = r'//.*?$'
            # Regular expression pattern to match multi-line comments
            multi_line_comment_pattern = r'\/\*[\s\S]*?\*\/'
            # Find all single-line comments
            single_line_comments = re.findall(single_line_comment_pattern, file_content, re.MULTILINE)
            # Find multi-line comments
            multi_line_comments = re.findall(multi_line_comment_pattern, file_content, re.MULTILINE)
            # Extract the first three comments
            first_three_comments = single_line_comments[:3] + multi_line_comments[:3 - len(single_line_comments)]
            # Remove all comments from the file content
            cleaned_content = re.sub(single_line_comment_pattern, '', file_content)
            cleaned_content = re.sub(multi_line_comment_pattern, '', cleaned_content)
            # Remove leading and trailing whitespace
            cleaned_content = cleaned_content.strip()


            cleaned.append(remove_empty_lines(remove_comments(cleaned_content)))
            prompts.append('=>'.join(((''.join(first_three_comments))[2:]).split('//')))

        #removes empty lines
        def remove_empty_lines(code):
            # Split the code snippet into lines
            lines = code.split('\n')
            # Remove empty lines
            non_empty_lines = [line for line in lines if line.strip()]
            # Join the non-empty lines back together
            cleaned_code = '\n'.join(non_empty_lines)
            return cleaned_code
        
        c_code_list = []  # List to store code contents
        
        # Iterate over .c files in the folder
        for filename in os.listdir(folder_name):
            if filename.endswith('.c'):
                # Read content of the file
                with open(os.path.join(folder_name, filename), 'r') as file:
                    code_content = file.read()
                    c_code_list.append(code_content)
                    file.close()
        for cd in c_code_list:
            extract_first_three_comments_and_clean(cd)
        return cleaned, prompts

    # This method converts cleaned code into tokens
    def tokenizing(self,cleaned_code):
        # function to tokenize a single code snippet
        def tokentomap(code):
            # Tokenize the code snippet using Python's tokenize module
            # Encode the code snippet to UTF-8 bytes and read it as lines of code
            # Return a list of token strings from the code snippet
            return [tok.string for tok in tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)]
        # Apply the tokentomap function to each cleaned code snippet in the list
        return [tokentomap(cd) for cd in cleaned_code]

    # This method iterates through each topic, 
    # cleans the code files within that topic,
    # tokenizes the cleaned code, and saves the data as JSON files.
    def build_dataset(self):
        
        for top in self.topics:
            topic_files_folder = self.workspace + '/' + top
            cleaned_code, prompts = self.cleaning(topic_files_folder)
            tokenized_code = self.tokenizing(cleaned_code)

            dataset = [{'prompt': prmpt, 'cleaned_code': cln_cd, 'tokenized_code': tok_cd} for prmpt, cln_cd, tok_cd in zip(prompts, cleaned_code, tokenized_code)]

            topic_json_file = self.workspace + '/' + top + '.json'
            # Save the data to a JSON file
            with open(topic_json_file, 'w') as json_file:
                json.dump(dataset, json_file)
                json_file.close()
            print(f'{top}.json was created in {self.workspace}')

        print('Cleaning, and Annotating ... Finished')


#'/home/othmane/Downloads/Prj_Lng/Data_Encryption.json'



        

