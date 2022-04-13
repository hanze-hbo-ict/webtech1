# De tabel is nu aangemaakt door BasicModelApp en SetUpDatabase uit te voeren
# Nu aandacht voor de nodige CRUD-opdrachten
# Dit is slechts een overzicht, later wordt het script automatisch uitgevoerd
# Het is de bedoeling een ieder vertrouwd te maken met CRUD-commando's

from basic_model_app import db,Cursist

###########################
###### CREATE ############
#########################
elsje = Cursist('Elsje',19)
db.session.add(elsje)
db.session.commit()

###########################
###### READ ##############
#########################
alle_cursisten = Cursist.query.all() # overzicht van alle studenten
print(*alle_cursisten, sep='\n')
print('\n')
# Zoeken op ID
cursist_twee = Cursist.query.get(2)
print(cursist_twee)
print(cursist_twee.leeftijd)
print('\n')
# Filteren op naam cursist  WERKT MOMENTEEL NIET
# cursist_elsje = Cursist.query.filter_by(naam='Elsje')
# print(cursist_elsje)
# print('\n')
###########################
###### UPDATE ############
#########################

# Zoek het juiste record, wijzig het en leg de aanpassing vast.
cursist_joyce = Cursist.query.get(1)
cursist_joyce.leeftijd = 40
db.session.add(cursist_joyce)
db.session.commit()

###########################
###### DELETE ############
#########################
cursist_elsje = Cursist.query.get(3)
print (cursist_elsje)
db.session.delete(cursist_elsje)
db.session.commit()

# Overzicht na alle aanpassingen:
alle_cursisten = Cursist.query.all()
print(*alle_cursisten, sep='\n')
