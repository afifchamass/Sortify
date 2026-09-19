import unittest

from app.curator.config import SETTINGS, assert_read_only
from app.curator.router import audit_capabilities


class SafetyTests(unittest.TestCase):
    def test_foundation_is_hard_read_only(self):
        self.assertFalse(SETTINGS.write_enabled)
        self.assertIsNone(assert_read_only())

    def test_capabilities_expose_no_spotify_writes(self):
        payload = audit_capabilities()
        self.assertFalse(payload["spotify_write_operations_enabled"])
        self.assertEqual("READ_ONLY", payload["mode"])
