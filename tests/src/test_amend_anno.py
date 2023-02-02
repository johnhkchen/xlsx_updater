# Amend Annotation Tests
# Expected Usage: python3 src/amend_anno.py
#
# Applies fixes to annotation files
#
# Input: Annotation File (xlsx)
# Input Path: 'input/xlsx'
#
# Output: Updated Annotation File (xlsx)
# Output Path: 'output/xlsx'

from amend_annotation import amend_annotation


def test_quality_check_method_available():
    assert callable(amend_annotation)
