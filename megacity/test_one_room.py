import os
import tempfile
import unittest

from megacity.body import LooperBody
from megacity.loop import PACKET_KEYS, Looper
from megacity.room import Room


class OneRoomLooperTests(unittest.TestCase):
    def test_wall_is_not_a_switch(self):
        loop = Looper()
        start = tuple(loop.room.avatar)
        packet = loop.step("north")
        self.assertFalse(packet["new_state_after_action"]["accepted"])
        self.assertEqual(tuple(loop.room.avatar), start)
        self.assertTrue(packet["why_this_action"].startswith("caller asked"))

    def test_body_cannot_write_the_room(self):
        room = Room()
        body = LooperBody()
        self.assertFalse(hasattr(body, "room"))
        room.act("jump")
        self.assertEqual(tuple(room.avatar), (1, 1))
        self.assertFalse(room.switch_on)

    def test_reaches_the_mark_and_keeps_every_receipt(self):
        loop = Looper()
        packets = loop.run_until_done()
        self.assertTrue(loop.body.done)
        self.assertTrue(packets[-1]["new_state_after_action"]["goal_open"])
        self.assertTrue(loop.room.switch_on)
        self.assertGreaterEqual(len(loop.body.memory), 4)
        for packet in packets:
            for key in PACKET_KEYS:
                self.assertIn(key, packet)
            self.assertIn("field", packet)
            self.assertIn("void", packet)
            self.assertIn(packet["chosen_next_action"], packet["available_choices"])

    def test_save_reload_continues_the_same_loop(self):
        original = Looper()
        original.step()
        original.step()
        twin = Looper()
        twin.step()
        twin.step()
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "room.json")
            original.save(path)
            loaded = Looper.load(path)
        self.assertEqual(loaded.room.avatar, original.room.avatar)
        self.assertEqual(loaded.room.switch_on, original.room.switch_on)
        self.assertEqual(loaded.body.memory, original.body.memory)
        self.assertEqual(loaded.step_index, original.step_index)
        again = loaded.step()
        expected = twin.step()
        self.assertEqual(again["chosen_next_action"], expected["chosen_next_action"])
        self.assertEqual(again["new_state_after_action"], expected["new_state_after_action"])
        self.assertEqual(len(loaded.body.memory), 3)


if __name__ == "__main__":
    unittest.main()
