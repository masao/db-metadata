#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;
use DB_File;

use lib ".";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

$| = 1;

# 1ページに表示する件数
my $MAX = 10;

# 1ページに表示する件数
my $MAX_PAGE = 20;

# URI らしき文字列に自動的にリンクを張る？
my $USE_AUTOLINK = 1;

# 一覧表示の際に表示すべき項目:  @conf::PARAMETERS で定義済の値を入れる
my @DISPLAY_ELEMENTS = ('username', 'date');

# CGIパラメータ
my $q = new CGI;
my $SCRIPT_NAME = $q->script_name();
my $page = CGI::escapeHTML($q->param('page')) || 0;
my $search = CGI::escapeHTML($q->param('search')) || "";
my $sort = CGI::escapeHTML($q->param('sort')) || 0;
my $id = CGI::escapeHTML($q->param('id'));
my $scan = CGI::escapeHTML($q->param('scan'));

# 記録されているデータを保持する配列
my @files = ();

main();
sub main {
    print $q->header("text/html; charset=UTF-8");

    if (defined $id) {
	my $tmpl = HTML::Template->new('filename' => 'template/browse-id.tmpl');
	my $content = exec_xslt("$conf::DATADIR/$id.xml", "template/browse-id.xsl");
	$tmpl->param('TITLE' => "データベース情報の閲覧",
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'CONTENT' => $content,
		     'ID' => $id);
	print $tmpl->output;
    } elsif (defined $scan) {
	if (length($search)) {
	    my $tmpl = HTML::Template->new('filename' => 'template/browse-scan-search.tmpl');
	    my @files = get_scanned_files($scan, $search);
	    $tmpl->param('TITLE' => "データベース情報の閲覧",
			 'HOME_TITLE' => $conf::HOME_TITLE,
			 'HOME_URL' => $conf::HOME_URL,
			 'FROM' => $conf::FROM,
			 'SCRIPT_NAME' => $SCRIPT_NAME,
			 'scan' => $scan,
			 'scanstr' => $conf::PARAM_LABELS{$scan},
			 'search' => $search,
			 'search_result' => scalar @files,
			 'list_table' => list_table(@files),
			 'list_page' => list_pages(@files)
			);
	    print $tmpl->output;
	} else {
	    my $tmpl = HTML::Template->new('filename' => 'template/browse-scan.tmpl');
	    $tmpl->param('TITLE' => "$conf::PARAM_LABELS{$scan} 一覧",
			 'HOME_TITLE' => $conf::HOME_TITLE,
			 'HOME_URL' => $conf::HOME_URL,
			 'FROM' => $conf::FROM,
			 'scan_list' => scan_list($scan));
	    print $tmpl->output;
	}
    } else {
	my $tmpl = HTML::Template->new('filename' => 'template/browse.tmpl');
	my @files = reverse util::pickup_files();
	@files = do_search(@files);

	$tmpl->param('TITLE' => "データベース情報の閲覧",
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'SCRIPT_NAME' => $SCRIPT_NAME,
		     'search' => $search,
		     'search_result' => scalar @files,
		     'list_table' => list_table(@files),
		     'list_page' => list_pages(@files)
		    );
	print $tmpl->output;
    }
}

sub do_search(@) {
    my (@files) = @_;
    my @result = ();
    if (length($search)) {	# 検索
	foreach my $file (@files) {
	    my $cont = util::readfile("$conf::DATADIR/$file");
	    push @result, $file if $cont =~ /$search/oi;
	}
    } else {
	@result = @files;
    }
    return @result;
}

sub scan_list($) {
    my ($dbname) = @_;
    my $result = "";
    my %hash = ();
    tie(%hash, 'DB_File', "$dbname.db", O_RDONLY) ||
	die "tie fail: $dbname.db: $!";
    foreach my $key (sort { count_num($hash{$b}) <=> count_num($hash{$a})
				|| $a cmp $b } keys %hash) {
	$result .= "<li><a href=\"$SCRIPT_NAME?search=$key;scan=$dbname\">$key</a>";
	$result .= " (". count_num($hash{$key}) .")\n";
    }
    return $result;
}

sub count_num($) {
    my ($str) = @_;
    my @tmp = split(/,/, $str);
    return scalar @tmp;
}

# scan+search条件に合致するファイル名を返す。
sub get_scanned_files($$) {
    my ($dbname, $str) = @_;
    my %hash = ();
    tie(%hash, 'DB_File', "$dbname.db", O_RDONLY) ||
	die "tie fail: $dbname.db: $!";
    return map { "$_.xml" } split(/,/, $hash{$str});
}

sub list_table(@) {
    my (@files) = @_;
    my $retstr = '';
    for (my $i = $page * $MAX; $i < @files && $i < ($page+1) * $MAX; $i++) {
	my $id = $files[$i];
	$id =~ s/\.xml$//g;
	$retstr .= exec_xslt("$conf::DATADIR/$files[$i]", "template/list.xsl",
			     ('id' => "'$id'"));
    }
    return $retstr;
}

sub list_pages(@) {
    my (@files) = @_;
    my $base_url = "$SCRIPT_NAME?sort=$sort;search=$search";
    $base_url .= ";scan=$scan" if defined $scan;
    my $retstr = "<p>ページ:\n";

    my $start = $page - $MAX_PAGE/2;
    $start = 0 if $start < 0;
    $retstr .= "... " if ($start != 0);

    for (my $i = $start; $i < $page+$MAX_PAGE/2 && $i*$MAX < @files; $i++) {
	if ($i == $page) {
	    $retstr .= "[". ( $i+1 ) ."]\n";
	} else {
	    $retstr .= "<a href=\"$base_url;page=$i\">[". ( $i+1 ) ."]</a>\n";
	}
    }
    $retstr .= " ..." if ($page+$MAX_PAGE/2) * $MAX < @files;
    $retstr .= "</p>\n";
    return $retstr;
}

sub exec_xslt($$%) {
    my ($xmlsrc, $xsltsrc, %param) = @_;
    require XML::LibXML;
    require XML::LibXSLT;

    return "<p class=\"error\">データファイルが読み込めません。</p>"
	unless -r $xmlsrc;

    my $parser = new XML::LibXML;
    my $xslt = new XML::LibXSLT;

    my $source = $parser->parse_file($xmlsrc);
    my $style_doc = $parser->parse_file($xsltsrc);
    my $stylesheet = $xslt->parse_stylesheet($style_doc);
    my $result = $stylesheet->transform($source, %param);
    return $stylesheet->output_string($result);
}

# 数字を考慮したソート
sub fncmp() {
    my ($x, $y) = @_;
    $x =~ s/(\d+)/sprintf("%05d", $1)/ge;
    $y =~ s/(\d+)/sprintf("%05d", $1)/ge;
    return $x cmp $y;
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda($conf::HOME_TITLE,
	   $conf::HOME_URL,
	   $conf::FROM,
	   $conf::PARAM_LABELS,
	  );
