新生銀行のポイントプログラムにエントリーするツール。
このツールは自動で規約などに同意することを選択するので、同意できない場合は使用しないでください。
同意する必要のある規約は[ポイントプログラムのページ](https://www.shinseibank.com/service/point/)
などの新生銀行のウェブページから確認してください。

このツールを使用することによって被る結果のいかなる責任も負いません。

# 必要なもの
* Docker

または

- Python 3
- Pipenv
- Chrome
- [Chrome driver](https://chromedriver.chromium.org/downloads)

# 使用方法
```
pipenv run python ./autoentry.py --driver=/path/to/chromedriver \
  --account_num <account number> \
  --date_of_birth 'YYYY-MM-DD' \
  --tpoint_num <T point number> \
  --email <email>            
```

コマンドラインフラグの説明
* driver
  * Chrome driver がおいてあるパス。（Dockerの場合不要）
* account_num
  * 新生銀行の10桁の口座番号
* date_of_birth
  * 生年月日 YYYY-MM-DD
* tpoint_num
  * 16, 9桁のTポイントカード番号
* dpoint_num
  * 12桁のDポイント番号
* nanaco_num
  * 16桁のnanaco番号
* email
  * ポイントエントリーなどのメールを受け取ったメールアドレス

ポイントナンバーは複数指定された場合、プログラムが一つ選んでエントリーします。
コマンドラインフラグの説明
