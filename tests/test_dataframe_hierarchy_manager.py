from unittest import TestCase
from hierarchy_manager.dataframe_hierarchy_manager import DataFrameHierarchyManager


class TestDataframeHierarchyManager(TestCase):

    _test_hierarchy_path = 'data/test_hierarchy.txt'
    _thm = DataFrameHierarchyManager(hierarchy_path=_test_hierarchy_path)

    def test_detect_labels(self):
        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies and water')
        extracted_labels = set(extracted_labels)
        specific_labels = set(specific_labels)
        self.assertSetEqual(extracted_labels, {'cookies', 'water'})
        self.assertSetEqual(specific_labels, {'cookies', 'water'})
        self.assertIsNone(chosen_label)

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies water')
        extracted_labels = set(extracted_labels)
        specific_labels = set(specific_labels)
        self.assertSetEqual(extracted_labels, {'cookies', 'water'})
        self.assertSetEqual(specific_labels, {'cookies', 'water'})
        self.assertIsNone(chosen_label)

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('broths blah blah blah cookies')
        extracted_labels = set(extracted_labels)
        specific_labels = set(specific_labels)
        self.assertSetEqual(extracted_labels, {'broths', 'cookies'})
        self.assertSetEqual(specific_labels, {'broths', 'cookies'})
        self.assertEqual(chosen_label, 'food')

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('cookies and bakery')
        extracted_labels = set(extracted_labels)
        self.assertSetEqual(extracted_labels, {'cookies', 'bakery'})
        self.assertListEqual(specific_labels, ['cookies'])
        self.assertEqual(chosen_label, 'cookies')

        extracted_labels, specific_labels, chosen_label = self._thm.detect_labels('delicious cookies')
        self.assertListEqual(extracted_labels, ['cookies'])
        self.assertListEqual(specific_labels, ['cookies'])
        self.assertEqual(chosen_label, 'cookies')
