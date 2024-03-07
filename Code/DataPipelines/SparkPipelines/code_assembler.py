from extraction_tools import *
'''
This function takes in a father code and a list of extracted functions from this code 
and reassembles each function in the context of the father code (types, global variables ...)
It was used in the spark pre-processing code
'''
def code_assembler(from_source_path, subject, original_code_file_name, lst_codes):
    father_code_path = from_source_path + '/' + subject + '_fs/' + original_code_file_name + '.c'
    content = clean(father_code_path)
    #intermediary functions
    all_functions = {}
    lst_codes = [clean_cd(cd) for cd in lst_codes]
    for cd in lst_codes:
        nm = extract_function_name(cd)
        all_functions[nm] = cd
    #getting all the types, global variables in the father code
    #types
    all_types = extract_type_blocks(content)
    #types names
    all_types_names = all_types.keys()
    #function_names
    all_functions_names = all_functions.keys()
    content2 = content
    for k in all_functions_names:
        content2 = delete_substring(content2, all_functions[k])
    for kk in all_types_names:
        content2 = delete_substring(content2, all_types[kk])
    content2 = remove_includes(content2)
    #global variables
    all_variables = extract_glo_var(content2)
    #global variables names
    all_variables_names = all_variables.keys()
    def deep_fun_in_fun(name):
        return functions_in_function(all_functions[name], list(all_functions_names)) + [name]
    funs_in_fun = {}
    vars_in_fun = {}
    typs_in_fun = {}
    #for each function i extract all the functions it needs
    for fun in all_functions_names:
        cd = all_functions[fun]
        ini_list = functions_in_function(cd, all_functions_names)
        n = -1
        while n != len(ini_list):
            n = len(ini_list)
            ini_list = list(set([item for sublist in map(deep_fun_in_fun, ini_list) for item in sublist]))
            funs_in_fun[fun] = ini_list

    #for each function i extract all the types and variables it needs
    for fun in all_functions_names:
        cd = all_functions[fun]
        vars_in_fun[fun] = glo_var_in_function(cd, all_variables_names)
        typs_in_fun[fun] = types_in_function(cd, all_types_names)
    ret = []
    ret.append(content)
    for fun in all_functions_names:
        if fun!='main':
            code = '//...' + '\n'
            for typ in typs_in_fun[fun]:
                code = code + all_types[typ] + '\n'
            for var in vars_in_fun[fun]:
                code = code + all_variables[var] + '\n'
            for f in funs_in_fun[fun]:
                code = code + all_functions[f] + '\n'
            code = code + all_functions[fun] + '\n'
            code = code + '//...'
            ret.append(code)

    return ret