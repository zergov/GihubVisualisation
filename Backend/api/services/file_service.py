class FileService:
    def __init__(self):
        self.file_type_mapping = {
            # Source code files
            '.py': 'source',
            '.java': 'source',
            '.c': 'source',
            '.cpp': 'source',
            '.h': 'source',
            '.html': 'source',
            '.js': 'source',
            '.tsx': 'source',
            '.ts': 'source',
            '.css': 'source',
            '.go': 'source',
            '.rb': 'source',
            '.php': 'source',

            # Test files
            '.test.js': 'test',
            '.spec.js': 'test',
            '.test.ts': 'test',
            '.spec.ts': 'test',
            '.test.py': 'test',
            '.spec.py': 'test',

            # Database files
            '.sql': 'database',
            '.db': 'database',
            '.sqlite': 'database',

            # Data files
            '.json': 'data',
            '.xml': 'data',
            '.csv': 'data',

            # Documentation files
            '.md': 'documentation',
            '.txt': 'documentation',
            '.rst': 'documentation',
        }

    def get_file_type(self, file_path: str) -> str:
        extension = file_path.split('.')[-1]
        file_type = self.file_type_mapping.get(f'.{extension}', 'file')

        # Check if 'test' is in the file name or in the path
        if 'test' in file_path.lower():
            return 'test'

        return file_type
