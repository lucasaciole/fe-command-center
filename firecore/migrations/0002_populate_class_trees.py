# Generated by Django 3.0.7 on 2020-06-09 18:59

from django.db import migrations

def create_tos_classes(apps, schema_editor):
	trees = ['Cleric','Swordsman','Scout', 'Archer', 'Wizard']
	classes = [
		['Priest','Krivis', 'Druid', 'Sadhu,',
		'Dievdirbys', 'Oracle','Monk','Pardoner', 'Paladin',
		'Chaplain', 'Plague Doctor', 'Kabbalist',
		'Inquisitor', 'Miko', 'Zealot', 'Exorcist', 'Crusader'],
		['Highlander', 'Petalsta', 'Hoplite', 'Barbarian', 'Cataphract',
		'Doppelsoeldner','Rodelero','Murmillo','Fencer', 'Dragoon',
		'Templar', 'Lancer', 'Matador', 'Nak Muay', 'Retiarus', 'Hackapell', 'Blossom Blader'],
		['Assassin','Outlaw','Squire','Corsair','Shinobi','Thauamturge', 'Enchanter','Linker',
		'Rogue','Schwazer Reiter','Bullet Marker', 'Ardito', 'Sheriff', 'Rangda'],
		['Hunter', 'Quarrel Shooter', 'Ranger', 'Sapper', 'Wugushi', 'Fletcher', 'Pied Piper',
		'Appraiser', 'Falconer', 'Canoneer', 'Musketeer', 'Mergen', 'Matros', 'Tiger Hunter',
		 'Arbalester'],
		['Pyromancer', 'Cryomancer', 'Psychokino', 'Alchemist', 'Sorcerer', 'Chronomancer',
		'Necromancer', 'Elementalist', 'Sage', 'Warlock', 'Featherfoot', 'Rune Caster',
		'Shadowmancer', 'Onmyoji', 'Taois', 'Bokor', 'Terramancer']
	]
	ClassTree = apps.get_model('firecore', 'ClassTree')
	Class = apps.get_model('firecore', 'Class')
	for tree, classes in zip(trees, classes):
		t = ClassTree(name=tree)
		t.save()
		for clss in classes:
			c = Class(name=clss,class_tree=t)
			c.save()

class Migration(migrations.Migration):

    dependencies = [
        ('firecore', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(create_tos_classes),
    ]
