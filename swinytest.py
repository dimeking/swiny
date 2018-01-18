import unittest
from swiny import to_piglatin
from swiny import to_english
 
class TestSwiny(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_topiglatin_truelove(self):
        self.assertEqual(to_piglatin({},"True Love"), "uetray ovelay")
 
    def test_topiglatin_wakeup(self):
        self.assertEqual(to_piglatin({},"wake up"), "akeway upyay")
 
    def test_frompiglatin_truelove(self):
        self.assertEqual(to_english({},"uetray ovelay"), "true love")
 
    def test_frompiglatin_wakeup(self):
        self.assertEqual(to_english({},"akeway upyay"), "wake up")
 
if __name__ == '__main__':
    unittest.main()