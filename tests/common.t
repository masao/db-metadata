#!/usr/bin/perl -w
# $Id$
# ���̤���ƥ��Ȥ�Ԥ���

use strict;
use Test;

BEGIN { plan test => 16 }

common_test("./browse.cgi");

chdir("./member");
$ENV{'REMOTE_USER'} = "masao";

common_test("./browse.cgi");
common_test("./update.cgi");
common_test("./bbs.cgi");

sub common_test($) {
    my ($cgi) = @_;
    # syntax ��
    ok(`perl -cwT $cgi 2>&1`, qr/syntax OK/, "$cgi: syntax");

    # Ŭ���ʰ����Ǽ¹Ԥ��Ƥ⡢�ٹ�/���顼��å�������ɽ�����ʤ�����
    for my $arg (0, 1, "x"x500) {
	ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
    }
}    
