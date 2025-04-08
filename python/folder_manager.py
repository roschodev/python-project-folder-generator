import os


class FolderManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
    

    def create_folders(self, lines, project, path):
        base_path = os.path.join(path, f"{project.code}_{project.location}_{project.name}_{project.client}")
        print(base_path)
        os.mkdir(base_path)       
        os.chdir(base_path) 
        current_indent_level = 0
        path_stack = [base_path]
        
      
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Ignore empty lines
                indent_level = len(line) - len(stripped_line)
                folder_name = stripped_line.strip()

                # Adjust the path stack based on indentation (nesting level)
                if indent_level > current_indent_level:
                    path_stack.append(os.path.join(path_stack[-1], folder_name))
                elif indent_level < current_indent_level:
                    path_stack = path_stack[:indent_level // 4 + 1]  # Adjust the path stack
                    path_stack.append(os.path.join(path_stack[-1], folder_name))
                else:
                    path_stack[-1] = os.path.join(os.path.dirname(path_stack[-1]), folder_name)

                current_indent_level = indent_level

                # Create the directory
                os.makedirs(path_stack[-1], exist_ok=True)
