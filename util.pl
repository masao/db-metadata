# -*- CPerl -*-
# $Id$

package util;

use strict;
use IO::File;

my $NKF = '/usr/local/bin/nkf';
my $SENDMAIL = '/usr/lib/sendmail';

sub pickup_files() {
    my @files = ();
    opendir(DIR, $conf::DATADIR) || die "opendir: $conf::DATADIR: $!";
    @files = sort grep(/^\d+\.xml$/, readdir(DIR));
    closedir(DIR) || die "closedir: $!";
    return @files;
}

# 言語（$conf::LANG）を考慮して、テンプレートファイル名を展開する
sub template_fname($) {
    my ($fname) = @_;

    if (-r "$fname.$conf::LANG") {
	return "$fname.$conf::LANG";
    } elsif (-r "$fname") {
	return "$fname";
    } else {
	warn "Can't read $fname";
	return "$fname";
    }
}

# データベース名を取出してくる
sub get_dbname($) {
    my ($id) = @_;

    my $cont = util::readfile("$conf::DATADIR/$id.xml");
    my @tmp = get_tagvalues($cont, "dbname");

    return $tmp[0];
}

# コメント情報を取り出してくる
sub bbs_list($) {
    my ($id, $basedir) = @_;
    return undef if not -f "$basedir/bbs/$id";
    my $fh = util::fopen("$basedir/bbs/$id");
    my $retstr = "";
    my $i = 0;
    while (defined(my $line = <$fh>)) {
	my ($user, $date, $comment) = $line =~ /^([^\t]+)\t([^\t]+)\t(.*)$/;
	$retstr .= <<EOF;
<div class="comment">
<a name="$i" href="#$i">・</a>
<span class="user"><a href="browse.cgi?scan=username;search=$user">$user</a></span>
<span class="date">$date</span>
<p class="comment">$comment</p>
</div>
EOF
	$i++;
    }
    return $retstr;
}

# グループ情報を取出す
sub get_groupinfo($$) {
    my ($fname, $user) = @_;
    my %info = ();
    my $fh = fopen($fname);
    while (defined(my $line = <$fh>)) {
	if ($line =~ /^([^\t]+)\t([^:]+):([^\t]+)\t([^\t]*)\t(.*)$/){
	    next if (defined($user) && $user ne $2);
	    $info{$1} = {'user' => $2,
			 'name' => $3,
			 'description' => $4,
			 'list' => [ split(',', $5) ]
			};
	    # print $line;
	}
    }
    return %info;
}

# グループ情報を書出す
sub write_groupinfo($%) {
    my ($fname, %info) = @_;
    my $fh = fopen(">$fname");
    foreach my $id (keys %info) {
	print $fh "$id\t";
	print $fh $info{$id}->{"user"} .":". $info{$id}->{"name"} ."\t";
	print $fh $info{$id}->{"description"} ."\t";
	print $fh join(",", @{$info{$id}->{'list'}});
	print $fh "\n";
    }
}

sub write_csv($@) {
    my ($fname, @values) = @_;
    my $fh = fopen(">>$fname");
    my @tmp = ();
    foreach my $entry (@values) {
	$entry =~ s/(["'])/\\$1/g;
	$entry = "\"$entry\"" if $entry =~ /[,\n\r]/;
	$entry =~ s/[\r\n]+/<br>/g;
	push @tmp, $entry;
    }
    print $fh join(',', @tmp), "\n";
}

sub send_mail($$$$$) {
    my ($from, $to, $subject, $name, $msg) = @_;
    my $fh = fopen("| $NKF -j | $SENDMAIL -oi -t -f $from");
    print $fh <<EOF;
From: $from
Subject: $subject
To: $to

 $name 様

$msg
EOF
}

sub html2txt {
    my ($html) = @_;
    my $tmpfile = "/tmp/.html2txt.$$";
    my $fh = fopen("|/usr/local/bin/w3m -dump -cols 78 -T text/html > $tmpfile");
    print $fh $html;
    $fh->close();
    my $result = readfile($tmpfile);
    unlink($tmpfile);
    return $result;
}

# タグの内容を正規表現で強引に引っ張ってくる
sub get_tagvalues($$) {
    my ($cont, $tagname) = @_;
    my @tmp = ();
    $cont =~ s/<$tagname(?:\s+[^>]*)?>([^<]+)<\/$tagname>/push @tmp, $1/ges;
    return @tmp;
}

# HTMLの実体参照を行なう。
sub escape_html($) {
    my ($str) = @_;
    return undef if not defined $str;
    $str =~ s/&/&amp;/g;
    $str =~ s/</&lt;/g;
    $str =~ s/>/&gt;/g;
    $str =~ s/"/&quot;/go;
    return $str;
}

# 配列の内容を uniq する
sub uniq(@) {
    my (@in) = @_;
    my %saw = ();
    @saw{@in} = ();
    my @out = sort keys %saw;  # remove sort if undesired
    return @out;
}

# 汚染されている変数をキレイにする。（CGI::Untaint のローカル実装）
sub untaint($$$) {
    my ($tainted, $pattern, $default) = (@_);
    # print "\$tainted: $tainted\t\$pattern: $pattern\t\$default:$default\n";
    return $default if !defined $tainted;

    if ($tainted =~ /^($pattern)$/) {
        # print "matched.\n";
        return $1;
    } else {
        return $default;
    }
}

# 効率よくファイルの中身を読み込む。
sub readfile ($) {
    my ($fname) = @_;
    my $fh = fopen($fname);
    my $cont = '';
    my $size = -s $fh;
    read $fh, $cont, $size;
    $fh->close;
    return $cont;
}

sub fopen($) {
    my ($fname) = @_;
    my $fh = new IO::File;
    $fh->open($fname) || die "fopen: $fname: $!";
    return $fh;
}

# For avoiding "used only once: possible typo at ..." warnings.
sub muda {}
1;
