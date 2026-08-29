#!/usr/bin/env python3
import argparse,json,subprocess,sys,shutil
PRESETS={"shorts":{"max_duration":65,"min_width":720,"min_height":1280},"landscape":{"min_width":1280,"min_height":720}}
def probe(path):
 if not shutil.which("ffprobe"): raise RuntimeError("ffprobe not found")
 cmd=["ffprobe","-v","error","-show_streams","-show_format","-of","json",path]
 return json.loads(subprocess.check_output(cmd,text=True))
def inspect(data,preset=None):
 vids=[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]
 auds=[s for s in data.get("streams",[]) if s.get("codec_type")=="audio"]
 fmt=data.get("format",{}); out={"ok":True,"checks":[],"summary":{}}
 dur=float(fmt.get("duration") or 0); out["summary"]["duration_sec"]=round(dur,3)
 if vids:
  v=vids[0]; w=int(v.get("width") or 0); h=int(v.get("height") or 0)
  out["summary"].update({"video_codec":v.get("codec_name"),"width":w,"height":h,"fps":v.get("avg_frame_rate")})
 else: out["checks"].append({"name":"video_stream","pass":False,"detail":"video stream missing"}); out["ok"]=False
 if auds:
  a=auds[0]; out["summary"].update({"audio_codec":a.get("codec_name"),"sample_rate":a.get("sample_rate"),"channels":a.get("channels")})
 else: out["checks"].append({"name":"audio_stream","pass":False,"detail":"audio stream missing"}); out["ok"]=False
 if preset and vids:
  rule=PRESETS[preset]; v=vids[0]; w=int(v.get("width") or 0); h=int(v.get("height") or 0)
  for key,label,val in [("min_width","width",w),("min_height","height",h)]:
   if key in rule:
    ok=val>=rule[key]; out["checks"].append({"name":label,"pass":ok,"detail":f"{val} >= {rule[key]}"}); out["ok"] &= ok
  if "max_duration" in rule:
   ok=dur<=rule["max_duration"]; out["checks"].append({"name":"duration","pass":ok,"detail":f"{dur:.2f}s <= {rule['max_duration']}s"}); out["ok"] &= ok
 return out
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--preset",choices=PRESETS); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
 try:r=inspect(probe(a.path),a.preset)
 except Exception as e: print(f"ERROR: {e}",file=sys.stderr); return 2
 print(json.dumps(r,ensure_ascii=False,indent=2) if a.json else "\n".join([f"OK: {r['ok']}",*(f"{k}: {v}" for k,v in r['summary'].items()),*(f"{'PASS' if c['pass'] else 'FAIL'} {c['name']}: {c['detail']}" for c in r['checks'])])); return 0 if r["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
