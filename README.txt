# PhotoMap Creator V8

PhotoMap Creator V8 は、写真のGPS情報を読み取り、Google My Maps用データや写真帳を自動作成するソフトです。

## 動作環境

Windows PC

※ Pythonのインストールは必要ありません。
※ setup.batの実行も必要ありません。

## 初めて使うとき

1. `PhotoMapCreator` フォルダをPCへコピーします。

2. フォルダ内の `PhotoMapCreator.exe` をダブルクリックします。

3. 「番号または新しいプロジェクト名：」と表示されたら、新しいプロジェクト名を入力して Enter キーを押します。

例：

`genba01`

4. `projects` フォルダの中に、新しいプロジェクトが自動作成されます。

例：

`projects\genba01`

その中に、

`photos`

`output`

の2つのフォルダが自動作成されます。

## 写真を登録する方法

作成されたプロジェクトの `photos` フォルダへ写真をコピーします。

例：

`projects\genba01\photos`

写真を入れたあと、もう一度 `PhotoMapCreator.exe` をダブルクリックします。

表示されたプロジェクト一覧から使用するプロジェクトの番号を入力して、Enter キーを押します。

## 作成されるファイル

処理が完了すると、プロジェクトの `output` フォルダに次のファイルが作成されます。

`MyMaps.kml`
Google My Maps用KMLデータ

`MyMaps.csv`
Google My Maps用CSVデータ

`photo_book.html`
写真帳

`photo_sheet.html`
写真一覧

## 注意事項

`PhotoMapCreator.exe` だけを別の場所へ移動しないでください。

PhotoMapCreatorフォルダは、フォルダごと使用してください。

`icons` フォルダや、PhotoMapCreatorと一緒に入っているシステム用ファイルは削除しないでください。

写真はJPEG形式（`.jpg` / `.jpeg`）を使用してください。

GPS情報が入っていない写真は、地図上の位置情報を作成できません。

写真やGoogle My Maps上で写真を表示する機能を利用する場合は、インターネット接続が必要です。

## 普段の使い方

1. `PhotoMapCreator.exe` をダブルクリック
2. 使用するプロジェクト番号を入力
3. Enterキーを押す
4. `output` フォルダで作成結果を確認

Python、PowerShell、コマンド操作は必要ありません。
