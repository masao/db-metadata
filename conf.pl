# $Id$
package conf;

### 全般の設定

# 担当者のメールアドレス
$FROM = 'yuka@ulis.ac.jp';

# ページのタイトル
$TITLE = 'データベース情報の登録/更新';

# ホームページの URL
$HOME_URL = 'http://nile.ulis.ac.jp/~masao/test/dbxml/';

# ホームページのタイトル
$HOME_TITLE = 'データベース情報共有プロジェクト';

# 必須項目を示すマーク（HTML）
$REQ_MARK = '<small><font color="red">※</font></small>';

# 登録内容を記録するディレクトリ名: `chmod a+w $DATADIR`しておくこと。
$DATADIR = 'data';

# メール通知機能を使う？: 使う場合は 1 にする。
$USE_MAIL = 0;

  # メール通知する場合の Subject: （非ASCIIは使えない）
  $SUBJECT = '[DB Metadata]';

# データを登録する XML のルート要素名
$ROOT_ELEMENT = 'データベース';

### HTML の <form> 部品の定義

# フォーム部品のラベル（名前）
%PARAM_LABELS = ('name' => '名前',
		 'post' => '所属',
		 'e-mail' => 'E-mail',# メール通知する場合は必要（宛先）
		 'note' => '通信',
		 'date' => '登録日時',
		 'contact' => '連絡先',
		 'contact_name' => '名称',
		 'address' => '住所',
		 'phone' => '電話',
		 'keyword' => 'キーワード',
		);

# フォーム部品の表示順序、CVSファイルへの登録順も兼ねる
@PARAMETERS = ('name', 'post', 'e-mail', 'note', 'date', 'contact', 'keyword');

# フォーム部品のうち、必須入力項目のもの
# （「e-mail」の場合はメールアドレスの簡易チェックも行う）
%REQ_PARAMETERS = ('name' => 1, 'e-mail' => 1);

# フォーム部品の種類: textfield, textarea, radio, etc.
#
# 「external」は登録時に動的に情報を追加したい場合に用いる。
#
%PARAM_TYPES = ('name' => 'textfield:40',
		'post' => 'textfield:40',
		'e-mail' => 'textfield:40',
		'note' => 'textarea:4:50',
		'date' => 'external:scalar localtime()',
		'contact' => 'nest:contact_name:address:phone',
		'contact_name' => 'textfield:40',
		'address' => 'textfield:40',
		'phone' => 'textfield:40',
		'keyword' => 'textfield:50',
	       );

# repeatable な入力項目
%PARAM_REPEATABLES = ('keyword' => 1);

### 設定おわり
1;
