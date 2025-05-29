import os
import tempfile
from zipfile import ZipFile
import subprocess

class CodebaseExtractor:
    def __init__(self, path_or_url):
        self.path_or_url = path_or_url
        self.temp_dir = tempfile.mkdtemp()
        self.file_paths = []

    def extract(self):
        if self.path_or_url.endswith('.zip') and os.path.exists(self.path_or_url):
            with ZipFile(self.path_or_url, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
        elif self.path_or_url.startswith('http') and 'github.com' in self.path_or_url:
            subprocess.run(['git', 'clone', self.path_or_url, self.temp_dir], check=True)
        else:
            raise ValueError('Input must be a local zip file or GitHub repo URL')
        for root, _, files in os.walk(self.temp_dir):
            if '__MACOSX' in root:
                continue
            for f in files:
                if f.endswith(('.py', '.java', '.kt')):
                    self.file_paths.append(os.path.join(root, f))
        return self.file_paths, self.temp_dir

    def cleanup(self):
        import shutil
        shutil.rmtree(self.temp_dir)
