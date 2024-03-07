import re

def clean_cd(code):
    def remove_empty_lines(code):
        # Split the code snippet into lines
        lines = code.split('\n')
        # Remove empty lines
        non_empty_lines = [line for line in lines if line.strip()]
        # Join the non-empty lines back together
        cleaned_code = '\n'.join(non_empty_lines)
        return cleaned_code
    return remove_empty_lines(re.sub(r'\/\/.*|\/\*[\s\S]*?\*\/', '', code))

#first step: we load the content of the file and remove comments and empty lines
def clean(file_path):
    def remove_empty_lines(code):
        # Split the code snippet into lines
        lines = code.split('\n')
        # Remove empty lines
        non_empty_lines = [line for line in lines if line.strip()]
        # Join the non-empty lines back together
        cleaned_code = '\n'.join(non_empty_lines)
        return cleaned_code
    with open(file_path, 'r') as file:
        content = file.read()
        file.close()
    return remove_empty_lines(re.sub(r'\/\/.*|\/\*[\s\S]*?\*\/', '', content))

def remove_includes(c_code):
    # Define regular expression pattern to match #include directives
    pattern = r'#\s*include\s*<.*?>\s*|#\s*include\s*".*?"\s*'
    # Remove all matches of the pattern
    result = re.sub(pattern, '', c_code)
    return result

#from a code that only contains a function gets the name of the function
def extract_function_name(code):
    function_name_pattern = r'\b\w+\s+(\w+)\s*\([^)]*\)\s*{'
    # Find the function name using regex    
    match = re.search(function_name_pattern, code)
    # If a match is found, extract the function name
    if match:
        function_name = match.group(1)
        return function_name
    else:
        return ""
#from a (struct id {};) gets the id
def struct_name(code):
    struct_name_pattern = r'struct\s+(\w+)\s*\{'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from a (enum id {};) gets the id
def enum_name(code):
    struct_name_pattern = r'enum\s+(\w+)\s*\{'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from a (union id {};) gets the id
def union_name(code):
    struct_name_pattern = r'union\s+(\w+)\s*\{'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from a (typedef struct {} id;) gets the id
def typ_struct_name(code):
    struct_name_pattern = r'typedef\s+struct\s*\{[^{}]*\}\s*(\w+)\s*;'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from a (typedef union {} id;) gets the id
def typ_union_name(code):
    struct_name_pattern = r'typedef\s+union\s*\{[^{}]*\}\s*(\w+)\s*;'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from a (typedef enum {} id;) gets the id
def typ_enum_name(code):
    struct_name_pattern = r'typedef\s+enum\s*\{[^{}]*\}\s*(\w+)\s*;'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""
#from (typedef type * id;) gets the id
def typ_ptr_name(code):
    struct_name_pattern = r'typedef\s+(?:\w+\s*)?\*+\s*(\w+)\s*;'
    # Find the struct name using regex
    match = re.search(struct_name_pattern, code)
    # If a match is found, extract the struct name
    if match:
        struct_name = match.group(1)
        return struct_name
    else:
        return ""

def name_case(key, code):
    if key == "Struct":
        return struct_name(code)
    elif key == "Union":
        return union_name(code)
    elif key == "Enum":
        return enum_name(code)
    elif key == "Typedef_struct":
        return typ_struct_name(code)
    elif key == "Typedef_enum":
        return typ_enum_name(code)
    elif key == "Typedef_union":
        return typ_union_name(code)
    elif key == 'Typedef_Ptrs':
        return typ_ptr_name(code)

#in a code that doesn't include function, type definitions of #include statements
#we use this function to extract the lines where a declaration took place
def extract_global_variables(c_code):
    global_variable_declarations = {}
    # Regular expression pattern to match global variable declarations
    global_variable_pattern = r'\b(?:\w+\s+)*(\w+)\s*(?:\[\s*\d*\s*\])*(?:\s*=\s*(?:[^;]*))?\s*;'
    # Split the code into lines for line numbering
    lines = c_code.split('\n')
    # Find all global variable declarations using regex
    matches = re.finditer(global_variable_pattern, c_code)
    # Extract variable names and their line numbers from matches
    for match in matches:
        global_variable_name = match.group(1)
        # Find the line number of the variable declaration
        line_number = 1
        for i, line in enumerate(lines):
            if match.group(0) in line:
                line_number = i + 1
                break
        global_variable_declarations[global_variable_name] = line_number
    return global_variable_declarations 

def get_line(c_code, i):
    lines = c_code.split('\n')
    if i >= 1 and i <= len(lines):
        return lines[i-1]
    else:
        return "Line number out of range."
#deletes every occurence of substring in original_string
def delete_substring(original_string, substring):
    # Replace every occurrence of the substring with an empty string
    new_string = original_string.replace(substring, "")
    return new_string

#takes a c code and extract the functions alongside their names in a dictianary
def extract_functions(content):
    # Regular expression to match C function definitions
    pattern = r'(?:\w+\s+)+\w+\s*\([^)]*\)\s*{[^{}]*}'
    # Find all matches
    matches = re.findall(pattern, content, re.MULTILINE)
    funs = {}
    for cd in matches:
        nm = extract_function_name(cd)
        funs[nm] = cd
    return funs

#takes the names of all the function names in a c code and in a code that only contains a function F
#we use this function to get the defined functions that were used in F
def functions_in_function(code, all_functions):
    l = []
    for fun in all_functions:
        if fun != extract_function_name(code):
            if (fun+'(' in code) or (fun in code):
                l.append(fun)
    return l

def glo_var_in_function(code, all_var):
    ll = list(all_var)
    l = ll.copy()
    for var in all_var:
        #if ('\n' +var+' ')or(' '+var+' ') or ('\n' +var+'+') \
        #or ('\n' +var+'/') or ('\n' +var+'-') or ('\n' +var+'*') or ('\n' +var+'.')\
        #or (' ' +var+'+') or (' ' +var+'/') or (' ' +var+'-') or (' ' +var+'*') \
        #    or (' ' +var+'.') or (' ' +var+'\n')or(' '+var+' ') or ('+' +var+'\n') \
        #or ('/' +var+'\n') or ('-' +var+'\n') or ('*' +var+'\n') or ('.' +var+'\n')\
        #or ('+' +var+' ') or ('/' +var+' ') or ('-' +var+' ') or ('*' +var+' ') \
        #    or ('.' +var+' ') in code:
        #    
        #if (' '+var+' ') and (var+' ') and (var+'\n') and (var+'+') \
        #    and (var+'*') and (var+'.') and (var+'-') and (var+')') and ('('+var) not in code:
        if var not in code:
            l.remove(var)
    return l

#takes the names of all the function names in a c code and in a code that only contains a function F
#we use this function to get the defined types that were used in F
def types_in_function(code, all_types):
    l = []
    for t in all_types:
        #if ('\n' +t+' ') or (' ' +t+' ') in code:
        if t in code:
            l.append(t) 
    return l

#gets all the global variables and the lines where they were declared
#the code shouldn't contain functions on type declarations
def extract_glo_var(code):
    d = extract_global_variables(code)
    for k in d.keys():
        d[k] = get_line(code, d[k])
    return d  #key: types #value: line of declaration 

#from a c code extracts the type definition in a dictionary
#the keys are the names of the types
def extract_type_blocks(content):
    typs = {}
    # Regular expression patterns to match type blocks
    patterns = [
        (r'struct\s+[^{;]+\s*{[^{}]*}\s*;', "Struct"),
        (r'enum\s+[^{;]+\s*{[^{}]*}\s*;', "Enum"),
        (r'union\s+[^{;]+\s*{[^{}]*}\s*;', "Union"),
        (r'typedef\s+(?:struct)\s*(?:\*\s*)?\s*{[^{}]*}\s*\w+\s*;', "Typedef_struct"),
        (r'typedef\s+(?:union)\s*(?:\*\s*)?\s*{[^{}]*}\s*\w+\s*;', "Typedef_union"),
        (r'typedef\s+(?:enum)\s*(?:\*\s*)?\s*{[^{}]*}\s*\w+\s*;', "Typedef_enum"),
        (r'typedef\s+(?:\w+\s*)?\*+\s*\w+\s*;', "Typedef_Ptrs")
    ]
    for pattern, type_name in patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        for cd in matches:
            nm = name_case(type_name, cd)
            typs[nm] = cd
    return typs

#ps for struct/enum/union id {...}; we should add typdef .... if it wasn't present
#in the original code