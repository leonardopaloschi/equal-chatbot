import unittest
from unittest.mock import patch
from generator import preprocess_texts, build_and_train_model

class Tests(unittest.TestCase):

    def test_preprocess_texts(self):
        self.assertEqual(preprocess_texts(['Hello     World!']), ["Hello World!"])
        self.assertEqual(preprocess_texts(['Hello     World!', "AAAAA BBBBB        C"]), ["Hello World!", "AAAAA BBBBB C"])
        self.assertEqual(preprocess_texts(["     1 2 3     "]), ["1 2 3"])
        self.assertEqual(preprocess_texts(["This     is      a    test  "]), ["This is a test"])

    @patch('generator.get_data')
    def test_build_and_train_model(self, mock_get_data):
        mock_get_data.return_value = ["Sample text for training."]
        try:
            build_and_train_model(mock_get_data.return_value)
        except Exception as e:
            self.fail(f"build_and_train_model raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
