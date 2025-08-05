import unittest
from src.services.xml_parser import XmlParser

class TestXmlParser(unittest.TestCase):

    def setUp(self):
        self.parser = XmlParser()

    def test_parse_valid_xml(self):
        xml_content = """
        <xml>
            <article id="1" name="Test Article" idOficio="123" pubName="Test Publication" artType="Type" pubDate="2023-01-01" artClass="Class" artCategory="Category" artSize="Size" artNotes="Notes" numberPage="1" pdfPage="1" editionNumber="1" highlightType="Type" highlightPriority="1" highlight="Highlight" highlightimage="Image" highlightimagename="ImageName" idMateria="1">
                <body>
                    <Identifica><![CDATA[Identifier]]></Identifica>
                    <Data><![CDATA[2023-01-01]]></Data>
                    <Ementa />
                    <Titulo>Test Title</Titulo>
                    <SubTitulo>Test Subtitle</SubTitulo>
                    <Texto><![CDATA[This is a test text.]]></Texto>
                </body>
                <Midias />
            </article>
        </xml>
        """
        result = self.parser.parse(xml_content)
        expected_result = {
            "id": "1",
            "name": "Test Article",
            "pubDate": "2023-01-01",
            "title": "Test Title",
            "subtitle": "Test Subtitle",
            "text": "This is a test text."
        }
        self.assertEqual(result, expected_result)

    def test_parse_invalid_xml(self):
        invalid_xml_content = "<xml><article></xml>"
        with self.assertRaises(Exception):
            self.parser.parse(invalid_xml_content)

    def test_extract_metadata(self):
        xml_content = """
        <xml>
            <article id="2" name="Another Article" pubDate="2023-01-02">
                <body>
                    <Identifica><![CDATA[Another Identifier]]></Identifica>
                    <Data><![CDATA[2023-01-02]]></Data>
                    <Titulo>Another Title</Titulo>
                    <Texto><![CDATA[Another test text.]]></Texto>
                </body>
            </article>
        </xml>
        """
        result = self.parser.extract_metadata(xml_content)
        expected_metadata = {
            "id": "2",
            "pubDate": "2023-01-02",
            "title": "Another Title",
            "text": "Another test text."
        }
        self.assertEqual(result, expected_metadata)

if __name__ == '__main__':
    unittest.main()