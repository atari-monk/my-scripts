import os

IGNORE = {
    "folders": {".git", "node_modules", "dist", "__pycache__", "venv", ".venv", "env", "my_scripts.egg-info", ".pytest_cache"},
    "files": {"package-lock.json"}
}

class DirectoryTreeGenerator:
    def __init__(self, root_path: str):
        self.root_path = os.path.normpath(root_path)
        self.repo_name = os.path.basename(self.root_path)
        
    def generate(self) -> str:
        structure = self._generate_structure(self.root_path)
        return f"# File Tree of repository `{self.repo_name}`\n\n```\n{structure}\n```"
    
    def _generate_structure(self, path: str, prefix: str = "") -> str:
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return f"{prefix}└── [Permission denied]\n"
            
        output = []
        filtered_items = [item for item in items if not self._should_ignore(os.path.join(path, item), item)]
        
        for i, item in enumerate(filtered_items):
            full_path = os.path.join(path, item)
            is_last = i == len(filtered_items) - 1
            line = prefix + ("└── " if is_last else "├── ") + item
            output.append(line)
            
            if os.path.isdir(full_path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                subtree = self._generate_structure(full_path, new_prefix)
                if subtree.strip():
                    output.append(subtree)
        
        return "\n".join(output)
    
    def _should_ignore(self, full_path: str, item: str) -> bool:
        if os.path.isdir(full_path) and item in IGNORE["folders"]:
            return True
        if os.path.isfile(full_path) and item in IGNORE["files"]:
            return True
        return False