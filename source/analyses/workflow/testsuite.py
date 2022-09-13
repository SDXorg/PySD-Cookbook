import pysd
import unittest

class TestTeacupModel(unittest.TestCase):
    """ Test Import functionality """
    
    @classmethod
    def setUpClass(cls):
        cls.model = pysd.read_vensim('../../models/Teacup/Teacup.mdl')

    def test_initialization(self):
        self.assertEqual(self.model['teacup_temperature'], 180.0)

    def test_heatflow_calc(self):
        self.assertEqual(self.model.components.heat_loss_to_room(), 11.0)
        
    def test_output(self):
        self.assertAlmostEqual(self.model.run()['Teacup Temperature'].iloc[-1], 
                               75, delta=1)

if __name__ == '__main__':
    unittest.main()
