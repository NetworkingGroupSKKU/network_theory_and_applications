__author__ = 'IoT/WSNs Team'
from copy import deepcopy
import random
DyR = 0.5 # prob. to switch to the new item when it has equal covering set with the current max-covering item
MuR = 0.2 # probability of NOT assigning new value to maxTemp when the new value is better than the current value
item_color = {'Ambank': set(['Celadon green', 'Blast-off bronze', 'Dark turquoise', 'Carmine (M&P)', 'Brick red', 'Dark sea green', 'Carmine', 'Atomic tangerine', 'French blue', 'Cyan cobalt blue', 'Donkey brown', 'Air Force blue (RAF)', 'Army green', 'Coquelicot', 'French plum', 'Celadon', 'Eton blue', 'Black bean', 'Bistre brown', 'Debian red', 'Bittersweet', 'Dark liver (horses)', 'Air Force blue (USAF)', 'Baby blue', 'Chocolate (web)', 'Arylide yellow', 'Deep Tuscan red', 'Bondi blue', 'Dark brown', 'Baby powder']), 'Tsingtao': set(['Catalina blue', 'Flavescent', 'Black', 'Burnt sienna', 'Ceil', 'English violet', 'Bisque', 'Azure (web color)', 'Bright pink', 'Cyan cobalt blue', 'Blue (pigment)', 'Charleston green', 'Chrome yellow', 'Amazon', 'Cyan-blue azure', 'Boysenberry', 'Dust storm', 'Desire', 'Dark jungle green', 'Desert sand', 'Antique ruby', 'Coral', 'Fern green', 'Desaturated cyan', 'Chartreuse (traditional)', 'Dim gray', 'Dark cerulean', 'Burnt orange', 'Cadet', 'Air Force blue (USAF)', 'Almond', 'Blue (NCS)', 'Cobalt Blue', 'British racing green', 'Deep magenta', 'Carrot orange', 'Cream']), 'Yamaha': set(['Deep carmine', 'Coffee', 'Dark pink', 'Cadmium red', 'French pink', 'Cordovan', 'Emerald']), 'Konica': set(['Dogwood rose', 'Blue (Munsell)', 'Cherry', 'Carolina blue', 'Dark tangerine', 'Deep moss green', 'Chocolate (traditional)', 'Azure mist', 'Blue-gray', 'Atomic tangerine', 'Blanched almond', 'Dark scarlet', 'Cyber yellow', 'Fluorescent yellow', 'Deep mauve', 'Baby pink', 'Desire', 'Dark jungle green', 'French beige', 'French sky blue', 'Beau blue', 'Aqua', 'Amaranth red', 'Chartreuse (traditional)', 'Eggplant', 'French raspberry', 'Electric yellow', 'Cool grey', 'Deep cerise', 'Dark imperial blue', 'Fawn', 'Cadet', 'Fuchsia purple', 'Forest green (traditional)', 'Artichoke', 'Bondi blue', 'Beaver']), 'LG': set(['Dark raspberry', 'French wine', 'Chinese red', 'Cerise', 'Antique fuchsia', 'Bronze Yellow', 'French blue', 'French mauve', 'Blue (pigment)', 'Flax', 'Cordovan', 'Bulgarian rose', 'Dark slate gray', 'Barbie pink', 'Desert', 'Azureish white', 'Amber (SAE/ECE)', 'Emerald', 'Cadmium green', 'Dark pastel red', 'Deep Red', 'Electric yellow', 'Deep cerise', 'Denim', 'Arylide yellow', 'Artichoke', 'French sky blue', 'Firebrick', 'Cal Poly green']), 'Epson': set(['Deep spring bud', 'Brilliant azure', 'Carmine red', 'Cadet grey', 'Camouflage green', 'Air superiority blue', 'Cinereous', 'Antique fuchsia', 'Bright cerulean', 'Buff', 'Ball blue', 'Atomic tangerine', 'Coral red', 'Dark pastel green', 'Cyan cobalt blue', 'Bistre', 'Charleston green', 'Carnelian', 'Baby pink', 'Bubbles', 'Deep chestnut', 'Bronze', 'Deep ruby', 'Boston University Red', 'Dark byzantium', 'Folly', 'Dark moss green', 'Chartreuse (traditional)', 'Beige', 'Cambridge Blue', 'Dark khaki', 'Coconut', 'Deep pink', 'Cotton candy', 'Dirt', 'Cobalt Blue', 'Dodger blue', 'Baby powder', 'French fuchsia']), 'Nexen': set(['Blue yonder', 'Deep jungle green', 'Carolina blue', 'Dark scarlet', 'Azure (web color)', 'Dandelion', 'Dark electric blue', 'Electric purple', 'French lime', 'Bright lavender', 'Cyber yellow', 'Cadmium yellow', 'Black olive', 'Catawba', 'Burnt umber', 'Blue Bell', 'Desert sand', 'Chestnut', 'English lavender', 'Copper', 'Coquelicot', 'Electric lime', 'English green', 'Desaturated cyan', 'Cinnabar', 'Beige', 'Eminence', 'Dark imperial blue', 'Amber', 'CG Red', 'Coconut', 'Boysenberry', 'Cadmium orange', 'Charm pink', 'Cyan azure', 'Chamoisee', 'Auburn', 'Dark pink', 'Deep coffee', 'Dark brown', 'French fuchsia']), 'Hana': set(['Celestial blue', 'Dark raspberry', 'Amaranth deep purple', 'Capri', 'Carmine', 'Ceil', 'Dutch white', 'Diamond', 'Baker-Miller pink', 'Deep spring bud', 'Chrome yellow', 'Black olive', 'Dark liver', 'Barbie pink', 'Feldgrau', 'Daffodil', 'Beau blue', 'Copper', 'Caput mortuum', 'Dark moss green', 'Amaranth red', 'Cinnabar', 'French bistre', "Big Dip O'ruby", 'Deep Green', 'Cambridge Blue', 'Bittersweet', 'Cadet blue', 'Dark coral', 'Firebrick', 'Dark salmon', 'Deep Tuscan red', 'British racing green', "B'dazzled blue"]), 'Honda': set(['Asparagus', 'Cyan cornflower blue', 'Chrome yellow']), 'Hyundai': set(['Azure (web color)', 'Brown Yellow', 'Bright pink', 'Boston University Red', 'Celeste', 'Blue (pigment)', 'Bright lavender', 'Crimson', 'Diamond', 'Antique white', 'Brunswick green', 'Fandango', 'Antique bronze', 'Electric yellow', 'Blueberry', 'Deep ruby']), 'Olympus': set(['Cornflower blue', 'Dark jungle green', 'Air Force blue (USAF)', 'Beau blue', 'Carnation pink', 'Donkey brown', 'Dark gray (X11)', 'Deep Tuscan red', 'Artichoke', 'Electric lavender', 'Cyan-blue azure', 'Bubbles', 'Caribbean green']), 'Alibaba': set(['Dark powder blue', 'Fulvous', 'Fluorescent orange', 'Dartmouth green', 'Blue-magenta violet', 'Copper penny', 'Camouflage green', 'Brown (traditional)', 'Bisque', 'Dim gray', 'Bitter lemon', 'Bright lavender', 'Antique white', 'Deep mauve', 'Brass', 'English green', 'Folly', 'Bright ube', 'Anti-flash white', 'Burgundy', 'Amaranth pink', 'Electric lavender', 'Charm pink', 'French lilac', 'Chamoisee', 'Cobalt Blue', 'Dark slate blue', 'Alabama crimson', 'China pink', 'Columbia Blue']), 'Astro': set(['Eggshell', 'Aureolin', 'Cerise pink', 'Bitter lime', 'American rose', 'Barn red', 'Fuchsia (Crayola)', 'Classic rose', 'Cyan cobalt blue', 'Asparagus', 'Emerald', 'Electric ultramarine', 'Desert', 'Bronze', 'Desert sand', 'Bright maroon', 'Cocoa brown', 'Fuchsia pink', 'Citron', 'Blue (Crayola)', 'Cyan azure', 'Deep jungle green', 'Dark slate blue', 'Claret', 'Electric green']), 'Casio': set(['Brown (web)', 'Alloy orange', 'Burgundy', 'Copper penny', 'Bitter lime', 'Champagne', 'Blue-gray', 'Coral red', 'Bitter lemon', 'Arctic lime', 'Bright lavender', 'Chrome yellow', 'Black olive', 'Dark cerulean', 'French bistre', 'Electric ultramarine', 'Falu red', 'Dust storm', 'Air Force blue (RAF)', 'Cool Black', 'Coquelicot', 'Aqua', 'French plum', 'Dark orchid', 'Eton blue', 'Diamond', 'Aero blue', 'Dark pastel red', 'Cedar Chest', 'Bone', 'Cambridge Blue', 'Bittersweet', 'Electric indigo', 'Crimson red', 'Dark puce']), 'Arirang': set(['Bangladesh green', 'Carmine red', 'Camouflage green', 'Crimson', 'Bronze Yellow', 'Deep chestnut', 'Blush', 'Byzantine', 'French blue', 'Dark candy apple red', 'Fashion fuchsia', 'Chinese violet', 'Dark taupe', 'Brass', 'Flattery', 'Bronze', 'Fawn', 'French beige', 'Dark byzantium', 'Dark khaki', "Big Dip O'ruby", 'Bright turquoise', 'Deep fuchsia', 'Caribbean green', 'Amaranth purple', 'Cambridge Blue', 'CG Red', 'Coconut', 'Citron', 'Deep puce', 'Dark salmon', 'Dark slate blue', 'Dark puce', 'Bondi blue', 'British racing green', 'Dark brown', 'Amethyst']), 'Nintendo': set(['Amaranth deep purple', 'Fuchsia', 'Brick red', 'Air superiority blue', 'Buff', 'Dark pastel green', 'Cyber yellow', 'Dark chestnut', 'Bisque', 'Dark taupe', 'Boysenberry', 'Blue sapphire', 'Army green', 'Coral', 'Cyber grape', 'Fallow', 'French wine', 'Deep carrot orange', 'Deep Red', 'Cedar Chest', 'Dark imperial blue', 'Amber', 'Ferrari Red', 'Carmine pink', 'French pink', 'Forest green (web)', 'French fuchsia', 'Copper (Crayola)']), 'Sony': set(['Celadon blue', 'English red', 'Cornell Red', 'Carmine', 'Blueberry', 'Classic rose', 'Bole', 'Byzantine', 'Dandelion', 'Copper red', 'Electric purple', 'Byzantium', 'Amazon', 'Cadmium yellow', 'Dark cerulean', 'Bleu de France', 'Bubbles', 'Bronze', 'Banana yellow', 'Cool Black', 'Asparagus', 'Blue-violet', 'Brilliant lavender', 'Cerulean', 'Caribbean green', 'Bulgarian rose', 'Dark midnight blue', 'Dark orange', 'Camel', 'French pink', 'Cobalt Blue', 'Feldspar', 'Black leather jacket', 'Electric green']), 'Hansol': set(['Dark gunmetal', 'Fulvous', 'English red', 'Crimson red', 'Carmine (M&P)', 'Citrine', 'Chocolate (traditional)', 'Blizzard Blue', 'Azure (web color)', 'Charcoal', 'Arctic lime', 'Dark liver', 'Apricot', 'Antique bronze', 'Dark sienna', 'French beige', 'Dark byzantium', 'Baby blue eyes', 'Android green', 'English green', 'Bottle green', 'Dark imperial blue', 'Bittersweet', 'Fire engine red', 'Celeste', 'Alabama crimson', 'Bondi blue']), 'Daewoo': set(['Cyber yellow', 'Dim gray', 'Chinese violet', 'Ferrari Red', 'Dark imperial blue']), 'Lenovo': set(['Deep sky blue']), 'Maxxis': set(['Dark red', 'Dark lava', 'Air superiority blue', 'Barn red', 'Ball blue', 'Diamond', 'Bole', 'French pink', 'Corn', 'Copper rose', 'Dark terra cotta', 'Azure mist', 'French bistre', 'Bubbles', 'Deep peach', 'Bronze', 'French beige', 'Deep Space Sparkle', 'Anti-flash white', 'Deep carrot orange', 'Dark green', 'Cambridge Blue', 'Flirt', 'Blue (Crayola)', 'Artichoke', 'Baby powder']), 'Samsung': set(['Cerulean blue', 'Flax', 'Cameo pink', 'Bright green', 'Dark cerulean', 'Cerulean frost']), 'Nissan': set(['Amaranth deep purple', 'Blue yonder', 'Aureolin', 'American rose', 'Flamingo pink', 'Coffee', 'Aqua', 'Deep spring bud', 'Flax', 'Apricot', 'Deep lilac', 'Bright ube', 'Blue-green', 'Black bean', 'Flame', 'Floral white', 'Cerulean', 'Dark orange', 'Coconut', 'Antique bronze', 'Chocolate (web)', 'Crimson glory']), 'Toyota': set(['Fluorescent orange', 'Fresh Air', 'Burlywood', 'Carmine red', 'Dark tangerine', 'Bitter lemon', 'Deep carmine pink', 'Barbie pink', 'Deep ruby', 'Brown Yellow', 'Air Force blue (RAF)', 'Desert sand', 'Apricot', 'Daffodil', 'Anti-flash white', 'Cocoa brown', 'Cadmium green', 'Dark pastel red', 'Egyptian blue', 'Amaranth purple', 'Acid green', 'Deep pink']), 'Fujitsu': set(['Catalina blue', 'Avocado', 'Buff', 'Blanched almond', 'Ceil', 'Cyan (process)', 'Dark slate gray', 'Deep lilac', 'Eucalyptus', 'Dark moss green', 'Flirt', 'Blue-violet', 'Eggplant', 'Azure', 'Electric yellow', 'Boysenberry', 'Cyan cornflower blue', 'Dollar bill', 'Deep jungle green', 'Alabama crimson', 'Brunswick green', 'Carrot orange', 'Copper (Crayola)', 'Ebony']), 'Mitsubishi': set(['Catalina blue', 'Dogwood rose', 'Alloy orange', 'Dark goldenrod', 'Capri', 'Cameo pink', 'Cornsilk', 'Azure mist', 'Coral red', 'Dandelion', "Davy's grey", 'Bistre', 'Arctic lime', 'Deep carmine pink', 'Chinese violet', 'Dark midnight blue', 'Drab', 'Bleu de France', 'Dark purple', 'Bubbles', 'Asparagus', 'Bottle green', 'Aero blue', 'Debian red', 'Bulgarian rose', 'Dark imperial blue', 'Dark coral', 'Forest green (web)', 'Bondi blue', 'Electric purple']), 'Sharp': set(['Deep spring bud', 'Celadon green', 'Bangladesh green', 'Bright lilac', 'Dark goldenrod', 'Crimson red', 'Earth yellow', 'China rose', 'Blueberry', 'Alice blue', 'Aero', 'Donkey brown', 'Dark chestnut', 'Cadmium yellow', 'Dark slate gray', 'Celadon blue', 'Electric blue', 'Beau blue', 'Android green', 'Black bean', 'Beige', 'Cocoa brown', 'Amaranth pink', 'Blue (RYB)', 'Bone', 'Fuchsia purple', 'Fawn', 'Dark orange', 'Carmine pink', 'Deer', 'Alabama crimson', 'Black leather jacket', 'Field drab']), 'Asus': set(['Byzantine', 'Cyber yellow', 'Celeste', 'Banana Mania', 'Amaranth', 'Cameo pink', 'Cornsilk']), 'Ottogi': set(['Dark cyan', 'Celadon blue', 'Alloy orange', 'Blue (Munsell)', 'Coyote brown', 'Aureolin', 'Capri', 'Chinese red', 'Carolina blue', 'Amethyst', 'Bright green', 'Carmine', 'Cameo pink', 'American rose', 'Cinereous', 'Bronze Yellow', 'Barn red', 'Azure (web color)', 'Cyan (process)', 'Carnelian', 'Dark slate gray', 'Banana yellow', 'Dark jungle green', 'Amber (SAE/ECE)', 'Alice blue', 'Dark spring green', 'Coral', 'Fern green', 'Cyber grape', 'Electric cyan', 'Floral white', 'Cool Black', 'French raspberry', 'Deep cerise', 'Cambridge Blue', 'Fluorescent pink', 'Battleship grey', 'China pink', 'Dark lavender', 'Auburn', 'French lilac', 'Crimson glory', 'French rose']), 'Singha': set(['Bangladesh green', 'Dark blue', 'Black', 'Deep green-cyan turquoise', 'Aquamarine', 'Cameo pink', 'Deep moss green', 'Coral red', 'Dark blue-gray', 'Arctic lime', 'Drab', 'Antique brass', 'Alabama crimson', 'Desire', 'Dark byzantium', 'Air superiority blue', 'Brown-nose', 'Cadmium orange', 'Air Force blue (USAF)', 'China pink', 'Firebrick', 'Claret']), 'Mazda': set(['Dark red', 'Blue yonder', 'Dartmouth green', 'Cadet grey', 'Dark tangerine', 'Bitter lime', 'Cornsilk', 'Chestnut', 'Brilliant rose', 'Bole', 'Bitter lemon', 'Bistre', 'Flax', 'Cyber yellow', 'Emerald', 'Dark olive green', 'Baby pink', 'Cambridge Blue', 'Cafe au lait', 'Bottle green', 'Black bean', 'Floral white', 'Deep carrot orange', 'Electric yellow', 'Bone', 'Amber', 'CG Red', 'AuroMetalSaurus', 'Dark gray (X11)', 'Cobalt Blue', 'Apple green', 'Baby powder']), 'Apollo': set([]), 'Canon': set(['Fandango pink', 'Cosmic latte', 'Dark gunmetal', 'Dark brown-tangelo', 'Alloy orange', 'Alizarin crimson', 'Bright lilac', 'Blue yonder', 'Ao (English)', 'Carmine (M&P)', 'Dark green (X11)', 'Aquamarine', 'Bright navy blue', 'Cerulean frost', 'Dark pastel green', 'Bistre', 'Flax', 'Bright lavender', 'Cool grey', 'Desert sand', 'Fluorescent yellow', 'Dark turquoise', 'Bubbles', 'Burnt umber', 'Celadon blue', 'Asparagus', 'Brandeis blue', 'Fuchsia', 'Desaturated cyan', "Big Dip O'ruby", 'Eggplant', 'Cedar Chest', 'Cadet', 'Boysenberry', 'Copper penny', 'Dark blue', 'Cobalt Blue', 'Antique brass', 'Blond', 'Beaver', 'Electric green', 'Copper (Crayola)', 'Cream']), 'Nikon': set(['Eucalyptus']), 'SK': set(['Brown (web)', 'Blue Lagoon', 'Cadet grey', 'Flamingo pink', 'Dutch white', 'Cerulean frost', 'Fuchsia (Crayola)', 'Copper red', 'Ash grey', 'Barn red', 'French bistre', 'Dark purple', 'Blue Bell', 'Brown-nose', 'Amaranth red', 'Flame', 'Aero blue', 'Deep koamaru', 'Fuchsia pink', 'Fire engine red', 'Battleship grey', 'Denim']), 'Hitachi': set(['Blue (Pantone)', 'Blue-gray', 'Coral red', 'Electric indigo', 'Blast-off bronze', 'CG Red', 'Baby blue eyes', 'Alizarin crimson', 'Fluorescent orange', 'Cordovan', 'Brown-nose', 'African violet', 'Anti-flash white', 'Fallow', 'Dodger blue', 'Amethyst', 'Cyber grape', 'Carmine', 'Dark pastel red', 'Deep maroon']), 'Acer': set(['Antique fuchsia', 'Cherry blossom pink', 'Caput mortuum', 'Bottle green', 'Dark scarlet', 'Deep aquamarine', 'Deep Space Sparkle', 'Antique bronze']), 'Lexus': set(['Cyan cornflower blue']), 'Kumho': set(['Bittersweet shimmer', 'Brown (web)', 'Cornell Red', 'Feldgrau', 'Eerie black', 'Earth yellow', 'Cornsilk', 'Fuchsia (Crayola)', 'Deep carmine', 'Dim gray', 'Deep carmine pink', 'Deep lemon', 'Catawba', 'Electric blue', 'Folly', 'Dark violet', 'Dark pastel blue', 'Flirt', 'Black bean', 'Floral white', 'Deep koamaru', 'Cool grey', 'Ferrari Red', 'Forest green (web)', 'British racing green']), 'Panasonic': set(['Fawn', 'China rose', 'AuroMetalSaurus', 'Burlywood', 'Bangladesh green', 'Blue-green', 'British racing green', 'Blue Lagoon', 'Bluebonnet', 'Capri', 'Bondi blue', 'Aquamarine', 'Bisque'])}
colorPool = set([])
itemPool = []
testlist = ['Canon', 'Ottogi', 'Arirang', 'Nexen', 'Tsingtao', 'Sharp', 'Casio', 'LG', 'Maxxis', 'Hana', 'Kumho', 'Hansol', 'Epson', 'Fujitsu', 'Alibaba', 'Ambank', 'Sony', 'Mazda', 'SK', 'Singha', 'Toyota', 'Hitachi', 'Astro', 'Konica', 'Acer', 'Yamaha', 'Olympus', 'Asus', 'Panasonic', 'Nintendo', 'Mitsubishi', 'Hyundai', 'Lenovo', 'Samsung']
for item in item_color:
    colorPool.update(item_color[item])      #add colors belong to each brand name (item) to the set
    itemPool.append(item)                   #add item name to the list

def are_exclusive(keys, items):
    "this is to check if for key k in keys, items[k]s have common values or not\
    keys is a list of keys items is a list of items\
    usage: are_exclusive(list_of_keys, item_color)"
    for i in range(0,len(keys)-2):
        for j in range(i+1,len(keys)-1):
            if len(items[keys[i]] & items[keys[j]]) > 0:
                print "Set", keys[i],"and",keys[j],"consist of common values:", items[keys[i]] & items[keys[j]],
                #return 0                    # any pair of keys that have common value => return 1
    else:
        return True                            # return 1 means exclusive (good)
def union(keys, items):
    "This is to find the union set of all the items which indexes in keys\
    usage:    union(list_of_keys,dictionary)\
    "
    u = set([])
    for key in keys:
        u = u | items[key]
    return u

def find_max_set(itemSet, colorSet):
    "This function is to find the set that its colors having max intersection with the colorSet"
    maxTemp = itemSet[0]
    for item in itemSet:
        if len(item_color[item] & colorSet) > len(item_color[maxTemp] & colorSet):
            if random.random() > MuR:
                maxTemp = item
        elif len(item_color[item] & colorSet) == len(item_color[maxTemp] & colorSet):
            if random.random() < DyR:
                maxTemp = item
    return maxTemp
def max_inclusive():
    "This is to count the number of max cover inclusive, print out the set of brand names that cover all"
    print "-----------Finding max inclusive set-------------"
    itemPool_temp = deepcopy(itemPool)          # clone and store in a temporal pool list
    colorPool_temp = deepcopy(colorPool)        # put all colors in a set Pool
    #print itemPool_temp
    selected_max_inclusive = []                 # a list of selected items
    while len(colorPool_temp) > 0:
        max_cardin = find_max_set(itemPool_temp, colorPool_temp)    # find the max intersection with the current color Pool
        colorPool_temp = colorPool_temp - item_color[max_cardin]    # substract the colors covered by the max_cardin from the color Pool
        itemPool_temp.remove(max_cardin)                            # remove the max_cardin from the item Pool
        selected_max_inclusive.append(max_cardin)                   # put the max_cardin into the selected set
    print "Selected max inclusive:", selected_max_inclusive
    print "Number of colors covered:",len(union(selected_max_inclusive,item_color))
    print "Number of items to cover all the color set:",len(selected_max_inclusive)
    print colorPool
    #print "Items in the inclusive is inclusive? ", are_exclusive(selected_max_inclusive,item_color),
    #-------------------------------------------------------------------------------------

def max_exclusive():
    #"This is to count the number of max cover inclusive, print out the set of brand names that cover all"
    print "-----------Finding max exclusive set-------------"
    itemPool_temp = deepcopy(itemPool)          # clone and store in a temporal pool
    colorPool_temp = deepcopy(colorPool)        # put all colors in a set Pool
    selected_max_exclusive = []                 # a list of selected items

    while len(itemPool_temp) > 0:
        max_cardin = find_max_set(itemPool_temp, colorPool_temp)    # find the max intersection with the current color Pool
        print max_cardin
        colorPool_temp = colorPool_temp - item_color[max_cardin]    # substract all colors of the item from the color Pool
        selected_max_exclusive.append(max_cardin)                   # add item to the selected list
        #    print len(itemPool_temp)
        itemPool_temp.remove(max_cardin)
        #here remove all items that have common color values with the selected item (to satisfy the 'exclusive' requirement)
        tobeRemoved = []
        for item in itemPool_temp:
            if len(item_color[item] & item_color[max_cardin]) > 0:
                tobeRemoved.append(item)
        print "Do oi co chung nay so bi remove co ma:",len(union(tobeRemoved,item_color))
        for item_r in tobeRemoved:
            print "Removing",item_r
            itemPool_temp.remove(item_r)
        print "End of one iteration============================="

    print "Selected max exclusive: ",selected_max_exclusive
    print "Number of brand names:",len(selected_max_exclusive),"covering:",len(union(selected_max_exclusive,item_color)),"colors"
    print "Colors:", union(selected_max_exclusive,item_color)
    print "Items in the exclusive is exclusive?", are_exclusive(selected_max_exclusive, item_color)
#-------------------------------------------------------------------------------------

def max_k_inclusive(k):
    #Max k inclusive
    t = 0
    itemPool_temp = deepcopy(itemPool)          # clone and store in a temporal pool
    colorPool_temp = deepcopy(colorPool)        # put all colors in a set Pool
    selected_k_inclusive = []                   # a list of selected items

    print "------------Finding max k-inclusive set------------"
    while (t < k):
        max_cardin_k = find_max_set(itemPool_temp, colorPool_temp)  # find the max intersection with the current color Pool
        if len(colorPool_temp) > 0:
            colorPool_temp = colorPool_temp - item_color[max_cardin_k]  # substract all colors of the item from the color Pool
            selected_k_inclusive.append(max_cardin_k)                   # put the max_cardin to the selected set
            itemPool_temp.remove(max_cardin_k)                          # remove from the Pool
            t += 1
        else:
            print "Max cover set reached at k =", t
            k = t
            break

    print "Selected", k, " items inclusive: ", selected_k_inclusive
    print "Number of covered colors:",len(union(selected_k_inclusive,item_color))
    print "Colors:", union(selected_k_inclusive,item_color)

while 1:
    print
    print
    print "There are",len(itemPool),"brand names, covering",len(colorPool),"colors"
    print "Select problem: "
    print "1. Max cover inclusive"
    print "2. Max cover exclusive"
    print "3. Max cover k"
    print "other. exit"
    sel = input("Your number:")
    if sel == 1:
        max_inclusive()
    elif sel == 2:
        max_exclusive()
    elif sel == 3:
        print "Please input k:"
        k = input()
        max_k_inclusive(k)
    else:
        break
