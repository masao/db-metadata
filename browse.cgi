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

# 記録されているデータを保持する配列
my @files = ();

main();
sub main {
    print $q->header("text/html; charset=EUC-JP");

    if (defined $id) {
	my $tmpl = HTML::Template->new('filename' => 'template/browse-id.tmpl');
	my $content = exec_xslt("data/$id.xml", "template/html.xsl");
	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'CONTENT' => $content);
	print $tmpl->output;
    } else {
	my $tmpl = HTML::Template->new('filename' => 'template/browse.tmpl');
	my @files = pickup_files();
	@files = do_search(@files);

	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'SCRIPT_NAME' => script_name(),
		     'search' => $search,
		     'search_result' => scalar @files,
		     'list_table' => list_table(@files),
		     'list_page' => list_pages(@files)
		    );
	print $tmpl->output;
    }
}

sub pickup_files() {
    my @files = ();
    opendir(DIR, $conf::DATADIR) || die "opendir: $conf::DATADIR: $!";
    @files = sort fncmp grep { /^\d+\.xml$/ } readdir(DIR);
    closedir(DIR) || die "closedir: $!";
    return @files;
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

sub exec_xslt($$%) {
    my ($xmlsrc, $xsltsrc, %param) = @_;
    require XML::LibXML;
    require XML::LibXSLT;

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
util::muda($conf::TITLE,
	   $conf::HOME_TITLE,
	   $conf::HOME_URL,
	   $conf::FROM,
	  );
