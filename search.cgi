#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use DirHandle;

use lib ".";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

$| = 1;

# 1ページに表示する件数
my $MAX = 10;

# テーブル全体の背景色
my $BGCOLOR = '#ddddd0';

# テーブルヘッダの背景色
my $BGCOLOR_HEAD = '#00A020';

# URI らしき文字列に自動的にリンクを張る？
my $USE_AUTOLINK = 1;

# 一覧表示の際に表示すべき項目:  @conf::PARAMETERS で定義済の値を入れる
my @DISPLAY_ELEMENTS = ('name', 'date');

# CGIパラメータ
my $q = new CGI;
my $SCRIPT_NAME = $q->script_name();
my $page = CGI::escapeHTML($q->param('page')) || 0;
my $search = CGI::escapeHTML($q->param('search')) || "";
my $sort = CGI::escapeHTML($q->param('sort')) || 0;

# 記録されているデータを保持する配列
my @files = ();

main();
sub main {
    print $q->header("text/html; charset=EUC-JP");
    print $conf::HTML_HEADER;
    print <<EOF;
<hr>
<form method="GET" action="$SCRIPT_NAME">
<p>正規表現:
<input type="text" name="search" value="$search">
<input type="hidden" name="sort" value="$sort">
<input type="submit" value="絞り込み検索">
</p>
</form>
<hr>
EOF

    opendir(DIR, $conf::DATADIR) || die "opendir: $conf::DATADIR: $!";
    @files = grep { /^\d+\.xml$/o } readdir(DIR);
    closedir(DIR) || die "closedir: $!";

    if (length($search)) {	# 検索
	my @result = ();
	for my $file (@files) {
	    my $cont = util::readfile($file);
	    push @result, $file if $cont =~ /$search/oi;
	}
	@files = @result;
	print "<p>Perl で /$search/oi しています。grep -i とほぼ同じです。</p>";
 	print "<p><font color=\"red\">検索結果: ", $#files + 1, "件</font></p>\n";
    }

    print <<EOF;
<table width="100%" border="1" bgcolor="$BGCOLOR">
<tr bgcolor="$BGCOLOR_HEAD">
EOF
    for (my $i = 0; $i < @DISPLAY_ELEMENTS; $i++) {
	print <<EOF;
<th>
<a href="$SCRIPT_NAME?sort=$i;search=$search">$conf::PARAM_LABELS{$DISPLAY_ELEMENTS[$i]}</a>
<a href="$SCRIPT_NAME?sort=${i}r;search=$search">(*)</a>
</th>
EOF
    }
    print "</tr>\n";

    for (my $i = $page * $MAX; $i < @files && $i < ($page+1) * $MAX; $i++) {
	print "<tr valign=\"top\">\n";
	# print "<td><a href=\"$script_name/$i\">". $i+1 ."</a></td>\n";
	my $cont = util::readfile("$conf::DATADIR/$files[$i]");
	for my $elem (@DISPLAY_ELEMENTS) {
	    my @tmp = ();
	    my $tag = $conf::PARAM_LABELS{$elem};
	    $cont =~ s#<$tag[^>]*>([^<]*)</$tag>#push(@tmp, $1)#e;
	    $cont = join(",", @tmp);
	    $cont =~ s/^\s+//g;
	    $cont =~ s/\s+$//g;
	    if ($USE_AUTOLINK) {
		$cont =~ s#((https?|ftp)://[;\/?:@&=+\$,A-Za-z0-9\-_.!~*'()]+)#<a href="$1">$1</a>#gi;
	    }
	    print "<td>$cont</td>\n";
	}
	print "</tr>\n";
    }
    print "</table>\n";
    print_pages();
    print $conf::HTML_FOOTER;
}


# 数字を考慮したソート
sub fncmp() {
    my ($x, $y) = @_;
    $x =~ s/(\d+)/sprintf("%05d", $1)/ge;
    $y =~ s/(\d+)/sprintf("%05d", $1)/ge;
    return $x cmp $y;
}

sub print_pages() {
    my $base_url = "$SCRIPT_NAME?sort=$sort;search=$search";
    print "<p>ページ:\n";
    for (my $i = 0; $i*$MAX < @files; $i++) {
	if ($i == $page) {
	    print "[", $i+1, "]\n";
	} else {
	    print "<a href=\"$base_url;page=$i\">[", $i+1, "]</a>\n";
	}
    }
    print "</p>\n";
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda($conf::HTML_HEADER,
	   $conf::HTML_FOOTER,
	   $conf::PARAM_LABELS,
	  );
