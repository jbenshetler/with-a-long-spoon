#!/bin/sh
# Byte-oriented pass run 2026-09-13, before the python pass. Immune to the
# latin-1 decoding problem because grep does not decode. Full source rows.
BASE=https://data.sba.gov/sites/default/files/distribution/SBA-OCA-2022-07-001
for n in public_150k_plus_240930 public_up_to_150k_1_240930 public_up_to_150k_2_240930 \
         public_up_to_150k_3_240930 public_up_to_150k_4_240930 public_up_to_150k_5_240930 \
         public_up_to_150k_6_240930 public_up_to_150k_7_240930 public_up_to_150k_8_240930 \
         public_up_to_150k_9_240930 public_up_to_150k_10_240930 public_up_to_150k_11_240930 \
         public_up_to_150k_12_240930; do
  curl -s "$BASE/$n.csv" | grep -iE 'MIRANDA (HOLDING|INTEREST|CONSOLIDAT|ASSOCIAT|AFFILIAT|ENTERPRIS|INDUSTR|EQUIT|ESTATE|CONCERN|ASSET|COMPAN|TRUST)'
done
