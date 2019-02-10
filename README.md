## これなに？

IoTボタンで[MYレコーダー](https://www.kingtime.jp/record/myrecorder/)の打刻とSlackの勤怠報告などをまとめて行うAWS Lambda関数およびその周辺をまとめたプロジェクトです。

## 動作環境

以下の動作環境で動作を確認しています。

|ソフトウェア|バージョン|
|:---|:---|
|node|v10.13.0|
|npm|6.4.1|
|Serverless Framework|1.35.1|

## 事前準備

Lambda関数を実行する前に、以下の作業を実施する必要があります。

### Headless Chromium + Web DriverのDL

Headless Chrome + Selenium を含めたLambda Layerを作るため、事前に `layers/headless-chromium` 配下に必要なバイナリをDLしておきます。

```bash
$ cd layers/headless-chromium/
$ sh download_bin.sh
```

### AWS Secrets Managerに認証情報を登録する

AWSアカウント上のにMyレコーダーとSlackの認証情報を以下の形式で[AWS Secrets Manager](https://aws.amazon.com/jp/secrets-manager/)に登録しておきます。

|シークレット名|シークレットキー|シークレット値|
|:---|:---|:---|
|cm-clockin-button/myrecorder|id|<ログインID>|
|cm-clockin-button/myrecorder|passwd|<パスワード>|
|cm-clockin-button/slack|token|<レガシートークン>|

slackのレガシートークンの取得方法については[こちら](https://api.slack.com/custom-integrations/legacy-tokens)。

## Lambda関数のデプロイ

事前にデプロイしたいAWS環境の設定を`cm-clockin-button` としてプロファイルに登録し、以下のコマンドを実行します。

```
$ npm i
$ sls deploy
```

## IoTボタンとの連携

作成後は、[AWS IoT 1-Click](https://aws.amazon.com/jp/iot-1-click/)を利用してIoTボタンの接続先を作成したLambda関数に連携すると、以下のように動きます。

|ボタン操作|動作|
|:---|:---|
|シングルクリック|出勤|
|ダブルクリック|退勤|
