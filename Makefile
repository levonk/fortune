POSSIBLE += $(shell ls -1 | egrep -v '\.dat|README|Makefile|\.sh' | sed -e 's/$$/.dat/g')

all: ${POSSIBLE}

%.dat: %
	@strfile $< $@
	@fortune $<
