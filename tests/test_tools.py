from unittest import TestCase
from ec2ools.tools import PH_CONST, INLINE_DELIM, inline_item
# from ec2ools.tools import inline_item
__author__ = 'yairgrosu'

TEST_PH_CONST = PH_CONST
TEST_DELIM = '=='


class TestInline_item(TestCase):
    def test_inline_item_start(self):
        data = "Item"
        start_pos = "%s%s" % (data, TEST_PH_CONST)
        star_pos_item = inline_item(start_pos, None)
        self.assertEqual(data, star_pos_item)

        ph = 'PH'
        star_pos_item = inline_item(start_pos, ph)
        self.assertEqual(data + INLINE_DELIM + ph, star_pos_item)

    def test_inline_item_start(self):
        data = "Item"
        start_pos = "%s%s" % (data, TEST_PH_CONST)
        star_pos_item = inline_item(start_pos, None, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(data, star_pos_item)

        ph = 'PH'
        star_pos_item = inline_item(start_pos, ph, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(data + TEST_DELIM + ph, star_pos_item)


    def test_inline_item_end(self):
        data = "Item"
        end_pos = "%s%s" % (TEST_PH_CONST, data)
        star_pos_item = inline_item(end_pos, None, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(data, star_pos_item)

        ph = 'PH'
        star_pos_item = inline_item(end_pos, ph, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(ph + TEST_DELIM + data, star_pos_item)

    def test_inline_item_middle(self):
        data = "Item"
        end_pos = "%s%s%s" % (data, TEST_PH_CONST, data)
        star_pos_item = inline_item(end_pos, None, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(data + data, star_pos_item)

        ph = 'PH'
        star_pos_item = inline_item(end_pos, ph, TEST_DELIM, TEST_PH_CONST)
        self.assertEqual(data + TEST_DELIM + ph + TEST_DELIM + data, star_pos_item)
