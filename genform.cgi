#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';

$| = 1;

use lib ".";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

main();
sub main {
    if (defined(param())) {
	my $error = '';
	for my $entry (keys %conf::REQ_PARAMETERS) { # 必須項目のエラー処理
	    if (!defined(param($entry)) || !length(param($entry))) {
		$error .= "<p>エラー: 「<font color=\"red\">$conf::PARAM_LABELS{$entry}</font>」は必須項目です。</p>\n";
	    } elsif ($entry eq "e-mail" && param($entry) !~ /\S+@\S+/) {
		$error .= "<p>エラー: 「<font color=\"red\">$conf::PARAM_LABELS{$entry}</font>」が正しくありません。</p>\n";
	    }
	}
	if (length($error)) {
	    print header();
	    print $conf::HTML_HEADER;
	    print $error;
	    print html_form();
	    print $conf::HTML_FOOTER;
	    exit;
	}

	my $xml = <<EOF;
<?xml version="1.0" encoding="EUC-JP"?>
<データベース>
EOF
	$xml .= param2xml(@conf::PARAMETERS);
	$xml .= "</データベース>\n";

	# データを登録する
	my $id = get_id();
	my $xmlfile = "$conf::DATADIR/$id.xml";
	my $fh = util::fopen(">$xmlfile");
	print $fh $xml;
	$fh->close;

	my $report = '';
	print header();
	print $conf::HTML_HEADER;
	print "<p>データを登録しました。</p>";
	print $conf::HTML_FOOTER;

	if ($conf::USE_MAIL) {
	    my $msg = util::html2txt($report);
	    util::send_mail($conf::FROM, param('e-mail'), $conf::SUBJECT,
			    param('name'), $msg);
	}
    } else {
	print header();
	print $conf::HTML_HEADER;
	print html_form();
	print $conf::HTML_FOOTER;
    }
}

sub html_form() {
    my $script_name = script_name();
    my $retstr = <<EOF;
$conf::NOTE
<form method="POST" action="$script_name">
<table cellpadding="2" border="2">
EOF
    $retstr .= param2form(@conf::PARAMETERS);
    $retstr .= <<EOF;
</table>
<p>
<input type="submit" value=" 登 録 ">
</p>
<p>$conf::REQ_MARK は必須入力項目を示します。</p>
</form>
EOF
}

# フォーム部品を設定に従って配置する
sub param2form(@) {
    my (@parameter) = (@_);
    my $retstr = '';
    for my $entry (@parameter) {
	next if $conf::PARAM_TYPES{$entry} =~ /^external/o;
	$retstr .= "<tr><td>$conf::PARAM_LABELS{$entry}";
	$retstr .= " $conf::REQ_MARK" if defined $conf::REQ_PARAMETERS{$entry};
	$retstr .= "</td><td>";
	my @type = split(/:/, $conf::PARAM_TYPES{$entry});
	if ($type[0] eq 'textfield') {
	    my $size = $type[1];
	    $retstr .= "<input type=\"text\" name=\"$entry\" value=\"";
	    $retstr .= CGI::escapeHTML(param($entry)) if defined param($entry);
	    $retstr .= "\"";
	    $retstr .= " size=\"$size\"" if defined $size;
	    $retstr .= ">";
	    if (defined $conf::PARAM_REPEATABLES{$entry}) {
		$retstr .= "<br><small>複数の項目を登録する場合は、コンマで区切って入れてください。<br>例: $conf::PARAM_LABELS{$entry}1,$conf::PARAM_LABELS{$entry}2,$conf::PARAM_LABELS{$entry}3</small>";
	    }
	} elsif ($type[0] eq 'textarea') {
	    my $rows = $type[1];
	    my $cols = $type[2];
	    $retstr .= "<textarea name=\"$entry\" rows=\"$rows\" cols=\"$cols\">";
	    $retstr .= CGI::escapeHTML(param($entry)) if defined param($entry);
	    $retstr .= "</textarea>";
	} elsif ($type[0] eq 'radio') {
            shift @type;
            foreach my $val (@type) {
                $retstr .= "<input type=\"radio\" name=\"$entry\" value=\"$val\"";
                if (defined(param($entry)) && param($entry) eq $val) {
                    $retstr .= " checked";
                }
                $retstr .= ">". $conf::PARAM_LABELS{"$entry:$val"};
            }
	} elsif ($type[0] eq "nest") {
	    shift @type;
	    $retstr .= "<table cellpadding=\"1\" border=\"1\" width=\"100%\">";
	    $retstr .= param2form(@type);
	    $retstr .= "</table>";
	}
	$retstr .= "</td></tr>\n";
    }
    return $retstr;
}

# ユーザが入力したパラメータをXML化する。
sub param2xml (@) {
    my @parameters = (@_);
    my $xml = '';
    for my $entry (@parameters) {
	my $value = CGI::escapeHTML(param($entry));
	my $tag = $conf::PARAM_LABELS{$entry};
	my ($type, @args) =split(/:/, $conf::PARAM_TYPES{$entry});
	if ($type eq "textfield") {
	    if (defined $conf::PARAM_REPEATABLES{$entry} &&
		param($entry) =~ /,/o) {
		my @values = split(/,/, CGI::escapeHTML(param($entry)));
		for my $val (@values) {
		    $xml .= "<$tag>$val</$tag>\n";
		}
	    } else {
		$xml .= "<$tag>". CGI::escapeHTML(param($entry)) ."</$tag>\n";
	    }
	} elsif ($type eq "radio") {
	    my $str = $entry . CGI::escapeHTML(param($entry));
	    $xml .= "<$tag>$conf::PARAM_LABELS{$str}</$tag>";
	} elsif ($type eq "textarea") {
	    $xml .= "<$tag>". CGI::escapeHTML(param($entry)) ."</$tag>\n";
	} elsif ($type eq "external") {
	    param($entry, eval "$args[0]");
	    $xml .= "<$tag>". CGI::escapeHTML(param($entry)) ."</$tag>\n";
	} elsif ($type eq "nest") {
	    $xml .= "<$tag>". param2xml(@args) ."</$tag>\n";
	}
    }
    return $xml;
}

sub get_id() {
    my $i = 0;
    while (-f "$conf::DATADIR/$i.xml") {
	$i++;
    }
    return $i;
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda(
$conf::FROM,
$conf::SUBJECT,
$conf::NOTE,
$conf::USE_MAIL,
);
