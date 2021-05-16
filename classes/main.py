from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi_Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("MegaElixir", "M-elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

spells = [fire, thunder, blizzard, meteor, quake, cure, cura]

items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
         {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
         {"item": hielixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Giant        :", 3760, 65, 60, 34, spells, items)
player2 = Person("Cheese-It Man:", 4160, 65, 60, 34, spells, items)
player3 = Person("Dragon       :", 3970, 65, 60, 34, spells, items)
enemy = Person("Magnus", 12000, 65, 180, 25, [], [])

players = [player1, player2, player3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=====================================================================")
    print("\nNAME                    HP                               MP")

    for player in players:
        player.get_stats()

    for player in players:
        print("\n")
        player.choose_action()
        choice = input("Choose Action: ")
        index = int(choice) - 1

        if index==0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(bcolors.BOLD +"You attacked for", dmg, "amount of damage." + bcolors.ENDC)
        elif index==1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic: ")) - 1

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals for", str(magic_dmg) + bcolors.ENDC)
                if player.get_hp() > player.get_max_hp():
                    player.hp = player.get_max_hp()
            elif spell.type == "black":
              enemy.take_damage(magic_dmg)
              print(bcolors.OKBLUE + str(spell.name), "dealt", magic_dmg, "damage." + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                   player.heal(item["item"].prop)
                   print(bcolors.OKGREEN + item.name + " heals", item.prop, " health.")
                   if player.get_hp() > player.get_max_hp():
                    player.hp = player.get_max_hp()
            elif item.type == "elixir":
                   player.hp = player.get_max_hp()
                   player.mp = player.maxmp
                   print(bcolors.OKGREEN + item.name + " fully restores HP\MP." + bcolors.ENDC)
            elif item.type == "M-elixir":
                player1.hp = player1.get_max_hp()
                player1.mp = player1.maxmp
                player2.hp = player2.get_max_hp()
                player2.mp = player2.maxmp
                player3.hp = player3.get_max_hp()
                player3.mp = player3.maxmp
                print(bcolors.OKGREEN + item.name + " fully restores HP\MP of al." + bcolors.ENDC)
            elif item.type == "attack":
                   enemy.take_damage(item.prop)
                   print(bcolors.OKGREEN + item.name + " deals " + str(item.prop) + " damage." + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player1.take_damage(enemy_dmg)
    print(bcolors.FAIL + "Enemy attacked for", enemy_dmg, "amount of damage." + bcolors.ENDC)

    print("------------------------------")
    print("Enemy HP:" + bcolors.FAIL + str(enemy.get_hp()), "/", str(enemy.get_max_hp()) + bcolors.ENDC)

    if player.get_hp()==0:
       print("*******************************")
       print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
       running = False
    elif enemy.get_hp()==0:
       print("*******************************")
       print(bcolors.OKGREEN + "You won!" + bcolors.ENDC)
       running = False