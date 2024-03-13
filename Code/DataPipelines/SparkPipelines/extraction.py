"""
This script extracts information from a C file and writes the extracted information into separate files.
An example of the assembler.

"""

from extraction_tools import *
import os

# Path to the C file
file_path ='.../file.c'
# Clean the content of the file 
content = clean(file_path)
# Extract the functions 
all_functions = extract_functions(content)
del all_functions['main']
# Extract the type blocks
all_types = extract_type_blocks(content)
# Extract the names of all functions and types
all_functions_names = all_functions.keys()
all_types_names = all_types.keys()
content2 = content
# Remove functions and types blocks from the content 
for k in all_functions_names:
    content2 = delete_substring(content2, all_functions[k])
for kk in all_types_names:
    content2 = delete_substring(content2, all_types[kk])
content2 = remove_includes(content2)
# Extract the global variables
all_variables = extract_glo_var(content2)
# Names of the global variables
all_variables_names = all_variables.keys()

# This function retrieves function within a function recursively
def deep_fun_in_fun(name):
    return functions_in_function(all_functions[name], list(all_functions_names)) + [name]

# Initialize dictionaries to store information about functions, variables and types within functions
funs_in_fun = {}
vars_in_fun = {}
typs_in_fun = {}
# Iterate over each function
for fun in all_functions_names:
    cd = all_functions[fun]
    # List of functions within the current function fun
    ini_list = functions_in_function(cd, all_functions_names)
    n = -1
    while n != len(ini_list):
        n = len(ini_list)
        ini_list = list(set([item for sublist in map(deep_fun_in_fun, ini_list) for item in sublist]))
        funs_in_fun[fun] = ini_list


for fun in all_functions_names:
    cd = all_functions[fun]
    vars_in_fun[fun] = glo_var_in_function(cd, all_variables_names)
    typs_in_fun[fun] = types_in_function(cd, all_types_names)

path = '....'  #output folder
for fun in all_functions_names:
        code = '//...' + '\n'
        for typ in typs_in_fun[fun]:
            code = code + all_types[typ] + '\n'
        for var in vars_in_fun[fun]:
            code = code + all_variables[var] + '\n'
        for f in funs_in_fun[fun]:
            code = code + all_functions[f] + '\n'
        code = code + all_functions[fun] + '\n'
        code = code + '//...'
        with open(path+'/'+fun+'.txt', "w") as file:
            file.write(code)
            file.close()
print("Extraction Complete!")



