#!/usr/bin/perl -w
# $Id$
# browse.cgi に対するテストを行う。

use strict;
use Test;

BEGIN { plan test => 9 }

my $cgi = "./browse.cgi";
my @test_args =
    ("id=0001",
     "id=unknown",
     "search=新聞",
     "scan=keyword",
     "id=8139", # 一番データが多い
     "id=9354", # 最後のid
     "scan=keyword search=PC",
     "scan=keyword search=エネルギー page=1",
     "scan=system",
     );

foreach my $arg (@test_args) {
    ok(`perl -wT $cgi $arg 2>&1 > /dev/null`, '', "$cgi: $arg");
}
