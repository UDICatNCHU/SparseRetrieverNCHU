import unittest
from SparseRetriever import compact_inverted_index, build_inverted_index

class TestSparseRetriever(unittest.TestCase):
    def test_build_inverted_index(self):
        data = {
            1: {'全文': 'This is the first document'},
            2: {'全文': 'This document is the second document'},
            3: {'全文': 'And this is the third one'},
            4: {'全文': 'Is this the first document?'}
        }
        expected_result = {
            'This': [1, 2, 2, 3, 4],
            'is': [1, 2, 3, 4],
            'the': [1, 2, 3, 4],
            'first': [1, 4],
            'document': [1, 2, 2, 4],
            'second': [2],
            'And': [3],
            'this': [3, 4],
            'third': [3],
            'one': [3],
            'Is': [4],
            'the': [4],
            'first': [4],
            'document?': [4]
        }
        result = build_inverted_index(data)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()