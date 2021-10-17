import unittest
import godel

class GodelTestCase(unittest.TestCase):
    def test_godel(self):
        self.assertEqual(465807801831494163751710, godel.pm_lisp_to_godel_num(['=', ['0', '0']]))
        self.assertEqual(['next', '0'], godel.godel_num_to_pm_lisp(godel.pm_lisp_to_godel_num(['next', '0'])))

if __name__ == '__main__':
    unittest.main()
