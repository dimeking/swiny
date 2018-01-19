import unittest
from swiny import to_piglatin
from swiny import to_gibberish
 
class TestSwiny(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_topiglatin_truelove(self):
        self.assertEqual(to_piglatin({},"True Love"), "uetray ovelay")
 
    def test_topiglatin_wakeup(self):
        self.assertEqual(to_piglatin({},"wake up"), "akeway upyay")
 
    def test_togibberish_truelove(self):
        self.assertEqual(to_gibberish({},"true love"), "tridigue lidigove")
 
    def test_togibberish_wakeup(self):
        self.assertEqual(to_gibberish({},"wake up"), "widigake idigup")
 
if __name__ == '__main__':
    unittest.main()