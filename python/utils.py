def read_folder_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()
