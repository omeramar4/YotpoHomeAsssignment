import os
from pathlib import Path
from hierarchy_manager.dataframe_hierarchy_manager import DataFrameHierarchyManager


path = os.path.join(Path(os.getcwd()).parent, 'data/hierarchy.txt')
hm = DataFrameHierarchyManager(hierarchy_path=path)

extracted_labels, specific_labels, chosen_label = hm.detect_labels('yotpo')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels('my tasty bread')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels('board games')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels('coffee and tea')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels('cookies and candy')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels('bread and water')
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')

extracted_labels, specific_labels, chosen_label = hm.detect_labels("bakery and cookies and cakes")
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')
