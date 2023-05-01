# work_support

## ファイル名
音楽ファイルがout.wavに設定されているため、main.pyの変数nameを好きな音楽ファイル名に変更する。

## ライブラリのインストール
OpenCV、dlib、scipy、pyaudioなどが入っていない場合インストールする。

## 基準値の調整
瞬きの検出に用いる基準値であるEYE_AR_THRESHとEYE_AR_OPENINGの数値を変更する。設定方法が確率されていないため、各自で適切な数値を模索してください。（今後実装予定ではあります）

まず、setup.pyを実行しゆっくり瞬きを数回行い目の縦横比の最大値と最小値を得ます。この最大値と最小値の中央値付近で基準値を設定します。
EYE_AR_OPENINGを中央値に、EYE_AR_THRESHを中央値より0.03程小さく設定してみてください。（main.py）
基準値を設定したらmain.pyを実行し、目を閉じたときfalse、目を開けたときtrueが表示されるかを確認します。また、瞬きの検出が正常にできているかを確認します。
もし、瞬きの検出精度が悪いときは基準値を調整してください。


## How-To-Edit
1. プロジェクトをクローン
```bash
$ git clone git@github.com:tus18/WorkSupport.git
```

2. コンパイル
```bash
$ python main.py
```
3. プログラム終了
```
Escキーで終了
```
