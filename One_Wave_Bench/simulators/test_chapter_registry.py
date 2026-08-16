import unittest

from chapter_registry import Coverage, REGISTRY, coverage_counts, validate_registry


class ChapterRegistryTests(unittest.TestCase):
    def test_registry_is_valid(self):
        validate_registry()

    def test_every_current_science_chapter_is_registered(self):
        self.assertEqual(len(REGISTRY), 23)

    def test_every_chapter_declares_motion_and_interaction(self):
        self.assertTrue(all(item.motions and item.interactions for item in REGISTRY))

    def test_every_chapter_declares_gray_control(self):
        self.assertTrue(all(item.gray_control for item in REGISTRY))

    def test_coverage_count_matches_registry(self):
        self.assertEqual(sum(coverage_counts().values()), len(REGISTRY))

    def test_unbuilt_chapters_are_not_mislabeled(self):
        self.assertTrue(all(item.coverage is Coverage.PLANNED for item in REGISTRY if item.engine == "UNBUILT"))


if __name__ == "__main__":
    unittest.main()

