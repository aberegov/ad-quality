import unittest
from com.conversant.common.SlidingBuffer import SlidingBuffer

class SlidingBufferTestCase(unittest.TestCase):
    def setUp(self):
        self.buffer = SlidingBuffer(3)

    def tearDown(self):
        self.buffer.clear()
        del self.buffer

    def test_add_item(self):
        self.buffer.add(10)
        self.assertEqual(10, self.buffer.sum)
        self.assertEqual(10, self.buffer.total)
        self.assertEqual(0, self.buffer.archived)

    def test_add_two_items(self):
        self.buffer.add(10)
        self.buffer.add(30)
        self.assertEqual(40, self.buffer.sum)
        self.assertEqual(40, self.buffer.total)
        self.assertEqual(0, self.buffer.archived)

    def test_add_three_items(self):
        self.buffer.add(10)
        self.buffer.add(30)
        self.buffer.add(50)
        self.assertEqual(90, self.buffer.sum)
        self.assertEqual(90, self.buffer.total)
        self.assertEqual(0, self.buffer.archived)

    def test_add_four_items(self):
        self.buffer.add(10)
        self.buffer.add(30)
        self.buffer.add(50)
        self.buffer.add(70)
        self.assertEqual(150, self.buffer.sum)
        self.assertEqual(160, self.buffer.total)
        self.assertEqual(10, self.buffer.archived)

    def test_add_many_items(self):
        s = 0
        for i in range(1,11):
            self.buffer.add(i)
            s += i

        self.assertEqual(27, self.buffer.sum)
        self.assertEqual(s,  self.buffer.total)
        self.assertEquals(s - 27, self.buffer.archived)



