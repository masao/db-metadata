#!/usr/local/bin/perl -w
# -*- CPerl -*-
# $Id$

# 登録/更新用 CGI

use strict;
use POSIX;
use CGI qw/:standard/;
use CGI::Carp 'fatalsToBrowser';
use HTML::Template;

$| = 1;

use lib "..";
require 'util.pl';
require 'conf.pl';	# 設定内容を読み込む

my $q = CGI->new();
$q->import_names();

my $user = $q->remote_user();

main();
sub main {
    if (defined($q->param('submit'))) {	# 登録処理
	my $error = '';
	foreach my $entry (keys %conf::REQ_PARAMETERS) { # 必須項目のエラー処理
	    if (!defined($q->param($entry)) || !length($q->param($entry))) {
		$error .= "<p>エラー: 「<font color=\"red\">$conf::PARAM_LABELS{$entry}</font>」は必須項目です。</p>\n";
	    } elsif ($entry eq "e-mail" && $q->param($entry) !~ /\S+@\S+/) {
		$error .= "<p>エラー: 「<font color=\"red\">$conf::PARAM_LABELS{$entry}</font>」が正しくありません。</p>\n";
	    }
	}
	if (length($error)) {
	    print header();
	    my $tmpl = HTML::Template->new('filename' => '../template/form.tmpl');
	    $tmpl->param('TITLE' => $conf::TITLE,
			 'HOME_TITLE' => $conf::HOME_TITLE,
			 'HOME_URL' => $conf::HOME_URL,
			 'FROM' => $conf::FROM,
			 'SCRIPT_NAME' => script_name(),
			 'USER' => remote_user(),
			 'BASEDIR' => '..',
			 'ERROR' => $error,
			 'FORM_CONTROL' => param2form(@conf::PARAMETERS),
			 'REQ_MARK' => $conf::REQ_MARK,
			);
	    print $tmpl->output;
	    exit;
	}

	# lockdir();
	my $id = util::untaint($q->param('id'), '\d+', undef) || get_id();
	my $fh = util::fopen(">../$conf::DATADIR/$id.xml");
	print $fh param2xml($id);
	$fh->close;

	print header("text/html; charset=utf-8");
	my $tmpl = HTML::Template->new('filename' => '../template/update-complete.tmpl');
	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
#		     'SCRIPT_NAME' => script_name(),
		     'BASEDIR' => '..',
		     'USER' => remote_user(),
		     'DBID' => $id,
		     'DBTITLE' => $Q::dbname,
		    );
	print $tmpl->output;
	# unlockdir();
	
    } elsif (defined($q->param('id'))) {	# 更新用フォーム生成
	my $id = $q->param('id');
	my $cont = util::readfile("$conf::DATADIR/$id.xml");
	if ($q->remote_user() ne (util::get_tagvalues($cont, "userid"))[0]) {
	    print $q->redirect("./browse.cgi?id=$id");
	    exit;
	}

	print header("text/html; charset=utf-8");
	my $tmpl = HTML::Template->new('filename' => '../template/form.tmpl');
	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'SCRIPT_NAME' => script_name(),
		     'USER' => remote_user(),
		     'BASEDIR' => '..',
		     'FORM_CONTROL' => param2form_update($cont, @conf::PARAMETERS),
		     'REQ_MARK' => $conf::REQ_MARK,
		    );
	print $tmpl->output;
    } else {				# 新規登録フォーム生成
	print header("text/html; charset=utf-8");
	my $tmpl = HTML::Template->new('filename' => '../template/form.tmpl');
	$tmpl->param('TITLE' => $conf::TITLE,
		     'HOME_TITLE' => $conf::HOME_TITLE,
		     'HOME_URL' => $conf::HOME_URL,
		     'FROM' => $conf::FROM,
		     'SCRIPT_NAME' => script_name(),
		     'USER' => remote_user(),
		     'BASEDIR' => '..',
		     'FORM_CONTROL' => param2form(@conf::PARAMETERS),
		     'REQ_MARK' => $conf::REQ_MARK,
		    );
	print $tmpl->output;
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
           $retstr .= CGI::escapeHTML($q->param($entry)) if defined $q->param($entry);
           $retstr .= "\">\n";
	   next;
       }

       $retstr .= "<tr><th>$conf::PARAM_LABELS{$entry}";
       $retstr .= " $conf::REQ_MARK" if defined $conf::REQ_PARAMETERS{$entry};
       $retstr .= "</th><td>";

       if ($type[0] eq 'textfield') {
           my $size = $type[1];
           $retstr .= "<input type=\"text\" name=\"$entry\" value=\"";
           $retstr .= CGI::escapeHTML($q->param($entry)) if defined $q->param($entry);
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
           $retstr .= CGI::escapeHTML($q->param($entry)) if defined $q->param($entry);
           $retstr .= "</textarea>";
       } elsif ($type[0] eq 'radio') {
            shift @type;
            foreach my $val (@type) {
                $retstr .= "<input type=\"radio\" name=\"$entry\" value=\"$val\"";
                if (defined($q->param($entry)) && $q->param($entry) eq $val) {
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

# 更新用のフォーム部品を既存の内容に従って配置する
sub param2form_update($@) {
    my ($cont, @parameter) = (@_);
    my $retstr = '';
    for my $entry (@parameter) {
	my @values = util::get_tagvalues($cont, $entry);
	my @type = split(/:/, $conf::PARAM_TYPES{$entry});
	if ($type[0] eq "external") {
	    next;
	} elsif ($type[0] eq 'hidden') {
	    $retstr .= "<input type=\"hidden\" name=\"$entry\" value=\"";
	    $retstr .= CGI::escapeHTML(join(',', @values)) if @values;
	    $retstr .= "\">\n";
	    next;
	}

	$retstr .= "<tr><th>$conf::PARAM_LABELS{$entry}";
	$retstr .= " $conf::REQ_MARK" if defined $conf::REQ_PARAMETERS{$entry};
	$retstr .= "</th><td>";

	if ($type[0] eq 'textfield') {
	    my $size = $type[1];
	    $retstr .= "<input type=\"text\" name=\"$entry\" value=\"";
	    $retstr .= CGI::escapeHTML(join(',', @values)) if @values;
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
	    $retstr .= CGI::escapeHTML($values[0]) if @values;
	    $retstr .= "</textarea>";
	}
	$retstr .= "</td></tr>\n";
    }
    return $retstr;
}

# ユーザが入力したパラメータをXML化する。
sub param2xml($) {
    my ($id) = @_;
    my $date = POSIX::strftime("%Y-%m-%dT%H:%M:%S", localtime());
    my $xml = <<EOF;
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE database_metadata SYSTEM "db.dtd">
<database_metadata>
  <id>$id</id>
  <source_id/>
  <created_date>$date</created_date>
  <update_date>$date</update_date>
  <userid>$user</userid>
  <dbname>$Q::dbname</dbname>
  <system>$Q::system</system>
  <condition>$Q::condition</condition>
EOF
    $xml .= repeatable_tags("format");
    $xml .= repeatable_tags("contributor");
    $xml .= <<EOF;
  <description>$Q::description</description>
EOF
    $xml .= repeatable_tags("subject");
    $xml .= repeatable_tags("type");
    $xml .= repeatable_tags("lang");
    $xml .= <<EOF;
  <period>$Q::period</period>
  <total>$Q::total</total>
  <interval>$Q::interval</interval>
  <interval_num>$Q::interval_num</interval_num>
  <region>$Q::region</region>
  <category/>
  <access>$Q::access</access>
</database_metadata>
EOF
    return $xml;
}

sub repeatable_tags($) {
    my ($tag) = @_;
    my $xml = "";
    if (!defined($q->param($tag)) || !length($q->param($tag))) {
	$xml = "  <$tag/>\n";
    } elsif (index($q->param($tag), ",")) {
	my @values = split(/,/, CGI::escapeHTML($q->param($tag)));
	for my $val (@values) {
	    $xml .= "  <$tag>$val</$tag>\n";
	}
    } else {
	$xml .= "  <$tag>". CGI::escapeHTML($q->param($tag)) ."</$tag>\n";
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
	    $report .= CGI::escapeHTML($q->param($entry));
	} elsif ($type eq "radio") {
	    my $str = $entry . $q->param($entry);
	    $report .= $conf::PARAM_LABELS{$str};
	} elsif ($type eq "textarea") {
	    $report .= "<pre>";
	    $report .= CGI::escapeHTML($q->param($entry));
	    $report .= "</pre>";
	} elsif ($type eq "external") {
	    $q->param($entry, eval "$args[0]");
	    $report .= CGI::escapeHTML($q->param($entry));
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
    my @files = util::pickup_files();
    my ($num) = $files[$#files] =~ /(\d+)\.xml$/;
    $num++;
    return sprintf("%04d", $num);
}

# For avoiding "used only once: possible typo at ..." warnings.
util::muda(
$conf::SUBJECT,
$conf::USE_MAIL,
);
