import unittest
import numpy as np
from DimondPricePrediction.source.DimondPricePrediction.components.model_trainer import ModelTrainer

class TestModelTrainer(unittest.TestCase):
    def test_model_training(self):
        train_array = np.array([
            [0.23, 'Ideal', 'E', 'SI2', 61.5, 55, 3.95, 3.98, 2.43, 326],
            [0.21, 'Premium', 'E', 'SI1', 59.8, 61, 3.89, 3.84, 2.31, 326],
        ], dtype=object)
        test_array = np.array([
            [0.23, 'Good', 'E', 'VS1', 63.3, 53, 3.85, 3.92, 2.48, 327],
        ], dtype=object)
        trainer = ModelTrainer()
        try:
            trainer.initate_model_training(train_array, test_array)
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main() 