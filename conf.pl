# $Id$
package conf;

### ���̤�����

# ô���ԤΥ᡼�륢�ɥ쥹
$FROM = 'yuka@ulis.ac.jp';

# �ڡ����Υ����ȥ�
$TITLE = '�ǡ����١����������Ͽ/����';

# �ۡ���ڡ����� URL
$HOME_URL = 'http://nile.ulis.ac.jp/~masao/test/dbxml/';

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
%PARAM_LABELS = ('name' => '̾��',
		 'post' => '��°',
		 'e-mail' => 'E-mail',# �᡼�����Τ������ɬ�סʰ����
		 'note' => '�̿�',
		 'date' => '��Ͽ����',
		 'contact' => 'Ϣ����',
		 'contact_name' => '̾��',
		 'address' => '����',
		 'phone' => '����',
		 'keyword' => '�������',
		);

# �ե��������ʤ�ɽ�������CVS�ե�����ؤ���Ͽ����ͤ�
@PARAMETERS = ('name', 'post', 'e-mail', 'note', 'date', 'contact', 'keyword');

# �ե��������ʤΤ�����ɬ�����Ϲ��ܤΤ��
# �ʡ�e-mail�פξ��ϥ᡼�륢�ɥ쥹�δʰץ����å���Ԥ���
%REQ_PARAMETERS = ('name' => 1, 'e-mail' => 1);

# �ե��������ʤμ���: textfield, textarea, radio, etc.
#
# ��external�פ���Ͽ����ưŪ�˾�����ɲä����������Ѥ��롣
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

# repeatable �����Ϲ���
%PARAM_REPEATABLES = ('keyword' => 1);

### ���ꤪ���
1;
