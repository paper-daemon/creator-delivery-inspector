import unittest
from creator_delivery_inspector import inspect
class T(unittest.TestCase):
 def test_shorts_pass(self):
  d={"format":{"duration":"59"},"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920,"avg_frame_rate":"30/1"},{"codec_type":"audio","codec_name":"aac","sample_rate":"48000","channels":2}]}
  self.assertTrue(inspect(d,"shorts")["ok"])
 def test_shorts_fail_landscape(self):
  d={"format":{"duration":"70"},"streams":[{"codec_type":"video","width":1920,"height":1080},{"codec_type":"audio"}]}
  self.assertFalse(inspect(d,"shorts")["ok"])
if __name__=="__main__": unittest.main()
