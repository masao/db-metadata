#!/usr/bin/perl -w
# $Id$
# 共通するテストを行う。

use strict;
use Test;

BEGIN { plan test => 4 }

my $cgi = "./browse.cgi";

foreach my $arg ("id=0001", "id=unknown", "search=新聞", "scan=keyword") {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
