from unittest import TestCase
from hierarchy_manager.tree_hierarchy_manager import TreeHierarchyManagerFormatOne


class TestTreeHierarchyManager(TestCase):

    _test_hierarchy_path = 'data/test_hierarchy.txt'
    _thm = TreeHierarchyManagerFormatOne(hierarchy_path=_test_hierarchy_path)

    def test_detect_labels(self):
        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies and water')
        self.assertListEqual(extracted_labels, ['cookies', 'water'])
        self.assertListEqual(specific_labels, ['cookies', 'water'])
        self.assertIsNone(chosen_label)

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies water')
        self.assertListEqual(extracted_labels, ['cookies', 'water'])
        self.assertListEqual(specific_labels, ['cookies', 'water'])
        self.assertIsNone(chosen_label)

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('broths blah blah blah cookies')
        self.assertListEqual(extracted_labels, ['broths', 'cookies'])
        self.assertListEqual(specific_labels, ['broths', 'cookies'])
        self.assertEqual(chosen_label, 'food')

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies and bakery')
        self.assertListEqual(extracted_labels, ['cookies', 'bakery'])
        self.assertListEqual(specific_labels, ['cookies'])
        self.assertEqual(chosen_label, 'cookies')

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('delicious cookies')
        self.assertListEqual(extracted_labels, ['cookies'])
        self.assertListEqual(specific_labels, ['cookies'])
        self.assertEqual(chosen_label, 'cookies')