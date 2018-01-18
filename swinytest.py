import unittest
from swiny import to_piglatin
 
class TestSwiny(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_piglatin_truelove(self):
        self.assertEqual(to_piglatin({},"True Love"), "ue tray ove lay")
 
    def test_piglatin_wakeup(self):
        self.assertEqual(to_piglatin({},"wake up"), "ake way up yay")
 
if __name__ == '__main__':
    unittest.main()