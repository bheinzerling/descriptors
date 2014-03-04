import unittest
from dirproc.tests.test_dirproc import DirectoryProcessorTest


loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTest(loader.loadTestsFromTestCase(DirectoryProcessorTest))
unittest.TextTestRunner().run(suite)
