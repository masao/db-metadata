#!/usr/bin/perl -w
# $Id$
# 共通するテストを行う。

use strict;
use Test;

BEGIN { plan test => 5 }

my $cgi = "./browse.cgi";
my @test_args =
    ("id=0001", "id=unknown", "search=新聞", "scan=keyword",
     "id=8139", # 一番データが多い
     );

foreach my $arg (@test_args) {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
