# characters 40 and 41 are '(' and ')' and making a regex out of them will return
#   re.error: missing ), unterminated subpattern at position 1
# characters 42 and 43 are * and + and can't be used in regex either
FUN = chr(44)
FUN_MEME, FUN_JOKE = map(chr, range(400, 402))
