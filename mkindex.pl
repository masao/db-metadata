#!/usr/local/bin/perl -w
# $Id$

use strict;
use DB_File;

require 'util.pl';
require 'conf.pl';      # 設定内容を読み込む

main();
sub main {
    my @files = util::pickup_files();
    my %keyword = ();
    tie(%keyword, 'DB_File', "keyword.db", O_CREAT|O_RDWR) ||
        die "tie fail: keyword.db: $!";

    foreach my $file (@files) {
	my $content = util::readfile("$conf::DATADIR/$file");
        my ($id) = get_tagvalues($content, "dbid");
        my @keywords = get_tagvalues($content, "keyword");
	# print "$id => @keywords\n";
	foreach my $key (@keywords) {
	    next unless defined $key;
	    if (defined $keyword{$key}) {
		$keyword{$key} .= ",$id";
	    } else {
		$keyword{$key} = $id;
	    }
	}
    }
    foreach my $key (sort keys %keyword) {
	print "$key => $keyword{$key}\n";
    }
}

sub get_tagvalues($$) {
    my ($cont, $tagname) = @_;
    my @tmp = ();
    $cont =~ s/<$tagname(?:\s+[^>]*)?>([^<]+)<\/$tagname>/push @tmp, $1/ges;
    return @tmp;
}
