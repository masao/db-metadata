# $Id$
package conf;

### 全般の設定

# 担当者のメールアドレス
$FROM = 'yuka@ulis.ac.jp';

# ページのタイトル
$TITLE = 'データベース情報の登録/更新';

# ホームページの URL
$HOME_URL = 'http://nile.ulis.ac.jp/~yuka/db-template/top.html';

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
%PARAM_LABELS = ('user' => '登録者',
		 'username' => '登録者名',
		 'e-mail' => 'E-mail',# メール通知する場合は必要（宛先）
		 'url' => 'URL',

		 'dbid' => 'データベースID',
		 'dbname' => 'データベース名',
		 'dbname_yomi' => 'データベース名・ヨミ',
		 'system' => 'システム名',
		 'system_yomi' => 'システム名・ヨミ',
		 'producer' => 'プロデューサ名',
		 'producer_yomi' => 'プロデューサ名・ヨミ',
		 'producer_country' => 'プロデューサ国名',
		 'distributor' => 'ディストリビュータ名',
		 'distributor_yomi' => 'ディストリビュータ名・ヨミ',
		 'distributor_country' => 'ディストリビュータ国名',

		 'description' => 'データベースの特徴',
		 'field' => '分野',
		 'subfield' => '分野',
		 'keyword' => 'キーワード',
		 'type' => 'データのタイプ',
		 'publication' => '冊子体名',
		 'survey' => '調査名',
		 'lang' => 'データの記述言語',
		 'period' => '収録期間',
		 'total' => '収録件数',
		 'interval' => '更新周期',
		 'interval_num' => '更新件数',
		 'region' => '収録情報の地域',

		 'service_type' => 'サービス種別',
		 'distribute_type' => 'データ提供形態',
		 'terminal_type' => '端末種別',
		 'fee' => 'サービス料金',
		 'time' => 'サービス時間帯',
		 'condition' => '使用条件',
		 'comment' => 'コメント',
		 'date' => '登録日'
		);

# フォーム部品の表示順序、CVSファイルへの登録順も兼ねる
@PARAMETERS = ('user',

	       'dbname',
	       'dbname_yomi',
	       'system',
	       'system_yomi',
	       'producer',
	       'producer_yomi',
	       'producer_country',
	       'distributor',
	       'distributor_yomi',
	       'distributor_country',

	       'description',
	       'field',
	       'keyword',
	       'type',
	       'publication',
	       'survey',
	       'lang',
	       'period',
	       'total',
	       'interval',
	       'interval_num',
	       'region',

	       'service_type',
	       'distribute_type',
	       'terminal_type',
	       'fee',
	       'time',
	       'condition',
	       'comment',
	       'date'
	      );

# フォーム部品のうち、必須入力項目のもの
# （「e-mail」の場合はメールアドレスの簡易チェックも行う）
%REQ_PARAMETERS = ('username' => 1,
		   'dbname' => 1,
#		   'description' => 1,
		  );

# フォーム部品の種類: textfield, textarea, radio, etc.
#
# 「external」は登録時に動的に情報を追加したい場合に用いる。
#
%PARAM_TYPES = ('user' => 'nest:username:e-mail:url',
		'username' => 'textfield:40',
		'e-mail' => 'textfield:40',# メール通知する場合は必要（宛先）
		'url' => 'textfield:40',

		'dbname'=> 'textfield:40',
		'dbname_yomi'=> 'textfield:40',
		'system'=> 'textfield:40',
		'system_yomi'=> 'textfield:40',
		'producer'=> 'textfield:40',
		'producer_yomi'=> 'textfield:40',
		'producer_country'=> 'textfield:40',
		'distributor'=> 'textfield:40',
		'distributor_yomi'=> 'textfield:40',
		'distributor_country'=> 'textfield:40',

		'description'=> 'textarea:5:60',
		'field'=> 'textfield:40',
		'keyword'=> 'textfield:40',
		'type'=> 'textfield:40',
		'publication'=> 'textfield:40',
		'survey'=> 'textfield:40',
		'lang'=> 'textfield:40',
		'period'=> 'textfield:40',
		'total'=> 'textfield:40',
		'interval'=> 'textfield:40',
		'interval_num'=> 'textfield:40',
		'region'=> 'textfield:40',

		'service_type'=> 'textfield:40',
		'distribute_type'=> 'textfield:40',
		'terminal_type'=> 'textfield:40',
		'fee' => 'textfield:40',
		'time' => 'textfield:40',
		'condition' => 'textfield:40',
		'comment' => 'textarea:4:60',
		'date' => 'external:sprintf("%d-%02d-%02d",(localtime)[5]+1900,(localtime)[4]+1,(localtime)[3])',
	       );

# repeatable な入力項目
%PARAM_REPEATABLES = ('keyword' => 1,
		      'type' => 1,
		      'lang' => 1,
		      'publication' => 1,
		      'service_type' => 1,
		      'distribute_type' => 1,
		     );

### 設定おわり
1;
