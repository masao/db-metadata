#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

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

	my $report = $conf::REPORT_HEADER;
	for my $entry (@conf::PARAMETERS) {
            $report .= "<tr><td>$conf::PARAM_LABELS{$entry}</td><td>";
            my @type =split(/:/, $conf::PARAM_TYPES{$entry});
            if ($type[0] eq "textfield") {
                $report .= CGI::escapeHTML(param($entry));
            } elsif ($type[0] eq "radio") {
		my $str = $entry . param($entry);
                $report .= $conf::PARAM_LABELS{$str};
            } elsif ($type[0] eq "textarea") {
		$report .= "<pre>";
		$report .= CGI::escapeHTML(param($entry));
		$report .= "</pre>";
	    } elsif ($type[0] eq "external") {
		param($entry, eval "$type[1]");
                $report .= CGI::escapeHTML(param($entry));
	    }
            $report .= "</td></tr>\n";
	}
	$report .= $conf::REPORT_FOOTER;

	# CSVファイルに書き込む
	util::write_csv($conf::FILENAME,
			map { defined(param($_)) ? param($_) : '' } @conf::PARAMETERS);

	print header();
	print $conf::HTML_HEADER;
	print $report;
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
<table border="2">
EOF
    for my $entry (@conf::PARAMETERS) {
	next if $conf::PARAM_TYPES{$entry} =~ /^external/;
	$retstr .= "<tr><td>$conf::PARAM_LABELS{$entry}";
	$retstr .= " ※" if defined $conf::REQ_PARAMETERS{$entry};
	$retstr .= "</td><td>";
	my @type = split(/:/, $conf::PARAM_TYPES{$entry});
	if ($type[0] eq 'textfield') {
	    my $size = $type[1];
	    $retstr .= "<input type=\"text\" name=\"$entry\" value=\"";
	    $retstr .= CGI::escapeHTML(param($entry)) if defined param($entry);
	    $retstr .= "\" size=\"$size\">";
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
	}
	$retstr .= "</td></tr>\n";
    }
    $retstr .= <<EOF;
</table>
<p>
<input type="submit" value=" 登 録 ">
</p>
<p>※ 必須入力項目です。</p>
</form>
EOF
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda(
$conf::FROM,
$conf::SUBJECT,
$conf::NOTE,
$conf::FILENAME,
$conf::USE_MAIL,
$conf::REPORT_HEADER,
$conf::REPORT_FOOTER,
);
