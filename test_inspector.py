import tempfile,unittest
from pathlib import Path
from creator_delivery_inspector import inspect,media_files
class T(unittest.TestCase):
 def test_shorts_pass(self):
  d={"format":{"duration":"30"},"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"x","avg_frame_rate":"30/1"},{"codec_type":"audio","codec_name":"aac","sample_rate":"48000","channels":2}]}
  self.assertTrue(inspect(d,"shorts")["ok"])
 def test_shorts_fail_landscape(self):
  d={"format":{"duration":"30"},"streams":[{"codec_type":"video","width":1920,"height":1080,"codec_name":"x","avg_frame_rate":"30/1"}]}
  self.assertFalse(inspect(d,"shorts")["ok"])
 def test_rejects_invalid_duration_metadata(self):
  for value in ("-1","NaN","inf"):
   d={"format":{"duration":value},"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"x","avg_frame_rate":"30/1"}]}
   with self.subTest(value=value):
    with self.assertRaisesRegex(ValueError,"finite non-negative"):
     inspect(d,"shorts")
 def test_missing_duration_is_not_zero_second_success(self):
  d={"format":{},"streams":[{"codec_type":"video","width":1080,"height":1920,"codec_name":"x","avg_frame_rate":"30/1"}]}
  with self.assertRaisesRegex(ValueError,"finite non-negative"):
   inspect(d,"shorts")
 def test_stream_duration_is_used_when_format_duration_is_missing(self):
  d={"format":{},"streams":[{"codec_type":"video","duration":"30","width":1080,"height":1920,"codec_name":"x","avg_frame_rate":"30/1"}]}
  r=inspect(d,"shorts")
  self.assertTrue(r["ok"])
  self.assertEqual(r["summary"]["duration_sec"],30.0)
 def test_longest_stream_duration_is_used_when_format_duration_is_missing(self):
  d={"format":{},"streams":[
   {"codec_type":"audio","duration":"10","codec_name":"aac","sample_rate":"48000","channels":2},
   {"codec_type":"video","duration":"70","width":1080,"height":1920,"codec_name":"x","avg_frame_rate":"30/1"},
  ]}
  r=inspect(d,"shorts")
  self.assertFalse(r["ok"])
  self.assertEqual(r["summary"]["duration_sec"],70.0)
 def test_media_files_filters(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td); (p/'a.mp4').write_bytes(b'x'); (p/'b.txt').write_text('x'); (p/'c.wav').write_bytes(b'x')
   self.assertEqual([x.name for x in media_files(p)],['a.mp4','c.wav'])
if __name__=='__main__': unittest.main()
