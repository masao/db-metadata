INDEX = keyword.db dbname.db system.db username.db

all: $(INDEX) test

# 簡単なテストを行う
test: $(SCRIPTS)
	perl -e 'use Test::Harness qw(&runtests $$verbose); $$verbose=1; runtests @ARGV;' tests/*.t

$(INDEX):
	rm -f $(INDEX);
	for f in $(INDEX); do \
	    ./mkindex.pl `basename $$f .db`; \
	done;

clean:
	rm -f $(INDEX)
