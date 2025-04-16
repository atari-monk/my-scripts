import os
from datetime import datetime
from core.utils.script_utils import get_script_info

def get_file_path(config, args=[]):
    args, script_name, _ = get_script_info(args)
    
    current_year = datetime.now().strftime('%Y')
    current_month = datetime.now().strftime('%m')
    
    base_directory = config['base_directory']
    filename = config['filename']
    
    default_directory = os.path.join(base_directory, current_year)
    default_file_path = os.path.join(default_directory, current_month, filename)
    
    if len(args) == 0:
        file_path = default_file_path
    elif len(args) == 1:
        month = args[0].zfill(2)
        file_path = os.path.join(default_directory, month, filename)
    elif len(args) == 2:
        file_path = args[0]
    else:
        raise ValueError(f"Invalid arguments. Usage: <{script_name}> [<month_number>] <path_to_json_file>")
    
    return file_path

def get_file_paths(config, args=[]):
    args, script_name, _ = get_script_info(args)
    
    current_year = datetime.now().strftime('%Y')
    current_month = datetime.now().strftime('%m')
    
    base_directory = config['base_directory']
    filename_1 = config['filename_1']
    filename_2 = config['filename_2']
    
    default_directory = os.path.join(base_directory, current_year)
    default_file_1_path = os.path.join(default_directory, current_month, filename_1)
    default_file_2_path = os.path.join(default_directory, current_month, filename_2)
    
    if len(args) == 0:
        file_1_path = default_file_1_path
        file_2_path = default_file_2_path
    elif len(args) == 1:
        month = args[0].zfill(2)
        file_1_path = os.path.join(default_directory, month, filename_1)
        file_2_path = os.path.join(default_directory, month, filename_2)
    elif len(args) == 2:
        file_1_path = args[0]
        file_2_path = args[1]
    else:
        raise ValueError(f"Invalid arguments. Usage: <{script_name}> [<month_number>] <path_to_input_json_file> <path_to_output_json_file>")
    
    return file_1_path, file_2_path
