import os

IGNORE = {
    "folders": {".git", "node_modules", "dist", "__pycache__", "venv", ".venv", "env", "scripts.egg-info"},
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
        
        for i, item in enumerate(items):
            full_path = os.path.join(path, item)
            
            if self._should_ignore(full_path, item):
                continue
                
            is_last = i == len(items) - 1
            line = prefix + ("└── " if is_last else "├── ") + item
            output.append(line)
            
            if os.path.isdir(full_path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                output.append(self._generate_structure(full_path, new_prefix))
        
        return "\n".join(output)
    
    def _should_ignore(self, full_path: str, item: str) -> bool:
        if item in IGNORE["folders"] and os.path.isdir(full_path):
            return True
        if item in IGNORE["files"] and os.path.isfile(full_path):
            return True
        return False