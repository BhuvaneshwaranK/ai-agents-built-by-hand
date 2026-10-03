import unittest

from bob.shop import check_repair_status


class NotFoundTest(unittest.TestCase):
    def test_unknown_order_is_reported(self):
        result = check_repair_status("R-9999")
        self.assertIn("No repair found", result)


unittest.main()
