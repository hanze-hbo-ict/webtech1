# from speler import Speler
#
# bram = Speler("Bram")
#
# # print(bram.naam)
# # print(bram.levens)
# bram.levens -= 1
# print(bram.levens)
# bram.levens -= 1
# print(bram)
#
# bram.levens -= 1
# print(bram)
#
# bram.levens -= 1
# print(bram)
#
# bram.level = 2
# print(bram)
#
# bram.level += 5
# print(bram)
#
# bram.level = 3
# print(bram)
#
# bram.score = 500
# print(bram)

from aardman import Aardman, Ork, Uruk_Hai, Mordor

# shagrat = Ork()
# print(shagrat)

# gorbag = Ork("Gorbag")
# print(f"Gorbag - {gorbag}")
#
# duergar = Aardman("Duergar", 23)
# print(duergar)
#
# gorbag.slaan()
# random_aardman = Aardman("Aardman", 12, 1)
# print(random_aardman)
#
# random_aardman.schade(4)
# print(random_aardman)
#
# random_aardman.schade(8)
# print(random_aardman)
#
# random_aardman.schade(9)
# print(random_aardman)

# gothmog = Mordor("Gothmog")
# print(gothmog)
# gothmog.schade(12)
# print(gothmog)
#
lurtz = Uruk_Hai("Lurtz")
# print(lurtz)
# lurtz.schade(14)
# print(lurtz)
lurtz._levens = 0
lurtz._hit_points = 1
print(lurtz)
