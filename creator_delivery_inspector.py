#!/usr/bin/env python3
import argparse,csv,json,subprocess,sys,shutil,math
from pathlib import Path
PRESETS={"shorts":{"max_duration":65,"min_width":720,"min_height":1280},"landscape":{"min_width":1280,"min_height":720}}
MEDIA_EXTS={".mp4",".mov",".mkv",".webm",".m4v",".avi",".mp3",".wav",".m4a",".aac",".flac",".ogg"}
def probe(path):
 if not shutil.which("ffprobe"): raise RuntimeError("ffprobe not found")
 cmd=["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]
 return json.loads(subprocess.check_output(cmd,text=True))
def inspect(data,preset=None):
 vids=[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]
 auds=[s for s in data.get("streams",[]) if s.get("codec_type")=="audio"]
 fmt=data.get("format",{}); out={"ok":True,"checks":[],"summary":{}}
 dur=float(fmt.get("duration") or 0)
 if not math.isfinite(dur) or dur < 0: raise ValueError("duration must be a finite non-negative number")
 out["summary"]["duration_sec"]=round(dur,3)
 if vids:
  v=vids[0]; w=int(v.get("width") or 0); h=int(v.get("height") or 0)
  out["summary"].update({"video_codec":v.get("codec_name"),"width":w,"height":h,"fps":v.get("avg_frame_rate")})
 elif preset:
  out["checks"].append({"name":"video_stream","pass":False,"detail":"video stream missing"}); out["ok"]=False
 if auds:
  a=auds[0]; out["summary"].update({"audio_codec":a.get("codec_name"),"sample_rate":a.get("sample_rate"),"channels":a.get("channels")})
 else:
  out["summary"].update({"audio_codec":None,"sample_rate":None,"channels":None})
 if preset and vids:
  rule=PRESETS[preset]; v=vids[0]; w=int(v.get("width") or 0); h=int(v.get("height") or 0)
  for key,label,val in [("min_width","width",w),("min_height","height",h)]:
   if key in rule:
    ok=val>=rule[key]; out["checks"].append({"name":label,"pass":ok,"detail":f"{val} >= {rule[key]}"}); out["ok"] &= ok
  if "max_duration" in rule:
   ok=dur<=rule["max_duration"]; out["checks"].append({"name":"duration","pass":ok,"detail":f"{dur:.2f}s <= {rule['max_duration']}s"}); out["ok"] &= ok
 return out
def media_files(path):
 p=Path(path)
 if p.is_file(): return [p]
 if not p.is_dir(): raise FileNotFoundError(path)
 return sorted(x for x in p.rglob('*') if x.is_file() and x.suffix.lower() in MEDIA_EXTS)
def build_manifest(path,preset=None):
 rows=[]
 for f in media_files(path):
  try:
   r=inspect(probe(f),preset); s=r['summary']
   rows.append({"file":str(f),"ok":r['ok'],"duration_sec":s.get("duration_sec"),"width":s.get("width"),"height":s.get("height"),"video_codec":s.get("video_codec"),"audio_codec":s.get("audio_codec"),"sample_rate":s.get("sample_rate"),"channels":s.get("channels"),"error":""})
  except Exception as e:
   rows.append({"file":str(f),"ok":False,"duration_sec":"","width":"","height":"","video_codec":"","audio_codec":"","sample_rate":"","channels":"","error":str(e)})
 return rows
def write_manifest(rows,path):
 fields=["file","ok","duration_sec","width","height","video_codec","audio_codec","sample_rate","channels","error"]
 with open(path,"w",newline="",encoding="utf-8-sig") as fh:
  w=csv.DictWriter(fh,fieldnames=fields); w.writeheader(); w.writerows(rows)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--preset",choices=PRESETS); ap.add_argument("--json",action="store_true"); ap.add_argument("--manifest",help="write batch CSV manifest") ; a=ap.parse_args()
 if a.manifest or Path(a.path).is_dir():
  try: rows=build_manifest(a.path,a.preset)
  except Exception as e: print(f"ERROR: {e}",file=sys.stderr); return 2
  if a.manifest: write_manifest(rows,a.manifest)
  print(json.dumps(rows,ensure_ascii=False,indent=2) if a.json else f"files={len(rows)} ok={sum(bool(r['ok']) for r in rows)} fail={sum(not bool(r['ok']) for r in rows)}" )
  return 0 if rows and all(bool(r['ok']) for r in rows) else 1
 try:r=inspect(probe(a.path),a.preset)
 except Exception as e: print(f"ERROR: {e}",file=sys.stderr); return 2
 print(json.dumps(r,ensure_ascii=False,indent=2) if a.json else "\n".join([f"OK: {r['ok']}",*(f"{k}: {v}" for k,v in r['summary'].items()),*(f"{'PASS' if c['pass'] else 'FAIL'} {c['name']}: {c['detail']}" for c in r['checks'])])); return 0 if r["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
