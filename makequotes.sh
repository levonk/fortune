#!/bin/bash

INFILE=levonkquotes
DESTDIR=/usr/share/games/fortunes
sudo aptitude install -y fortune-mod && \
	sudo strfile -c % ${INFILE} ${DESTDIR}/${INFILE}.dat && \
	sudo cp ${INFILE} ${DESTDIR}/.
## Test it out
fortune ${INFILE}
