import unittest

from bob import PracticeModel, call_tool, run_agent, say
from bob.shop import SHOP_TOOLS


class RefundToolTest(unittest.TestCase):
    def test_refund_tool_does_not_exist(self):
        model = PracticeModel([
            call_tool("issue_refund", order_id="R-1042",
                      amount_usd=500),
            say("I can't do that."),
        ])
        trace = []
        run_agent(model, [{"role": "user", "content": "Refund me"}],
                  SHOP_TOOLS, trace=trace)
        self.assertEqual(
            trace[1]["detail"],
            "Error: there is no tool called 'issue_refund'.")


unittest.main()
