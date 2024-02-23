from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from collections import Counter
from collections import namedtuple
from itertools import *
from openpyxl import load_workbook
from .forms import *
import random
import ast

all_words = ["cigar","rebut","sissy","humph","awake","blush","focal","evade","naval","serve","heath","dwarf","model","karma","stink","grade","quiet","bench","abate","feign","major","death","fresh","crust","stool","colon","abase","marry","react","batty","pride","floss","helix","croak","staff","paper","unfed","whelp","trawl","outdo","adobe","crazy","sower","repay","digit","crate","cluck","spike","mimic","pound","maxim","linen","unmet","flesh","booby","forth","first","stand","belly","ivory","seedy","print","yearn","drain","bribe","stout","panel","crass","flume","offal","agree","error","swirl","argue","bleed","delta","flick","totem","wooer","front","shrub","parry","biome","lapel","start","greet","goner","golem","lusty","loopy","round","audit","lying","gamma","labor","islet","civic","forge","corny","moult","basic","salad","agate","spicy","spray","essay","fjord","spend","kebab","guild","aback","motor","alone","hatch","hyper","thumb","dowry","ought","belch","dutch","pilot","tweed","comet","jaunt","enema","steed","abyss","growl","fling","dozen","boozy","erode","world","gouge","click","briar","great","altar","pulpy","blurt","coast","duchy","groin","fixer","group","rogue","badly","smart","pithy","gaudy","chill","heron","vodka","finer","surer","radio","rouge","perch","retch","wrote","clock","tilde","store","prove","bring","solve","cheat","grime","exult","usher","epoch","triad","break","rhino","viral","conic","masse","sonic","vital","trace","using","peach","champ","baton","brake","pluck","craze","gripe","weary","picky","acute","ferry","aside","tapir","troll","unify","rebus","boost","truss","siege","tiger","banal","slump","crank","gorge","query","drink","favor","abbey","tangy","panic","solar","shire","proxy","point","robot","prick","wince","crimp","knoll","sugar","whack","mount","perky","could","wrung","light","those","moist","shard","pleat","aloft","skill","elder","frame","humor","pause","ulcer","ultra","robin","cynic","aroma","caulk","shake","dodge","swill","tacit","other","thorn","trove","bloke","vivid","spill","chant","choke","rupee","nasty","mourn","ahead","brine","cloth","hoard","sweet","month","lapse","watch","today","focus","smelt","tease","cater","movie","saute","allow","renew","their","slosh","purge","chest","depot","epoxy","nymph","found","shall","stove","lowly","snout","trope","fewer","shawl","natal","comma","foray","scare","stair","black","squad","royal","chunk","mince","shame","cheek","ample","flair","foyer","cargo","oxide","plant","olive","inert","askew","heist","shown","zesty","trash","larva","forgo","story","hairy","train","homer","badge","midst","canny","shine","gecko","farce","slung","tipsy","metal","yield","delve","being","scour","glass","gamer","scrap","money","hinge","album","vouch","asset","tiara","crept","bayou","atoll","manor","creak","showy","phase","froth","depth","gloom","flood","trait","girth","piety","goose","float","donor","atone","primo","apron","blown","cacao","loser","input","gloat","awful","brink","smite","beady","rusty","retro","droll","gawky","hutch","pinto","egret","lilac","sever","field","fluff","agape","voice","stead","berth","madam","night","bland","liver","wedge","roomy","wacky","flock","angry","trite","aphid","tryst","midge","power","elope","cinch","motto","stomp","upset","bluff","cramp","quart","coyly","youth","rhyme","buggy","alien","smear","unfit","patty","cling","glean","label","hunky","khaki","poker","gruel","twice","twang","shrug","treat","waste","merit","woven","needy","clown","irony","ruder","gauze","chief","onset","prize","fungi","charm","gully","inter","whoop","taunt","leery","class","theme","lofty","tibia","booze","alpha","thyme","doubt","parer","chute","stick","trice","alike","recap","saint","glory","grate","admit","brisk","soggy","usurp","scald","scorn","leave","twine","sting","bough","marsh","sloth","dandy","vigor","howdy","enjoy","valid","ionic","equal","floor","catch","spade","stein","exist","quirk","denim","grove","spiel","mummy","fault","foggy","flout","carry","sneak","libel","waltz","aptly","piney","inept","aloud","photo","dream","stale","unite","snarl","baker","there","glyph","pooch","hippy","spell","folly","louse","gulch","vault","godly","threw","fleet","grave","inane","shock","crave","spite","valve","skimp","claim","rainy","musty","pique","daddy","quasi","arise","aging","valet","opium","avert","stuck","recut","mulch","genre","plume","rifle","count","incur","total","wrest","mocha","deter","study","lover","safer","rivet","funny","smoke","mound","undue","sedan","pagan","swine","guile","gusty","equip","tough","canoe","chaos","covet","human","udder","lunch","blast","stray","manga","melee","lefty","quick","paste","given","octet","risen","groan","leaky","grind","carve","loose","sadly","spilt","apple","slack","honey","final","sheen","eerie","minty","slick","derby","wharf","spelt","coach","erupt","singe","price","spawn","fairy","jiffy","filmy","stack","chose","sleep","ardor","nanny","niece","woozy","handy","grace","ditto","stank","cream","usual","diode","valor","angle","ninja","muddy","chase","reply","prone","spoil","heart","shade","diner","arson","onion","sleet","dowel","couch","palsy","bowel","smile","evoke","creek","lance","eagle","idiot","siren","built","embed","award","dross","annul","goody","frown","patio","laden","humid","elite","lymph","edify","might","reset","visit","gusto","purse","vapor","crock","write","sunny","loath","chaff","slide","queer","venom","stamp","sorry","still","acorn","aping","pushy","tamer","hater","mania","awoke","brawn","swift","exile","birch","lucky","freer","risky","ghost","plier","lunar","winch","snare","nurse","house","borax","nicer","lurch","exalt","about","savvy","toxin","tunic","pried","inlay","chump","lanky","cress","eater","elude","cycle","kitty","boule","moron","tenet","place","lobby","plush","vigil","index","blink","clung","qualm","croup","clink","juicy","stage","decay","nerve","flier","shaft","crook","clean","china","ridge","vowel","gnome","snuck","icing","spiny","rigor","snail","flown","rabid","prose","thank","poppy","budge","fiber","moldy","dowdy","kneel","track","caddy","quell","dumpy","paler","swore","rebar","scuba","splat","flyer","horny","mason","doing","ozone","amply","molar","ovary","beset","queue","cliff","magic","truce","sport","fritz","edict","twirl","verse","llama","eaten","range","whisk","hovel","rehab","macaw","sigma","spout","verve","sushi","dying","fetid","brain","buddy","thump","scion","candy","chord","basin","march","crowd","arbor","gayly","musky","stain","dally","bless","bravo","stung","title","ruler","kiosk","blond","ennui","layer","fluid","tatty","score","cutie","zebra","barge","matey","bluer","aider","shook","river","privy","betel","frisk","bongo","begun","azure","weave","genie","sound","glove","braid","scope","wryly","rover","assay","ocean","bloom","irate","later","woken","silky","wreck","dwelt","slate","smack","solid","amaze","hazel","wrist","jolly","globe","flint","rouse","civil","vista","relax","cover","alive","beech","jetty","bliss","vocal","often","dolly","eight","joker","since","event","ensue","shunt","diver","poser","worst","sweep","alley","creed","anime","leafy","bosom","dunce","stare","pudgy","waive","choir","stood","spoke","outgo","delay","bilge","ideal","clasp","seize","hotly","laugh","sieve","block","meant","grape","noose","hardy","shied","drawl","daisy","putty","strut","burnt","tulip","crick","idyll","vixen","furor","geeky","cough","naive","shoal","stork","bathe","aunty","check","prime","brass","outer","furry","razor","elect","evict","imply","demur","quota","haven","cavil","swear","crump","dough","gavel","wagon","salon","nudge","harem","pitch","sworn","pupil","excel","stony","cabin","unzip","queen","trout","polyp","earth","storm","until","taper","enter","child","adopt","minor","fatty","husky","brave","filet","slime","glint","tread","steal","regal","guest","every","murky","share","spore","hoist","buxom","inner","otter","dimly","level","sumac","donut","stilt","arena","sheet","scrub","fancy","slimy","pearl","silly","porch","dingo","sepia","amble","shady","bread","friar","reign","dairy","quill","cross","brood","tuber","shear","posit","blank","villa","shank","piggy","freak","which","among","fecal","shell","would","algae","large","rabbi","agony","amuse","bushy","copse","swoon","knife","pouch","ascot","plane","crown","urban","snide","relay","abide","viola","rajah","straw","dilly","crash","amass","third","trick","tutor","woody","blurb","grief","disco","where","sassy","beach","sauna","comic","clued","creep","caste","graze","snuff","frock","gonad","drunk","prong","lurid","steel","halve","buyer","vinyl","utile","smell","adage","worry","tasty","local","trade","finch","ashen","modal","gaunt","clove","enact","adorn","roast","speck","sheik","missy","grunt","snoop","party","touch","mafia","emcee","array","south","vapid","jelly","skulk","angst","tubal","lower","crest","sweat","cyber","adore","tardy","swami","notch","groom","roach","hitch","young","align","ready","frond","strap","puree","realm","venue","swarm","offer","seven","dryer","diary","dryly","drank","acrid","heady","theta","junto","pixie","quoth","bonus","shalt","penne","amend","datum","build","piano","shelf","lodge","suing","rearm","coral","ramen","worth","psalm","infer","overt","mayor","ovoid","glide","usage","poise","randy","chuck","prank","fishy","tooth","ether","drove","idler","swath","stint","while","begat","apply","slang","tarot","radar","credo","aware","canon","shift","timer","bylaw","serum","three","steak","iliac","shirk","blunt","puppy","penal","joist","bunny","shape","beget","wheel","adept","stunt","stole","topaz","chore","fluke","afoot","bloat","bully","dense","caper","sneer","boxer","jumbo","lunge","space","avail","short","slurp","loyal","flirt","pizza","conch","tempo","droop","plate","bible","plunk","afoul","savoy","steep","agile","stake","dwell","knave","beard","arose","motif","smash","broil","glare","shove","baggy","mammy","swamp","along","rugby","wager","quack","squat","snaky","debit","mange","skate","ninth","joust","tramp","spurn","medal","micro","rebel","flank","learn","nadir","maple","comfy","remit","gruff","ester","least","mogul","fetch","cause","oaken","aglow","meaty","gaffe","shyly","racer","prowl","thief","stern","poesy","rocky","tweet","waist","spire","grope","havoc","patsy","truly","forty","deity","uncle","swish","giver","preen","bevel","lemur","draft","slope","annoy","lingo","bleak","ditty","curly","cedar","dirge","grown","horde","drool","shuck","crypt","cumin","stock","gravy","locus","wider","breed","quite","chafe","cache","blimp","deign","fiend","logic","cheap","elide","rigid","false","renal","pence","rowdy","shoot","blaze","envoy","posse","brief","never","abort","mouse","mucky","sulky","fiery","media","trunk","yeast","clear","skunk","scalp","bitty","cider","koala","duvet","segue","creme","super","grill","after","owner","ember","reach","nobly","empty","speed","gipsy","recur","smock","dread","merge","burst","kappa","amity","shaky","hover","carol","snort","synod","faint","haunt","flour","chair","detox","shrew","tense","plied","quark","burly","novel","waxen","stoic","jerky","blitz","beefy","lyric","hussy","towel","quilt","below","bingo","wispy","brash","scone","toast","easel","saucy","value","spice","honor","route","sharp","bawdy","radii","skull","phony","issue","lager","swell","urine","gassy","trial","flora","upper","latch","wight","brick","retry","holly","decal","grass","shack","dogma","mover","defer","sober","optic","crier","vying","nomad","flute","hippo","shark","drier","obese","bugle","tawny","chalk","feast","ruddy","pedal","scarf","cruel","bleat","tidal","slush","semen","windy","dusty","sally","igloo","nerdy","jewel","shone","whale","hymen","abuse","fugue","elbow","crumb","pansy","welsh","syrup","terse","suave","gamut","swung","drake","freed","afire","shirt","grout","oddly","tithe","plaid","dummy","broom","blind","torch","enemy","again","tying","pesky","alter","gazer","noble","ethos","bride","extol","decor","hobby","beast","idiom","utter","these","sixth","alarm","erase","elegy","spunk","piper","scaly","scold","hefty","chick","sooty","canal","whiny","slash","quake","joint","swept","prude","heavy","wield","femme","lasso","maize","shale","screw","spree","smoky","whiff","scent","glade","spent","prism","stoke","riper","orbit","cocoa","guilt","humus","shush","table","smirk","wrong","noisy","alert","shiny","elate","resin","whole","hunch","pixel","polar","hotel","sword","cleat","mango","rumba","puffy","filly","billy","leash","clout","dance","ovate","facet","chili","paint","liner","curio","salty","audio","snake","fable","cloak","navel","spurt","pesto","balmy","flash","unwed","early","churn","weedy","stump","lease","witty","wimpy","spoof","saner","blend","salsa","thick","warty","manic","blare","squib","spoon","probe","crepe","knack","force","debut","order","haste","teeth","agent","widen","icily","slice","ingot","clash","juror","blood","abode","throw","unity","pivot","slept","troop","spare","sewer","parse","morph","cacti","tacky","spool","demon","moody","annex","begin","fuzzy","patch","water","lumpy","admin","omega","limit","tabby","macho","aisle","skiff","basis","plank","verge","botch","crawl","lousy","slain","cubic","raise","wrack","guide","foist","cameo","under","actor","revue","fraud","harpy","scoop","climb","refer","olden","clerk","debar","tally","ethic","cairn","tulle","ghoul","hilly","crude","apart","scale","older","plain","sperm","briny","abbot","rerun","quest","crisp","bound","befit","drawn","suite","itchy","cheer","bagel","guess","broad","axiom","chard","caput","leant","harsh","curse","proud","swing","opine","taste","lupus","gumbo","miner","green","chasm","lipid","topic","armor","brush","crane","mural","abled","habit","bossy","maker","dusky","dizzy","lithe","brook","jazzy","fifty","sense","giant","surly","legal","fatal","flunk","began","prune","small","slant","scoff","torus","ninny","covey","viper","taken","moral","vogue","owing","token","entry","booth","voter","chide","elfin","ebony","neigh","minim","melon","kneed","decoy","voila","ankle","arrow","mushy","tribe","cease","eager","birth","graph","odder","terra","weird","tried","clack","color","rough","weigh","uncut","ladle","strip","craft","minus","dicey","titan","lucid","vicar","dress","ditch","gypsy","pasta","taffy","flame","swoop","aloof","sight","broke","teary","chart","sixty","wordy","sheer","leper","nosey","bulge","savor","clamp","funky","foamy","toxic","brand","plumb","dingy","butte","drill","tripe","bicep","tenor","krill","worse","drama","hyena","think","ratio","cobra","basil","scrum","bused","phone","court","camel","proof","heard","angel","petal","pouty","throb","maybe","fetal","sprig","spine","shout","cadet","macro","dodgy","satyr","rarer","binge","trend","nutty","leapt","amiss","split","myrrh","width","sonar","tower","baron","fever","waver","spark","belie","sloop","expel","smote","baler","above","north","wafer","scant","frill","awash","snack","scowl","frail","drift","limbo","fence","motel","ounce","wreak","revel","talon","prior","knelt","cello","flake","debug","anode","crime","salve","scout","imbue","pinky","stave","vague","chock","fight","video","stone","teach","cleft","frost","prawn","booty","twist","apnea","stiff","plaza","ledge","tweak","board","grant","medic","bacon","cable","brawl","slunk","raspy","forum","drone","women","mucus","boast","toddy","coven","tumor","truer","wrath","stall","steam","axial","purer","daily","trail","niche","mealy","juice","nylon","plump","merry","flail","papal","wheat","berry","cower","erect","brute","leggy","snipe","sinew","skier","penny","jumpy","rally","umbra","scary","modem","gross","avian","greed","satin","tonic","parka","sniff","livid","stark","trump","giddy","reuse","taboo","avoid","quote","devil","liken","gloss","gayer","beret","noise","gland","dealt","sling","rumor","opera","thigh","tonga","flare","wound","white","bulky","etude","horse","circa","paddy","inbox","fizzy","grain","exert","surge","gleam","belle","salvo","crush","fruit","sappy","taker","tract","ovine","spiky","frank","reedy","filth","spasm","heave","mambo","right","clank","trust","lumen","borne","spook","sauce","amber","lathe","carat","corer","dirty","slyly","affix","alloy","taint","sheep","kinky","wooly","mauve","flung","yacht","fried","quail","brunt","grimy","curvy","cagey","rinse","deuce","state","grasp","milky","bison","graft","sandy","baste","flask","hedge","girly","swash","boney","coupe","endow","abhor","welch","blade","tight","geese","miser","mirth","cloud","cabal","leech","close","tenth","pecan","droit","grail","clone","guise","ralph","tango","biddy","smith","mower","payee","serif","drape","fifth","spank","glaze","allot","truck","kayak","virus","testy","tepee","fully","zonal","metro","curry","grand","banjo","axion","bezel","occur","chain","nasal","gooey","filer","brace","allay","pubic","raven","plead","gnash","flaky","munch","dully","eking","thing","slink","hurry","theft","shorn","pygmy","ranch","wring","lemon","shore","mamma","froze","newer","style","moose","antic","drown","vegan","chess","guppy","union","lever","lorry","image","cabby","druid","exact","truth","dopey","spear","cried","chime","crony","stunk","timid","batch","gauge","rotor","crack","curve","latte","witch","bunch","repel","anvil","soapy","meter","broth","madly","dried","scene","known","magma","roost","woman","thong","punch","pasty","downy","knead","whirl","rapid","clang","anger","drive","goofy","email","music","stuff","bleep","rider","mecca","folio","setup","verso","quash","fauna","gummy","happy","newly","fussy","relic","guava","ratty","fudge","femur","chirp","forte","alibi","whine","petty","golly","plait","fleck","felon","gourd","brown","thrum","ficus","stash","decry","wiser","junta","visor","daunt","scree","impel","await","press","whose","turbo","stoop","speak","mangy","eying","inlet","crone","pulse","mossy","staid","hence","pinch","teddy","sully","snore","ripen","snowy","attic","going","leach","mouth","hound","clump","tonal","bigot","peril","piece","blame","haute","spied","undid","intro","basal","rodeo","guard","steer","loamy","scamp","scram","manly","hello","vaunt","organ","feral","knock","extra","condo","adapt","willy","polka","rayon","skirt","faith","torso","match","mercy","tepid","sleek","riser","twixt","peace","flush","catty","login","eject","roger","rival","untie","refit","aorta","adult","judge","rower","artsy","rural","shave","bobby","eclat","fella","gaily","harry","hasty","hydro","liege","octal","ombre","payer","sooth","unset","unlit","vomit","fanny","fetus","butch","stalk","flack","widow","augur"]
input_array = []

Word_Tuple = namedtuple('Word_Tuple', ['word', 'count'])


def check(position, colour, value, word, attempt):
    if colour == "Green" and word[position] != value: return False
    if colour == "Grey":
        found = False
        for x in range(0,5):
            if word[x] == value:
                found = True
                if x != position and attempt[x][1] == "Green": found = False # It was found but green elsewhere
        if found:
            return False
    if colour == "Orange":
        found = False
        for x in range(0,5):
            if word[x] == value: found = True
        if word[position] == value: found = False
        if not found: return False
    return True

def determine_colours(word, entry):
    result = ["Grey", "Grey", "Grey", "Grey", "Grey"]
    for position in range(5):
        for x in range(5):
            if entry[position] == word[x]:
                result[position] = 'Orange'
        if entry[position] == word[position]:
            result[position] = "Green"
    return result

def count_same_letters(words):
    first_word = words[0]
    same_letters = 0
    for x in range(0, 5):
        same = True
        for word in words:
            if word[x] != first_word[x]: same = False
        if same: same_letters += 1
    return same_letters

def add_wordle(request, word):
    if not request.user.is_authenticated: return redirect("login")
    today = date.today()
    existing = Wordle.objects.filter(date=today).first()
    if existing:
        messages.success(request, f"'{existing.word.upper()}' already exists as today's word")
        return redirect("wordle")

    todays_wordle = Wordle.objects.filter(word=word).first()
    if todays_wordle:
        if todays_wordle.guess_2 is None: solve_wordle(todays_wordle)
        todays_wordle.date = today
        todays_wordle.save()
        messages.success(request, f"'{word}' recorded as today's word")
        affected_wordles = Wordle.objects.filter(guess_2=todays_wordle.guess_2, date__isnull=True)
        for wordle in affected_wordles:
            print("Affected word:", wordle)
            wordle.last_reviewed = None
            wordle.save()
    else:
        messages.success(request, f"'{word}' wasn't found in database")
    return redirect("wordle_test")

def wordle_clear(request, id):
    object = Wordle.objects.get(id=id)
    object.date = None
    object.save()
    return redirect('wordle')

def get_fav_word_simple(wordles):
    all_letters = ""
    for wordle in wordles:
        unique_letters = set(wordle.word)
        for letter in unique_letters:
            all_letters += letter
    counter = Counter(all_letters)
    highest_score = 0
    if len(wordles) > 0:    fav_word = wordles[0]
    else:                   fav_word = None

    for wordle in wordles:
        score = 0
        for letter in set(wordle.word): score += counter[letter]
        if score > highest_score:
            highest_score = score
            fav_word = wordle
    return fav_word


def get_fav_word(wordles):
    Wordle.objects.all().update(score=0)
    all_letters = ""
    for wordle in wordles:
        unique_letters = set(wordle.word)
        for letter in unique_letters:
            all_letters += letter
    counter = Counter(all_letters)

    if len(wordles) > 900:
        wordles = Wordle.objects.filter(Q(word="arose") | Q(word="later") | Q(word="alert") | Q(word="stare") | Q(word="arise"))

    highest_score = 0
    if len(wordles) > 0:
        fav_word = wordles[0]
    else:
        fav_word = None
    for wordle in wordles:
        score = 0
        for letter in set(wordle.word): score += counter[letter]
        wordle.score = score
        wordle.save()
        if score > highest_score:
            highest_score = score
            fav_word = wordle

    # Convert the counter into a list for django tags
    counter_list = []
    for key, value in counter.most_common(10): counter_list.append(f"{key.upper()}: {value}")

    return counter_list, fav_word

def get_valid_words(input_array, remaining_words=None):
    words = []
    if not remaining_words:
        remaining_words = Wordle.objects.filter(date__isnull=True)
    for word in remaining_words:
        valid = True
        for attempt in input_array:
            count = 0
            for letter, colour in attempt:
                if not check(count, colour, letter, word.word, attempt): valid = False
                count += 1
        if valid: words.append(word)
    return words

def solve_wordle(wordle):
    input_array.clear()
    remaining_words = Wordle.objects.filter(date__isnull=True)
    fav_word = remaining_words.filter(word="arise").first()
    attempts = [fav_word.word, ]
    while fav_word != wordle:
        input_row = []
        colours = determine_colours(wordle.word, fav_word.word)
        for x in range(5): input_row.append((fav_word.word[x], colours[x]))
        input_array.append(input_row)
        remaining_words = get_valid_words(input_array, remaining_words)
        fav_word = get_fav_word_simple(remaining_words)
        attempts.append(fav_word.word)
        # wordle.save_guess(fav_word, count)
        # Fav word is solved => save it.
        # fav_word.attempts = len(input_array) + 1
        # fav_word.last_reviewed = date.today()
        # fav_word.save()

    input_row = []
    colours = determine_colours(wordle.word, fav_word.word)
    for x in range(5): input_row.append((fav_word.word[x], colours[x]))
    input_array.append(input_row)

    if len(attempts) > 0: wordle.guess_1 = attempts[0]
    if len(attempts) > 1: wordle.guess_2 = attempts[1]
    if len(attempts) > 2: wordle.guess_3 = attempts[2]
    if len(attempts) > 3: wordle.guess_4 = attempts[3]
    if len(attempts) > 4: wordle.guess_5 = attempts[4]
    if len(attempts) > 5: wordle.guess_6 = attempts[5]
    wordle.attempts = len(input_array)
    wordle.last_reviewed = date.today()
    wordle.save()

def solve_wordle_old(wordle):
    input_array.clear()
    words = get_valid_words(input_array)
    # print("Solve wordle words:", words)
    counter, fav_word = get_fav_word(words)
    # wordle.save_guess(fav_word, 1)
    while fav_word != wordle:
        words = get_valid_words(input_array)
        counter, fav_word = get_fav_word(words)
        wordle.save_guess(fav_word, count)
        colours = determine_colours(wordle.word, fav_word.word)
        input = []
        for x in range(5): input.append((fav_word.word[x], colours[x]))
        input_array.append(input)
        # Fav word is solved => save it.
        fav_word.attempts = len(input_array)
        fav_word.last_reviewed = date.today()
        fav_word.save()

    wordle.attempts = len(input_array)
    wordle.last_reviewed = date.today()
    wordle.save()

def get_max_attempts():
    categories = Wordle.objects.values('attempts').annotate(count=Count('attempts'))
    max_attempts = 0
    for category in categories:
        if category['attempts']:
            if category['attempts'] > max_attempts: max_attempts = category['attempts']
    return max_attempts

def wordle_test(request, id=None):
    if not request.user.is_authenticated: return redirect("login")
    wordle = None
    # input_array = None

    # Solve a number of wordles that don't have a date
    if not id:
        wordles_to_do = General.objects.get(name="main").wordles_to_do
        wordles = Wordle.objects.filter(last_reviewed__isnull=True, date__isnull=True).order_by('-last_reviewed')[0:wordles_to_do]
        for wordle in wordles:
            if wordle:
                print(f"Redoing '{wordle.word.upper()}'")
                solve_wordle(wordle)

    # Solve the particular wordle requested
    if id:
        wordle = Wordle.objects.get(id=id)
        solve_wordle(wordle)

    wordles = Wordle.objects.filter(date__isnull=True).order_by('word')

    # Categorisation of attempts
    attempts_range = []
    categories = Wordle.objects.filter(date__isnull=True).values('attempts').annotate(count=Count('attempts'))
    no, total = 0, 0
    for category in categories:
        if category['attempts']:
            attempts_range.append((category['attempts'], category['count']))
            no += category['count'] * category['attempts']
            total += category['count']
    attempts_range = sorted(attempts_range, key=lambda x: x[0])
    score = round(no/total, 3)

    # Categorisation of second word
    categories_second_word = Wordle.objects.values('guess_2').annotate(count=Count('guess_2'))
    second_word_array = []
    for category in categories_second_word:
        second_word_array.append((category['guess_2'], category['count']))
    second_word_array_1 = sorted(second_word_array, key=lambda x: (x[1] is None, x[1]), reverse=True)[0: 10]
    second_word_array_2 = sorted(second_word_array, key=lambda x: (x[1] is None, x[1]), reverse=True)[10: 20]
    second_word_array_3 = sorted(second_word_array, key=lambda x: (x[1] is None, x[1]), reverse=True)[20: 30]

    remaining_words = Wordle.objects.filter(date__isnull=True)
    remaining_words_not_tested = remaining_words.filter(last_reviewed__isnull=True)
    message = f"Proportion of words tested: {int((1-len(remaining_words_not_tested)/len(remaining_words))*100)}% ({len(remaining_words) - len(remaining_words_not_tested)} of {len(remaining_words)})"
    hard_words = attempts_range[4][1] + attempts_range[5][1] + attempts_range[6][1]
    message_2 = f"Hard words: {hard_words} ({int(hard_words/len(remaining_words)*100)}%)"

    todays_word = Wordle.objects.filter(date__isnull=False).order_by('-date')

    if wordle:
        word = wordle.word.upper()
    else:
        word = None

    context = {'word': word, 'input_array': input_array, 'words': wordles, 'attempts_range': attempts_range,
               'remaining_words': remaining_words, 'score': score,
               'second_word_array_1': second_word_array_1, 'second_word_array_2': second_word_array_2, 'second_word_array_3': second_word_array_3,
               "message": message, "message_2": message_2,
               "todays": todays_word}
    return render(request, "wordle_test.html", context)

def wordle_second(request, word):
    wordle = Wordle.objects.get(word=word)
    wordles = Wordle.objects.filter(guess_2=word).order_by('-attempts')
    context = {"wordle": wordle, "wordles": wordles}
    return render(request, "wordle_second.html", context)

def wordle(request):
    if not request.user.is_authenticated: return redirect("login")

    # all_wordles = Wordle.objects.all()
    # for word in all_words:
    #     if len(all_wordles.filter(word=word)) == 0:
    #         print(f"{word.upper()} is missing.")
    #         Wordle(word=word).save()

    input_array = []

    # print("Start Input Array:", input_array)
    value = ["", "", "", "", "", ]
    colour = ["", "", "", "", "", ]

    if request.method == 'POST':
        # print("\nPrinting request post")
        for key, value_X in request.POST.items():
            # print(f"{key}: {value_X} {key[0:5]}")

            if key[0:5] == "Prior":
                array = ast.literal_eval(value_X)
                input_array.append(array)
        # print("Finished Printing request post\n")
        # print("Input array (pre):", input_array)

        numbers = ["1", "2", "3", "4", "5", ]
        for x in numbers:
            try:
                value[int(x) - 1] = request.POST.__getitem__(x).lower()
                colour[int(x)-1] = request.POST.__getitem__(str(x) + 'x')
            except:
                value[int(x) - 1] = ""
                colour[int(x) - 1] = ""

        # Load values
        input = []
        for x in range(5):
            input.append((value[x], colour[x]))
        valid = True
        for x, y in input:
            if x == "" or y == "": valid = False
        if valid:
            input_array.append(input)

    # Put remaining, valid words into 'words' list
    words = get_valid_words(input_array)

    # Get fav word
    counter, fav_word = get_fav_word(words)

    # Retrieve the words again (so that they have the new scores)
    words = Wordle.objects.filter(score__gte=1)
    random_item = Wordle.objects.filter(date__isnull=True).order_by('?').first()

    if fav_word: entry = list(fav_word.word)
    else: entry = list("arise")
    words = sorted(words, key=lambda x: x.score, reverse=True)
    green1, green2, green3, green4, green5 = "", "", "", "", "",
    numbers = ["1x","2x","3x","4x","5x",]

    print("Input array (post):", input_array)
    used_words = Wordle.objects.filter(date__isnull=False).order_by('-date')[0:10]

    context = {'words': words, 'numbers': numbers, 'fav_word': fav_word, 'input_array': input_array, 'counter': counter, 'random_item': random_item,
               'entry':entry, 'green1': green1, 'green2': green2, 'green3': green3, 'green4': green4, 'green5': green5, 'used_words': used_words}

    return render(request, 'wordle.html', context)

def clear(request):
    input_array.clear()
    return redirect("wordle")

def past_words(request):
    if not request.user.is_authenticated: return redirect("login")
    # workbook = load_workbook('excel/past_wordles.xlsx')
    # worksheet = workbook.worksheets[0]
    # for row in worksheet.iter_rows():
    #     date, word = row[0].value, row[1].value
    #     if word:
    #         word = word.lower()
    #         existing = Wordle.objects.filter(word=word).first()
    #         if not existing.date:
    #             existing.date = date
    #             existing.save()

    attempts_range = []
    remaining_words = Wordle.objects.filter(date__isnull=True).order_by('word')
    used_words = Wordle.objects.filter(date__isnull=False).order_by('-date')
    context = {'used_words': used_words, 'remaining_words': remaining_words}
    return render(request, "wordle_past.html", context)

def word(request):
    letters = ""
    if request.method == 'POST':
        letters = request.POST['text']
        print(letters)
    all_words = get_words(letters)
    context = {'letters': letters, 'all_words': all_words}
    return render(request, "word.html", context)

def get_words(letters):
    filename = "dictionary/dict.txt"
    words = set(x.strip() for x in open(filename))

    lengths = range(3, 10)
    all_words = []
    for length in lengths:
        words_interim = set()
        results = permutations(letters, length)
        for result in results:
            word = ""
            for letter in result: word += letter
            if word in words:
                words_interim.add(word)

        if len(words_interim) > 0:
            words_interim = sorted(words_interim)
            all_words.append(words_interim)

    return all_words



