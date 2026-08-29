# Creator Delivery Inspector

ffprobe を使って動画/音声納品物の基本QAを行うCLI。Shorts/縦動画と横動画の簡易プリセット、フォルダ一括manifest出力に対応。

```bash
python3 creator_delivery_inspector.py sample.mp4 --preset shorts --json
python3 creator_delivery_inspector.py ./delivery --manifest delivery.csv
```

- ファイルを外部送信しません
- ffprobe が必要です
- CSVはExcelで開きやすいUTF-8 BOM付き
- MIT License
