import unittest

from bob import shop


class PromiseTests(unittest.TestCase):
    def test_booking_needs_approval(self):
        by_name = {t["name"]: t for t in shop.SHOP_TOOLS}
        self.assertTrue(by_name["book_appointment"]["needs_approval"])

    def test_public_tools_have_no_notebook(self):
        names = [t["name"] for t in shop.PUBLIC_TOOLS]
        self.assertNotIn("recall", names)
        self.assertNotIn("remember", names)


unittest.main()
