import os
import zipfile
import unittest
from src.services.zip_extractor import ZipExtractor

class TestZipExtractor(unittest.TestCase):

    def setUp(self):
        self.zip_extractor = ZipExtractor()
        self.test_zip_path = 'test_files/test.zip'  # Path to a test ZIP file
        self.extract_path = 'test_files/extracted'  # Path to extract files

        # Create a test ZIP file for testing
        with zipfile.ZipFile(self.test_zip_path, 'w') as zipf:
            zipf.writestr('test1.xml', '<xml><article id="1"></article></xml>')
            zipf.writestr('test2.xml', '<xml><article id="2"></article></xml>')

    def tearDown(self):
        # Clean up the created test files
        if os.path.exists(self.extract_path):
            for file in os.listdir(self.extract_path):
                os.remove(os.path.join(self.extract_path, file))
            os.rmdir(self.extract_path)
        if os.path.exists(self.test_zip_path):
            os.remove(self.test_zip_path)

    def test_extract_zip(self):
        extracted_files = self.zip_extractor.extract_zip(self.test_zip_path, self.extract_path)
        self.assertTrue(len(extracted_files) > 0)
        self.assertIn('test1.xml', extracted_files)
        self.assertIn('test2.xml', extracted_files)

    def test_extract_nonexistent_zip(self):
        with self.assertRaises(FileNotFoundError):
            self.zip_extractor.extract_zip('nonexistent.zip', self.extract_path)

if __name__ == '__main__':
    unittest.main()