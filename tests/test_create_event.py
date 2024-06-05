import unittest
from create_event import main

class TestCreateEvent(unittest.TestCase):
    def test_main(self):
        # Test if the main function runs without error
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {e}")

if __name__ == '__main__':
    unittest.main()