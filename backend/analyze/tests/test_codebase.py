from django.test import TestCase
from unittest.mock import patch, Mock
import os
import tempfile
import zipfile
import shutil
from ..core.codebase import CodebaseExtractor

class TestCodebaseExtractor(TestCase):
    def test_extract_zip(self):
        code = 'def foo():\n    pass\n'
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, 'foo.py')
            with open(py_file, 'w') as f:
                f.write(code)
            zip_path = os.path.join(tmpdir, 'test.zip')
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(py_file, arcname='foo.py')
            extractor = CodebaseExtractor(str(zip_path))
            files, temp_dir = extractor.extract()
            self.assertTrue(any(f.endswith('.py') for f in files))
            self.assertTrue(os.path.exists(temp_dir))
            shutil.rmtree(temp_dir)

    def test_extract_invalid_input(self):
        with self.assertRaises(ValueError):
            CodebaseExtractor('not_a_zip_or_github').extract()

