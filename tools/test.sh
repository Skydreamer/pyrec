#!/bin/sh

pocketsphinx_continuous \
     -infile petuhov_3new.wav \
     -hmm msu_ru_zero.cd_cont_2000 \
     -dict msu_ru_nsh.dic \
     -lm msu_ru_zero.lm.dmp 
