from os import path
import sys
import inspect
import unittest
# to import the retrieve_assembly_metadata
currentdir = path.dirname(path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = path.dirname(currentdir)
sys.path.insert(0, parentdir)
from retrieve_assembly_metadata import parse_args


class TestParser(unittest.TestCase):
    def test_single_accession(self):
        self.assertEqual(parse_args(['a']).accession, ['a'])

    def test_mutiple_accessions(self):
        self.assertEqual(parse_args(['a', 'b', 'c']).accession, ['a', 'b', 'c'])

    def test_single_file(self):
        self.assertEqual(parse_args(['-f', 'a']).file, 'a')
        self.assertEqual(parse_args(['-f', 'a']).accession, [])

    def test_empty_input(self):
        self.assertEqual(parse_args([]), None)

    def test_invalid_input(self):
        self.assertEqual(parse_args(['a', '-f']), None)
        self.assertEqual(parse_args(['-f', 'a', 'b']), None)
        self.assertEqual(parse_args(['-c', '1']), None)

    def test_one_core(self):
        self.assertEqual(parse_args(['a', '-c', '1']).core, 1)


if __name__ == '__main__':
    unittest.main()
