#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;

$| = 1;

use lib "..";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む


main();
sub main {
    if (defined(param('submit'))) {	# 登録処理
	
    } elsif (defined(param('id'))) {	# 更新用フォーム生成
	
    } else {				# 新規登録フォーム生成
	print header("text/html; charset=utf-8");
	my $tmpl = HTML::Template->new('filename' => '../template/form.tmpl');
	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'SCRIPT_NAME' => script_name(),
		     'USER' => remote_user(),
		     'FORM_CONTROL' => param2form(@conf::PARAMETERS),
		     'REQ_MARK' => $conf::REQ_MARK,
		    );
	print $tmpl->output;
	# print param2form(@conf::PARAMETERS);
    }
}

# フォーム部品を設定に従って配置する
sub param2form(@) {
    my (@parameter) = (@_);
    my $retstr = '';
    for my $entry (@parameter) {
       my @type = split(/:/, $conf::PARAM_TYPES{$entry});
       if ($type[0] eq "external") {
	   next;
       } elsif ($type[0] eq 'hidden') {
           $retstr .= "<input type=\"hidden\" name=\"$entry\" value=\"";
           $retstr .= CGI::escapeHTML(param($entry)) if defined param($entry);
           $retstr .= "\">\n";
	   next;
       }

       $retstr .= "<tr><th>$conf::PARAM_LABELS{$entry}";
       $retstr .= " $conf::REQ_MARK" if defined $conf::REQ_PARAMETERS{$entry};
       $retstr .= "</th><td>";

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
           $retstr .= "<textarea name=\"$entry\" rows=\"$rows\" cols=\"$cols\">
";
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
	my $tag = $entry; # $conf::PARAM_LABELS{$entry};
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

# 登録した内容を確認するために表示する
sub param2report (@) {
    my (@parameters) = @_;
    my $report = '';
    for my $entry (@parameters) {
	$report .= "<tr><td>$conf::PARAM_LABELS{$entry}</td><td>";
	my ($type, @args) =split(/:/, $conf::PARAM_TYPES{$entry});
	if ($type eq "textfield") {
	    $report .= CGI::escapeHTML(param($entry));
	} elsif ($type eq "radio") {
	    my $str = $entry . param($entry);
	    $report .= $conf::PARAM_LABELS{$str};
	} elsif ($type eq "textarea") {
	    $report .= "<pre>";
	    $report .= CGI::escapeHTML(param($entry));
	    $report .= "</pre>";
	} elsif ($type eq "external") {
	    param($entry, eval "$args[0]");
	    $report .= CGI::escapeHTML(param($entry));
	} elsif ($type eq "nest") {
	    $report .= "<table cellpadding=\"1\" border=\"1\" width=\"100%\">";
	    $report .= param2report(@args);
	    $report .= "</table>\n";
	}
	$report .= "</td></tr>\n";
    }
    return $report;
}

sub get_id() {
    my $i = 0;
    while (-f sprintf("$conf::DATADIR/%04.xml", $i)) {
	$i++;
    }
    return $i;
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda(
$conf::SUBJECT,
$conf::USE_MAIL,
);
