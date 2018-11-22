import unittest
import numpy as np
import math
import warnings

import ps5

class TestPS5(unittest.TestCase):

    def test_linear_regression(self):
        #simple y = x case
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [1,2,3,4,5,6,7,8,9,10]
        (m, b) = ps5.linear_regression(x, y)
        self.assertEqual(m, 1, "Calculated slope is incorrect")
        self.assertEqual(b, 0, "Calculated intercept is incorrect")

        #y = 5x - 3 case
        x = [-5, -3, -1, 1, 2, 6, 10]
        y = [-28, -18, -8, 2, 7, 27, 47]
        (m, b) = ps5.linear_regression(x, y)
        self.assertEqual(m, 5, "Calculated slope is incorrect")
        self.assertEqual(b, -3, "Calculated intercept is incorrect")

        #not exact line case - also tests for float handling
        x = [0,1,2,3,4,5,6,7,8,9,10,11]
        y = [-10,2,1,5,12,13,15,14,19,25,30,29]
        (m, b) = ps5.linear_regression(x, y)
        self.assertTrue(math.isclose(3.241, m, rel_tol=1e-3), "Calculated slope is incorrect")
        self.assertTrue(math.isclose(-4.910, b, rel_tol=1e-3), "Calculated intercept is incorrect")


    def test_evaluate_squared_error(self):
        #easy case
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [1,2,3,4,5,6,7,8,9,10]
        m = 1
        b = 0
        sqe = ps5.evaluate_squared_error(x, y, m ,b)
        self.assertEqual(sqe, 0, "Squared Error incorrect")

        #interesting case
        x = [0,1,2,3,4,5,6,7,8,9,10,11]
        y = [-10,2,1,5,12,13,15,14,19,25,30,29]
        m = 3
        b = -5
        sqe = ps5.evaluate_squared_error(x, y, m ,b)
        self.assertEqual(sqe, 119, "Squared Error incorrect")


    def test_generate_models(self):
        degs_msg = "generate_models should return one model for each given degree"
        list_type_msg = "generate_models should return a list of models"
        array_type_msg = "each model returned by generate_models should be of type np.array"
        coefficient_mismatch = "coefficients of returned model are not as expected"

        # simple y = x case.
        x = np.array(range(50))
        y = np.array(range(50))
        degrees = [1]
        models = ps5.generate_models(x, y, degrees)

        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        self.assertIsInstance(models[0], np.ndarray, array_type_msg)
        self.assertListEqual(list(models[0]), list(np.polyfit(x, y, 1)), coefficient_mismatch)

        # two models for y = 2x case
        y = np.array(range(0,100,2))
        degrees = [1, 2]
        models = ps5.generate_models(x, y, degrees)
        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        for m in models:
            self.assertIsInstance(m, np.ndarray, array_type_msg)
        for i in range(2):
            self.assertListEqual(list(models[i]), list(np.polyfit(x,y, degrees[i])), coefficient_mismatch)

        # three models
        degrees = [1,2,20]
        models = ps5.generate_models(x, y, degrees)
        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        for m in models:
            self.assertIsInstance(m, np.ndarray, array_type_msg)
        for i in range(3):
            self.assertListEqual(list(models[i]), list(np.polyfit(x,y, degrees[i])), coefficient_mismatch)


    def test_gen_cities_avg(self):
        # test for just one city
        climate = ps5.Dataset('data.csv')
        test_years = np.array(ps5.TESTING_INTERVAL)
        result = ps5.gen_cities_avg(climate, ['SEATTLE'], test_years)
        correct = [10.58684932, 11.28319672, 12.10643836, 12.82917808, 13.13178082, 12.50054645]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index])
            self.assertTrue(good_enough, "City averages do not match expected results")

        # national avg check (all cities)
        result = ps5.gen_cities_avg(climate, ps5.CITIES, test_years)
        correct = [ 16.46957462, 17.17387834, 16.25620043, 16.47222062, 17.17817592, 17.19825999]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index])
            self.assertTrue(good_enough, "City averages do not match expected results")

        # two-city check
        result = ps5.gen_cities_avg(climate, ['TAMPA', 'DALLAS'], test_years)
        correct = [ 22.03910959, 22.27206284, 21.31136986, 20.88123288, 22.07794521, 22.18155738]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index])
            self.assertTrue(good_enough, "City averages do not match expected results")

    def test_rmse(self):
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        result = ps5.rmse(np.array(y), np.array(estimate))
        correct = 35.8515457593
        self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

        y = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        result = ps5.rmse(np.array(y), np.array(estimate))
        correct = 40.513372278
        self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

    def test_find_interval(self):
        # Test 1: Existing positive and negative slope intervals on city data
        temp = ps5.Dataset('data.csv')
        test_years = np.array(range(1961, 2016))
        yearly_temps = ps5.gen_cities_avg(temp, ['PORTLAND'], test_years)

        result_neg = ps5.find_interval(test_years, yearly_temps, 20, False)
        correct_start = 31
        correct_end = 51
        self.assertIsNotNone(result_neg, "Returned None, but valid interval exists.")
        self.assertEqual(correct_start, result_neg[0], "Start year incorrect")
        self.assertEqual(correct_end, result_neg[1], "End year incorrect")

        result_pos = ps5.find_interval(test_years, yearly_temps, 20, True)
        correct_start = 15
        correct_end = 35
        self.assertIsNotNone(result_pos, "Returned None, but valid interval exists.")
        self.assertEqual(correct_start, result_pos[0], "Start year incorrect")
        self.assertEqual(correct_end, result_pos[1], "End year incorrect")

        # Test 2: y = 2x
        x = np.array(range(50))
        y = np.array(range(0,100,2))
        result_pos = ps5.find_interval(x, y, len(x)//2, True)
        result_neg = ps5.find_interval(x, y, len(x)//2, False)
        pos_correct_start = len(x)//2
        pos_correct_end = len(x)

        self.assertIsNone(result_neg, "Returned an interval, but should be None.")

        self.assertIsNotNone(result_pos, "Returned None, but valid interval exists.")
        self.assertEqual(pos_correct_start, result_pos[0], "Start year incorrect")
        self.assertEqual(pos_correct_end, result_pos[1], "End year incorrect")

        # Test 3: y = -2x
        x = np.array(range(50))
        y = np.array(range(100,0,-2))
        result_pos = ps5.find_interval(x, y, len(x)//2, True)
        result_neg = ps5.find_interval(x, y, len(x)//2, False)
        neg_correct_start = len(x)//2
        neg_correct_end = len(x)

        self.assertIsNone(result_pos, "Returned an interval, but should be None.")

        self.assertIsNotNone(result_neg, "Returned None, but valid interval exists.")
        self.assertEqual(neg_correct_start, result_neg[0], "Start year incorrect")
        self.assertEqual(neg_correct_end, result_neg[1], "End year incorrect")


if __name__ == '__main__':
    # Run the tests and print verbose output to stderr.
    warnings.simplefilter('ignore', np.RankWarning)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS5))
    unittest.TextTestRunner(verbosity=2).run(suite)
