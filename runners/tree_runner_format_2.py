from hierarchy_manager.tree_hierarchy_manager import TreeHierarchyManagerFormatTwo


path = '/Users/oamar/Documents/Interviews/YotpoHomeAsssignment/data/hierarchy.txt'
hm = TreeHierarchyManagerFormatTwo(hierarchy_path=path)

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

extracted_labels, specific_labels, chosen_label = hm.detect_labels("bakery and cookies omer amar cakes")
print(f'extracted labels: {extracted_labels}, '
      f'specific labels: {specific_labels}, '
      f'chosen label: {chosen_label}')
