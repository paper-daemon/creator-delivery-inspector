# Creator Delivery Inspector

ffprobe を使って動画/音声納品物の基本QAを行うCLI。Shorts/縦動画と横動画の簡易プリセット、フォルダ一括manifest出力に対応。

## Quick start

```bash
python3 creator_delivery_inspector.py sample.mp4 --preset shorts --json
python3 creator_delivery_inspector.py ./delivery --manifest delivery.csv
```

## Batch manifest

複数ファイルを走査すると、1行1ファイルのCSVにまとめます。

```text
file,ok,duration_sec,width,height,video_codec,audio_codec,sample_rate,channels,error
land.mp4,True,2.0,1920,1080,mpeg4,aac,44100,1,
short.mp4,True,2.0,1080,1920,mpeg4,aac,44100,1,
```

- ファイルを外部送信しません
- ffprobe が必要です
- CSVはExcelで開きやすいUTF-8 BOM付き
- 個別ファイルのprobe失敗もbatch全体を止めず`error`列へ残します
- durationはfiniteかつ0以上だけを正常メタデータとして扱います
- [duration metadataの検証境界](docs/duration-metadata-boundary.md)
- MIT License

## 任せたい場合

CLIを自分で回すのではなく、動画・音声の納品前QAとCSV一覧化をまとめて依頼したい場合は、ココナラでも受け付けています。

https://coconala.com/services/3914156

無料ツールの機能はサービス購入なしでもそのまま使えます。

## Duration metadata boundary

`format.duration` が無い場合はvideo/audio streamのdurationへfallbackします。どこにも有限・非負のdurationが無い場合は `0秒` とみなしてPASSせず、検査エラーとしてfail-closedにします。
