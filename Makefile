all: test

# 簡単なテストを行う
test: $(SCRIPTS)
	perl -e 'use Test::Harness qw(&runtests $$verbose); $$verbose=0; runtests @ARGV;' tests/*.t
