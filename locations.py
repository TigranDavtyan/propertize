from bidict import bidict
from pprint import pprint

class LocationGroup:
    def __init__(self, groupname, districts: dict,  groupid = None):
        self.ID = groupid
        self.NAME = groupname
        self.districts = bidict(districts)

    def __getitem__(self, key):
        if type(key) == str or type(key) == LocationGroup:
            return self.districts[key]
        elif type(key) == int:
            return self.districts.inverse[key]
        else:
            raise ValueError(f'Inapropiate value for "key" = {key}')
        
    def __contains__(self, value):
        if type(value) == str:
            return value in self.districts or value == self.NAME
        elif type(value) == int:
            return value in self.districts.inverse or value == self.ID
        else:
            raise ValueError(f'Inapropiate value for "value" = {value}')
        
    def values(self):
        return self.districts.values()

    def keys(self):
        return self.districts.keys()

    def __setitem__(self, ):
        print('LocationGroup is immutable')

    def __iadd__(self, other):
        self.districts.update(other.districts)

    def __add__(self, other):
        ret = bidict()
        ret.update(self.districts)
        ret.update(other.districts)

        return LocationGroup(None, ret)
    def __str__(self):
        print(f'ID: {self.ID}  NAME: {self.NAME}')
        pprint(self.districts.__dict__['_fwdm'])

    def __hash__(self):
        return self.ID.__hash__()


YEREVAN = LocationGroup('Yerevan',{
     'Ajapnyak':2 ,
     'Arabkir':3 ,
     'Avan':4 ,
     'Davitashen':5 ,
     'Erebuni':6 ,
     'Kanaker-Zeytun':7 ,
     'Kentron':8 ,
     'Malatia-Sebastia':9 ,
     'Nor Nork':10,
     'Shengavit':13,
     'Nork-Marash':11,
     'Nubarashen':12},1)
ARMAVIR = LocationGroup('Armavir',{
    'Armavir':24 ,
    'Echmiadzin':25 ,
    'Argavand':155,
    'Baghramyan':162,
    'Merdzavan':137,
    'Metsamor':26 ,
    'Mrgashat':196,
    'Musaler':111,
    'Nalbandyan':199,
    'Parakar':101,
    'Tairov':105,
    'Aghavnatun':141,
    'Aknalich':142,
    'Aknashen':143,
    'Alashkert':144,
    'Amasia':145,
    'Amberd':146,
    'Apaga':147,
    'Aragats':148,
    'Araks':149,
    'Aratashen':150,
    'Arazap':151,
    'Arevadasht':152,
    'Arevashat':153,
    'Arevik':154,
    'Argina':156,
    'Arshaluys':157,
    'Artamet':158,
    'Artashar':159,
    'Artimet':160,
    'Aygek':161,
    'Aygeshat':831,
    'Bambakashat':163,
    'Dalarik':164,
    'Dasht':165,
    'Doghs':166,
    'Ferik':167,
    'Gai':168,
    'Geghakert':169,
    'Getashen':170,
    'Griboyedov':171,
    'Hatsik':172,
    'Haykashen':173,
    'Haykavan':174,
    'Haytagh':175,
    'Hovtamej':176,
    'Janfida':178,
    'Jrarat':179,
    'Jrarbi':180,
    'Jrashen':181,
    'Karakert':182,
    'Khanjyan':183,
    'Khoronk':184,
    'Koghbavan':185,
    'Lenughi':186,
    'Lukashin':189,
    'Lusagyugh':190,
    'Margara':191,
    'Mayisyan':192,
    'Mrgastan':195,
    'Myasnikyan':198,
    'No Armavir':201,
    'No Artagers':202,
    'No Kesaria':203,
    'Norakert':200,
    'Norapat':204,
    'Noravan':205,
    'Pshatavan':207,
    'Ptghunk':208,
    'Sardarapat':138,
    'Shahumyan':209,
    'Shenavan':210,
    'Shenik':211,
    'Tandzut':212,
    'Taronik':213,
    'Tsaghkalanj':214,
    'Tsaghkunk':215,
    'Tsiatsan':216,
    'Vanand':217,
    'Vardanashen':218,
    'Voskehat':219,
    'Yeghegnut':220,
    'Yeraskhahun':221,
    'Yervandashat':222,
    'Zartonk':223},23)
ARARAT = LocationGroup('Ararat',{
    'Artashat':21 ,
    'Abovyan':269,
    'Ararat':20 ,
    'Arbat':272,
    'Argavand':106,
    'Ayntap':99 ,
    'Azatashen':140,
    'Dashtavan':291,
    'Geghanist':80 ,
    'Getapnya':110,
    'Ghukasavan':296,
    'Hayanist':109,
    'Hovtashat':300,
    'Khachpar':305,
    'Marmarashen':309,
    'Masis':22 ,
    'Mkhchyan':310,
    'No Kharberd':100,
    'No Kyurin':316,
    'Vedi':86 ,
    'Vosketap':338,
    'Araksavan':270,
    'Aralez':271,
    'Arevabuyr':127,
    'Arevshat':273,
    'Armash':274,
    'Avshar':275,
    'Aygavan':278,
    'Aygepat':276,
    'Aygestan':277,
    'Aygezard':279,
    'Azatavan':280,
    'Baghramyan':281,
    'Bardzrashen':282,
    'Berdik':283,
    'Berkanush':284,
    'Burastan':285,
    'Byuravan':286,
    'Dalar':287,
    'Darakert':288,
    'Darbnik':289,
    'Dashtakar':290,
    'Deghdzut':292,
    'Dimitrov':293,
    'Ditak':294,
    'Dvin':295,
    'Ginevet':297,
    'Goravan':298,
    'Hnaberd':299,
    'Hovtashen':301,
    'Jrahovit':302,
    'Jrashen':117,
    'Kaghtsrashen':303,
    'Kanachut':304,
    'Lanjar':115,
    'Lanjazat':306,
    'Lusarat':307,
    'Lusashogh':308,
    'Mrganush':311,
    'Mrgavan':312,
    'Mrgavet':313,
    'Narek':314,
    'Nizami':122,
    'No Kyank':315,
    'No Ughi':317,
    'Norabats':318,
    'Norabats':119,
    'Noramarg':319,
    'Norashen':320,
    'Noyakert':321,
    'Nshavan':322,
    'Paruy Sevak':323,
    'Pok Vedi':324,
    'Ranchpar':118,
    'Sayat-Nova':325,
    'Shahumyan':326,
    'Sipanik':327,
    'Sis':328,
    'Sisavan':329,
    'Surenavan':330,
    'Taperakan':331,
    'Urtsadzor':332,
    'Vanashen':333,
    'Vardashat':334,
    'Vardashen':335,
    'Veri Artashat':336,
    'Veri Dvin':337,
    'Vostan':339,
    'Yeraskh':341,
    'Zangakatun':342,
    'Zorak':123},19)
KOTAYK = LocationGroup('Kotayk',{
    'Abovian':41 ,
    'Aghveran':83 ,
    'Akunk':785,
    'Aragyugh':125,
    'Aramus':802,
    'Argel':79 ,
    'Arinj':81 ,
    'Arzakan':791,
    'Arzni':93 ,
    'Balahovit':803,
    'Bjni':90 ,
    'Byureghavan':76 ,
    'Charentsavan':66 ,
    'Dzoraghbyur':89 ,
    'Garni':77 ,
    'Goght':96 ,
    'Hrazdan':42 ,
    'Jrvezh':82 ,
    'Kamaris':808,
    'Kanakeravan':84 ,
    'Kasagh':85 ,
    'Kotayk':786,
    'Mayakovski':107,
    'Mrgashen':113,
    'No Artamet':814,
    'No Geghi':815,
    'No Gyugh':130,
    'No Hachen':75 ,
    'Nurnus':94 ,
    'Proshyan':95 ,
    'Ptghni':91 ,
    'Solak':124,
    'Tsakhkadzor':43 ,
    'Veri Ptghni':818,
    'Yeghvard':67 ,
    'Zovk':132,
    'Zovuni':70 ,
    'Aghavnadzor':789,
    'Alapars':790,
    'Artavaz':811,
    'Buzhakan':794,
    'Fantan':792,
    'Geghadir':131,
    'Geghard':804,
    'Geghashen':805,
    'Getamej':102,
    'Getargel':806,
    'Hankavan':121,
    'Hatis':797,
    'Hatsavan':787,
    'Jraber':114,
    'Jrarat':788,
    'Kaghsi':807,
    'Kaputan':798,
    'Karashamb':120,
    'Karenis':793,
    'Katnaghbyur':139,
    'Lernanist':809,
    'Marmarik':812,
    'Meghradzor':810,
    'Nor Yerznka':816,
    'Pyunik':813,
    'Saralanj':795,
    'Sevaberd':799,
    'Teghenik':817,
    'Voghjaberd':819,
    'Zar':800,
    'Zoravan':796},40)
SHIRAK = LocationGroup('Shirak',{
    'Gyumri':51 ,
    'Akhuryan':511,
    'Artik':50 ,
    'Ashotsk':535,
    'Maralik':78 ,
    'Akhurik':510,
    'Amasia':518,
    'Anipemza':496,
    'Anushavan':527,
    'Arapi':529,
    'Aregnadem':519,
    'Arevik':512,
    'Arevshat':528,
    'Aygabats':513,
    'Azatan':546,
    'Bagravan':497,
    'Bashgyugh':588,
    'Beniamin':548,
    'Byurakn':521,
    'Dzorakap':499,
    'Getap':551,
    'Getk':550,
    'Gharibjanyan':552,
    'Gtashen':522,
    'Gusanagyugh':500,
    'Hatsik':563,
    'Hatsikavan':554,
    'Haykavan':556,
    'Horom':558,
    'Hovuni':564,
    'Jajur':565,
    'Jajuravan':566,
    'Jrapi':503,
    'Jrarat':515,
    'Kamo':516,
    'Kaps':567,
    'Karnut':517,
    'Keti':568,
    'Krasar':539,
    'Krashen':569,
    'Lanjik':505,
    'Lusaghbyur':506,
    'Lusakert':561,
    'Marmashen':570,
    'Mayisyan':562,
    'Meghrashat':525,
    'Met Mantash':577,
    'Met Sepasar':540,
    'Musayelyan':594,
    'Nahapetavan':579,
    'No Kyank':580,
    'Panik':581,
    'Pemzashen':582,
    'Pok Mantash':578,
    'Pok Sepasar':541,
    'Sarakap':507,
    'Saralanj':583,
    'Sarnaghbyur':508,
    'Shirak':574,
    'Shirakavan':509,
    'Sizavet':543,
    'Spandaryan':585,
    'Vahramaberd':575,
    'Voghji':526,
    'Voskehask':599,
    'Yerazgavors':600,
    'Zuygaghbyur':545},49)
LORRI = LocationGroup('Lorri',{
    'Vanadzor':48 ,
    'Alaverdi':45 ,
    'Dsegh':112,
    'Odzun':134,
    'Spitak':46 ,
    'Stepanavan':47 ,
    'Tashir':69 ,
    'Agarak':457,
    'Akhtala':406,
    'Akori':411,
    'Amrakits':441,
    'Arevashogh':428,
    'Arevatsag':471,
    'Arjut':128,
    'Atan':424,
    'Aygehat':472,
    'Aznvadzor':429,
    'Bazum':430,
    'Bovadzor':458,
    'Darpas':431,
    'Debet':432,
    'Dzoraget':433,
    'Dzoragyugh':434,
    'Gargar':442,
    'Geghasar':436,
    'Ghursali':437,
    'Gogaran':438,
    'Gugark':439,
    'Gyulagarak':440,
    'Haghpat':413,
    'Hagvi':473,
    'Hartagyugh':447,
    'Hobardzi':443,
    'Jrashen':448,
    'Karadzor':449,
    'Karinj':426,
    'Kurtan':444,
    'Lejan':460,
    'Lermontovo':452,
    'Lernantsk':453,
    'Lernapat':454,
    'Lernavan':455,
    'Lor Berd':456,
    'Lorut':423,
    'Margahovit':464,
    'Marts':425,
    'Met Ayrum':408,
    'Met Parni':465,
    'Metsavan':466,
    'Mghart':475,
    'Mikhayelovka':468,
    'No Khachakap':469,
    'Pambak':477,
    'Privolnoye':484,
    'Pushkino':445,
    'Saramej':479,
    'Sarchapet':480,
    'Shahumyan':485,
    'Shamlugh':410,
    'Shenavan':486,
    'Shirakamut':487,
    'Shnogh':488,
    'Tsaghkashat':829,
    'Tsater':476,
    'Tumanyan':422,
    'Vahagnadzor':492,
    'Vahagni':493,
    'Vardablur':446,
    'Yeghegnut':494},44)
GEGHARKUNIK = LocationGroup('Gegharkunik',{
    'Chambarak':71 ,
    'Gavar':36 ,
    'Martuni':37 ,
    'Noratus':381,
    'Sevan':38 ,
    'Vardenis':39 ,
    'Akunk':343,
    'Areguni':352,
    'Artanish':384,
    'Artsvanist':344,
    'Astghadzor':345,
    'Berdkunk':346,
    'Chkalovka':347,
    'Ddmashen':348,
    'Drakhtik':385,
    'Dzoragyugh':349,
    'Gandzak':350,
    'Geghamasar':355,
    'Geghamavan':363,
    'Gegharkunik':364,
    'Geghhovit':365,
    'Hayravank':366,
    'Jil':386,
    'Kalavan':825,
    'Karchaghbyur':367,
    'Karmirgyugh':368,
    'Khachaghbyur':369,
    'Lchap':371,
    'Lchashen':372,
    'Lichk':374,
    'Met Masrik':377,
    'Nerki Getashen':378,
    'Norashen':380,
    'Pambak':359,
    'Pok Masrik':360,
    'Sarukhan':382,
    'Shatjrek':361,
    'Shatvan':362,
    'Shoghakat':383,
    'Tsaghkashen':389,
    'Tsaghkunk':390,
    'Tsakkar':391,
    'Tsapatagh':387,
    'Tsovagyugh':392,
    'Tsovak':395,
    'Tsovasar':393,
    'Tsovazard':394,
    'Tsovinar':396,
    'Vaghashen':397,
    'Vanevan':398,
    'Vardenik':400,
    'Varser':401,
    'Veri Getashen':402,
    'Yeranos':403,
    'Zolakar':404,
    'Zovaber':405},35)
SYUNIK = LocationGroup('Syunik',{
    'Goris':53 ,
    'Kapan':54 ,
    'Meghri':55 ,
    'Sisian':56 ,
    'Agarak':614,
    'Agarak':635,
    'Aghitu':645,
    'Akhlatyan':646,
    'Ashotavan':648,
    'Atchanan':615,
    'Bardzravan':602,
    'Brnakot':651,
    'Davi Bek':620,
    'Harzhis':676,
    'Kajaran':74 ,
    'Karahunj':604,
    'Karchevan':638,
    'Khndzoresk':605,
    'Lehvaz':639,
    'Lernadzor':613,
    'Sarnakunk':671,
    'Shaki':660,
    'Shikahogh':624,
    'Shinuhayr':674,
    'Syunik':628,
    'Tatev':679,
    'Tegh':680,
    'Tsghuk':673,
    'Veri Khotanan':632,
    'Verishen':607,
    'Yeghvard':634},52)
ARAGATSOTN = LocationGroup('Aragatsotn',{
    'Agarak':224,
    'Aghdzk':135,
    'Aparan':15 ,
    'Aragats':16 ,
    'Aragatsavan':229,
    'Aragatsotn':230,
    'Aruch':73 ,
    'Ashtarak':17 ,
    'Byurakan':97 ,
    'Karbi':241,
    'Kosh':92 ,
    'Ohanavan':251,
    'Oshakan':98 ,
    'Parpi':253,
    'Talin':18 ,
    'Tsaghkahovit':104,
    'Ujan':72 ,
    'Voskevaz':108,
    'Agarakavan':225,
    'Akunk':226,
    'Antarut':228,
    'Artashavan':231,
    'Arteni':826,
    'Ashnak':232,
    'Avan':233,
    'Bazmaghbyur':234,
    'Dashtadem':235,
    'Davtashen':236,
    'Ghazaravan':238,
    'Irind':239,
    'Kakavadzor':240,
    'Katnaghbyur':243,
    'Lernarot':244,
    'Mastara':126,
    'Melikgyugh':245,
    'Mughni':103,
    'Nerki Bazmaberd':246,
    'Nerki Sasnashen':247,
    'No Amanos':248,
    'No Yedesia':250,
    'Orgov':252,
    'Saghmosavan':136,
    'Sasunik':830,
    'Shamiram':255,
    'Suser':257,
    'Tatul':258,
    'Tegher':259,
    'Ushi':261,
    'Verin Sasnashen':263,
    'Voskehat':264},14)
TAVUSH = LocationGroup('Tavush',{
    'Berd':59 ,
    'Dilijan':58 ,
    'Ijevan':60 ,
    'Noyemberyan':68 ,
    'Achajur':764,
    'Acharkut':765,
    'Aghavnavank':750,
    'Aknaghbyur':766,
    'Archis':728,
    'Aygedzor':133,
    'Aygehovit':767,
    'Ayrum':727,
    'Azatamut':769,
    'Baghanis':756,
    'Bagratashen':729,
    'Berdavan':758,
    'Chinchin':738,
    'Debetavan':730,
    'Deghdzavan':731,
    'Ditavan':771,
    'Gandzakar':772,
    'Getahovit':773,
    'Gosh':751,
    'Haghartsin':752,
    'Haghtanak':732,
    'Hovk':753,
    'Jujevan':760,
    'Kayan':768,
    'Khachardzan':755,
    'Khashtarak':774,
    'Kirants':775,
    'Koghb':776,
    'Lusadzor':778,
    'Lusahovit':779,
    'Movses':741,
    'Nerkin Tsaghkavan':780,
    'Norashen':744,
    'Paravakar':745,
    'Ptghavan':734,
    'Sarigyugh':781,
    'Sevkar':782,
    'Tavush':746,
    'Teghut':754,
    'Varagavan':747,
    'Voskevan':763,
    'Yenokavan':784,
    'Zorakan':777},57)
VAYOTS_DZOR = LocationGroup('Vayots Dzor',{
    'Jermuk':65 ,
    'Vayk':62 ,
    'Yeghegnadzor':63 ,
    'Agarakadzor':693,
    'Aghavnadzor':694,
    'Areni':129,
    'Arpi':695,
    'Artabuynk':708,
    'Artavan':725,
    'Azatek':690,
    'Chiva':696,
    'Getap':703,
    'Gladzor':702,
    'Gndevaz':686,
    'Goghtanik':709,
    'Hermon':710,
    'Malishka':705,
    'Rind':700,
    'Sers':718,
    'Shatin':706,
    'Vernashen':704,
    'Yeghegis':717,
    'Yelpin':701,
    'Zaritap':726,
    'Zedea':692},61)
ARTSAKH = LocationGroup('Artsakh',{
     'Stepanakert':28,
     'Askeran':29,
     'Mardakert':32,
     'Martuni':33},27)
INTERNATIONAL = LocationGroup('International',{
    'Russia':820,
    'Georgia':821,
    'USA':822},116)

MARZER = LocationGroup('Marzer',{
    YEREVAN : 1,
    ARMAVIR : 23,
    ARARAT : 19,
    KOTAYK : 40,
    SHIRAK : 49,
    LORRI : 44,
    GEGHARKUNIK : 35,
    SYUNIK : 52,
    ARAGATSOTN : 14,
    TAVUSH : 57,
    VAYOTS_DZOR : 61,
    ARTSAKH : 27
})

def getLocationName(locid):
    for location_group in MARZER.keys():
        if locid == location_group.ID:
            return location_group.NAME
        if locid in location_group:
            return location_group[locid]

def getLocationParentLocationNames(locid):
    loc_name = getLocationName(locid)
            
    if locid not in MARZER:
        parent_location = [parent_location for parent_location in MARZER.keys() if locid in parent_location][0].ID
        parent_loc_name = getLocationName(parent_location)
    else:
        parent_loc_name = ''

    return loc_name, parent_loc_name
# ARMENIA = YEREVAN + ARMAVIR + ARARAT + KOTAYK + SHIRAK + LORRI + GEGHARKUNIK + SYUNIK + ARAGATSOTN + TAVUSH + VAYOTS_DZOR + ARTSAKH

# ALL = ARMENIA + MARZER