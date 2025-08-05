class ZipExtractor:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path

    def extract_zip(self):
        import zipfile
        import os

        extracted_files = []
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(self.zip_file_path))
            extracted_files = zip_ref.namelist()
        
        return extracted_files

    def get_xml_files(self, extracted_files):
        xml_files = [file for file in extracted_files if file.endswith('.xml')]
        return xml_files