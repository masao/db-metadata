#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;

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
    my $tmpl = HTML::Template->new('filename' => 'template/list.tmpl');

    opendir(DIR, $conf::DATADIR) || die "opendir: $conf::DATADIR: $!";
    @files = grep { /^\d+\.xml$/o } readdir(DIR);
    @files = sort { $a <=> $b } @files;
    closedir(DIR) || die "closedir: $!";

    my $search_result = '';
    if (length($search)) {	# 検索
	my @result = ();
	for my $file (@files) {
	    my $cont = util::readfile("$conf::DATADIR/$file");
	    push @result, $file if $cont =~ /$search/oi;
	}
	@files = @result;
	$search_result .= <<EOF;
<p>Perl で /$search/oi しています。grep -i とほぼ同じです。</p>
<p><font color="red">検索結果: $#files 件</font></p>
EOF
    }

    my $list_table = <<EOF;
<table width="100%" border="1" bgcolor="$BGCOLOR">
<tr bgcolor="$BGCOLOR_HEAD">
<th> - </th>
EOF
    for (my $i = 0; $i < @DISPLAY_ELEMENTS; $i++) {
	$list_table .= <<EOF;
<th>
<a href="$SCRIPT_NAME?sort=$i;search=$search">$conf::PARAM_LABELS{$DISPLAY_ELEMENTS[$i]}</a>
<a href="$SCRIPT_NAME?sort=${i}r;search=$search">(*)</a>
</th>
EOF
    }
    $list_table .= "</tr>\n";

    for (my $i = $page * $MAX; $i < @files && $i < ($page+1) * $MAX; $i++) {
	$list_table .= "<tr valign=\"top\">\n";
	$list_table .= "<td><a href=\"$files[$i]\">". ($i + 1) ."</a></td>\n";
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
	    $list_table .= "<td>$cont</td>\n";
	}
	$list_table .= "</tr>\n";
    }
    $list_table .= "</table>\n";

    $tmpl->param('TITLE' => $conf::TITLE,
		 'HOME_TITLE' => $conf::HOME_TITLE,
		 'HOME_URL' => $conf::HOME_URL,
		 'FROM' => $conf::FROM,
		 'SCRIPT_NAME' => script_name(),
		 'search_result' => $search_result,
		 'list_table' => $list_table,
		 'list_page' => list_pages()
		);
    print $tmpl->output;
}

# 数字を考慮したソート
sub fncmp() {
    my ($x, $y) = @_;
    $x =~ s/(\d+)/sprintf("%05d", $1)/ge;
    $y =~ s/(\d+)/sprintf("%05d", $1)/ge;
    return $x cmp $y;
}

sub list_pages() {
    my $base_url = "$SCRIPT_NAME?sort=$sort;search=$search";
    my $retstr = "<p>ページ:\n";
    for (my $i = 0; $i*$MAX < @files; $i++) {
	if ($i == $page) {
	    $retstr .= "[". ( $i+1 ) ."]\n";
	} else {
	    $retstr .= "<a href=\"$base_url;page=$i\">[". ( $i+1 ) ."]</a>\n";
	}
    }
    $retstr .= "</p>\n";
    return $retstr;
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda($conf::TITLE,
	   $conf::HOME_TITLE,
	   $conf::HOME_URL,
	   $conf::FROM,
	   $conf::PARAM_LABELS,
	  );
