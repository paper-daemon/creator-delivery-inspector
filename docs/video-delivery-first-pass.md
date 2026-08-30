# 動画納品QA、最初にどこを見るか

動画を最後まで目視する前に、まず「納品条件として機械的に落とせるもの」を先に見る。

Creator Delivery Inspector では `ffprobe` の結果から、解像度・尺・映像/音声codec・sample rate・channel数を確認できる。

## 今回の再現

Fedora上で2秒のfixtureを2本生成して、実際にShorts presetへ通した。

- 縦: `1080x1920`, 2.00s, MPEG-4 video + AAC 48kHz stereo → `ok: true`
- 横: `1920x1080`, 2.00s, MPEG-4 video + AAC 44.1kHz mono → Shorts presetでは `height 1080 >= 1280` がfalseになり `ok: false`

unit testも `3/3` 通過した。

## batch manifestの数字はpreset判定とは別

同じ2ファイルをfolder batchでmanifest化すると、probe自体が成功しているため2件とも `ok=True` になる。

これは矛盾ではなく、batch manifestの `ok` は「ファイルを正常にprobeできたか」で、Shorts presetの適合判定ではない。

なので納品QAでは、**probe成功** と **納品条件に合う** を分けて見る。

## 最後は現物を見る

解像度やcodecが正しくても、テロップ切れ、映像の黒フレーム、音ズレ、固有名詞、モザイク漏れ、内容の自然さまでは数値だけで判断できない。

順番は、**機械チェックで条件違反を先に拾う → 実映像で意味と見た目を確認する** が使いやすい。

- OSS: https://github.com/paper-daemon/creator-delivery-inspector
- managed QA: https://coconala.com/services/3914156

※ 上の数値は生成した検証fixtureの結果で、実案件の品質実績ではありません。
