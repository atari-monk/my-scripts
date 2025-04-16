import os

def get_script_info(args, verbose=False):
    script_path = args[0]
    script_name = os.path.basename(script_path)
    script_directory = os.path.dirname(script_path)
    
    if(verbose) :
        print(f"Script Name: {script_name}")
        print(f"Script Directory: {script_directory}")
        print(f"Arguments: {args}")
        
    return args[1:], script_name, script_directory