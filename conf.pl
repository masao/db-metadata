# $Id$
package conf;

### ���̤�����

# ô���ԤΥ᡼�륢�ɥ쥹
$FROM = 'yuka@ulis.ac.jp';

# �ڡ����Υ����ȥ�
$TITLE = '�ǡ����١����������Ͽ/����';

# �ۡ���ڡ����� URL
$HOME_URL = 'http://nile.ulis.ac.jp/~yuka/db-template/top.html';

# �ۡ���ڡ����Υ����ȥ�
$HOME_TITLE = '�ǡ����١�������ͭ�ץ�������';

# ɬ�ܹ��ܤ򼨤��ޡ�����HTML��
$REQ_MARK = '<small><font color="red">��</font></small>';

# ��Ͽ���Ƥ�Ͽ����ǥ��쥯�ȥ�̾: `chmod a+w $DATADIR`���Ƥ������ȡ�
$DATADIR = 'data';

# �᡼�����ε�ǽ��Ȥ���: �Ȥ����� 1 �ˤ��롣
$USE_MAIL = 0;

  # �᡼�����Τ������ Subject: ����ASCII�ϻȤ��ʤ���
  $SUBJECT = '[DB Metadata]';

# �ǡ�������Ͽ���� XML �Υ롼������̾
$ROOT_ELEMENT = '�ǡ����١���';

### HTML �� <form> ���ʤ����

# �ե��������ʤΥ�٥��̾����
%PARAM_LABELS = ('user' => '��Ͽ��',
		 'username' => '̾��',
		 'e-mail' => 'E-mail',# �᡼�����Τ������ɬ�סʰ����
		 'url' => 'URL',

		 'dbid' => '�ǡ����١���ID',
		 'dbname' => '�ǡ����١���̾',
		 'dbname_yomi' => '�ǡ����١���̾�����',
		 'system' => '�����ƥ�̾',
		 'system_yomi' => '�����ƥ�̾�����',
		 'producer' => '�ץ�ǥ塼��̾',
		 'producer_yomi' => '�ץ�ǥ塼��̾�����',
		 'producer_country' => '�ץ�ǥ塼����̾',
		 'distributor' => '�ǥ����ȥ�ӥ塼��̾',
		 'distributor_yomi' => '�ǥ����ȥ�ӥ塼��̾�����',
		 'distributor_country' => '�ǥ����ȥ�ӥ塼����̾',

		 'description' => '�ǡ����١�������ħ',
		 'field' => 'ʬ��',
		 'keyword' => '�������',
		 'type' => '�ǡ����Υ�����',
		 'publication' => '������̾',
		 'survey' => 'Ĵ��̾',
		 'lang' => '�ǡ����ε��Ҹ���',
		 'period' => '��Ͽ����',
		 'total' => '��Ͽ���',
		 'interval' => '��������',
		 'interval_num' => '�������',
		 'region' => '��Ͽ������ϰ�',

		 'service_type' => '�����ӥ�����',
		 'distribute_type' => '�ǡ����󶡷���',
		 'terminal_type' => 'ü������',
		 'fee' => '�����ӥ�����',
		 'time' => '�����ӥ�������',
		 'condition' => '���Ѿ��',
		 'comment' => '������',
		 'date' => '��Ͽ��'
		);

# �ե��������ʤ�ɽ�������CVS�ե�����ؤ���Ͽ����ͤ�
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

# �ե��������ʤΤ�����ɬ�����Ϲ��ܤΤ��
# �ʡ�e-mail�פξ��ϥ᡼�륢�ɥ쥹�δʰץ����å���Ԥ���
%REQ_PARAMETERS = ('username' => 1,
		   'dbname' => 1,
#		   'description' => 1,
		  );

# �ե��������ʤμ���: textfield, textarea, radio, etc.
#
# ��external�פ���Ͽ����ưŪ�˾�����ɲä����������Ѥ��롣
#
%PARAM_TYPES = ('user' => 'nest:username:e-mail:url',
		'username' => 'textfield:40',
		'e-mail' => 'textfield:40',# �᡼�����Τ������ɬ�סʰ����
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

# repeatable �����Ϲ���
%PARAM_REPEATABLES = ('keyword' => 1,
		      'type' => 1,
		      'lang' => 1,
		      'publication' => 1,
		      'service_type' => 1,
		      'distribute_type' => 1,
		     );

### ���ꤪ���
1;
