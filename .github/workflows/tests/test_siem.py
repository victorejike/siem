import unittest
import os
import tempfile
import sys

# Add the src 
sys.path.insert(0, os.path.join(os.path.dirname(file), '..', 'src', 'python'))

from siem_tool import EnhancedSIEM

class TestSIEMTool(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.siem = EnhancedSIEM(db_path=self.db_path)
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_ip_extraction(self):
        test_line = "2023-05-01T12:00:00 Failed login from 192.168.1.1"
        ip = self.siem.extract_ip(test_line)
        self.assertEqual(ip, "192.168.1.1")
    
    def test_no_ip_extraction(self):
        test_line = "2023-05-01T12:00:00 System started normally"
        ip = self.siem.extract_ip(test_line)
        self.assertIsNone(ip)
    
    def test_log_processing(self):
        test_line = "2023-05-01T12:00:00 Failed login from 192.168.1.1"
        result = self.siem.process_log(test_line, "test")
        self.assertIn("ip_address", result)
        self.assertEqual(result["ip_address"], "192.168.1.1")

if name == 'main':
    unittest.main()
