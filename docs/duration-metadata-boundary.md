# Duration metadata boundary

Creator Delivery Inspectorはffprobeのdurationを納品QAへ使いますが、数値へ変換できるだけでは有効な時間とは限りません。

## 再現した問題

修正前は次の値を受理していました。

- `-1` はShorts presetでも `-1 <= 65` となりPASS
- `NaN` はpreset無しだと `ok=true` のままsummaryへ残る
- `inf` もpreset無しだと `ok=true` のままsummaryへ残る

さらに、`format.duration` が無い時に複数streamのうち最初に見つかったdurationだけを採用すると、短い補助streamが先・長い本編streamが後にあるメディアで、実際より短い時間を採用する可能性がありました。Shortsの上限判定ではfail-openにつながるため、stream fallbackは有効なdurationの最大値を使います。

## 現在の境界

1. `format.duration` がfiniteかつ0以上ならそれを採用します。
2. container durationが無効または欠落している場合は、finiteかつ0以上のstream durationを集め、その最大値を採用します。
3. どこにも正常なdurationが無ければ `ValueError` とし、batch manifestではそのファイルを `ok=false` + `error` にできます。

負値、`NaN`、`inf` は正常判定へ通しません。

```bash
python3 -m unittest -v test_inspector.py
```

公開mainの回帰suiteでは、欠落duration、stream fallback、複数streamで最長durationを使う境界も確認します。この検証は動画品質そのものを保証するものではなく、入力メタデータから不正または過小な時間を正常判定へ通さないための回帰境界です。
