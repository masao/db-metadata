#!/usr/bin/perl -w
# $Id$
# ���̤���ƥ��Ȥ�Ԥ���

use strict;
use Test;

BEGIN { plan test => 3 }

my $cgi = "./browse.cgi";

foreach my $arg ("id=0001", "id=unknown", "search=��ʹ") {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
