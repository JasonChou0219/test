import unittest


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]                # DECLARE data    
        result = sum(data)              # TEST the function
        self.assertEqual(result, 6)     # ASSERT the result


if __name__ == '__main__':
    unittest.main()
