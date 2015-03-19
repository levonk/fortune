#!/bin/bash

INFILE=levonkquotes
DESTDIR=/usr/share/games/fortunes
sudo strfile -c % ${INFILE} ${DESTDIR}/${INFILE}.dat && sudo cp ${INFILE} ${DESTDIR}/.
fortune ${INFILE}
