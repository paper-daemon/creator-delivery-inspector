# Duration metadata boundary

Creator Delivery Inspectorはffprobeのdurationを納品QAへ使いますが、数値へ変換できるだけでは有効な時間とは限りません。

## 再現した問題

修正前は次の値を受理していました。

- `-1` はShorts presetでも `-1 <= 65` となりPASS
- `NaN` はpreset無しだと `ok=true` のままsummaryへ残る
- `inf` もpreset無しだと `ok=true` のままsummaryへ残る

## 現在の境界

`duration` はfiniteかつ0以上だけを受理します。負値、`NaN`、`inf` は `ValueError` として扱い、batch manifestではそのファイルを `ok=false` + `error` にできます。

```bash
python3 -m unittest -v test_inspector.py
```

公開mainで既存ケースを含む4 testsを実行します。この検証は動画品質そのものを保証するものではなく、入力メタデータから不正な時間を正常判定へ通さないための回帰境界です。
