from django.shortcuts import render
from profiles.models import Profile, ProfileImage
from django.db.models import Q, F
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import datetime as DT
from django.contrib.auth.models import User
from chat.models import Conversations
import datetime
import stripe
from checkout.models import Subscription

# Home page after user logs in
@login_required
def index(request):

    
    # Query profiles in distance order for 'Closest to you' section
    if request.user.profile.looking_for == "BOTH":
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
    else:
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
    # Profiles for quick match finder, exclude users winked or rejected previously
    if request.user.profile.looking_for == "BOTH":
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
    else:
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
    
    if card_profiles.count() == 0:
        card_profiles_exists = False
    else: 
        card_profiles_exists = True
    
    
    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)
    # Profiles for active most recently, excluding those who signed up in the last 7 days
    if request.user.profile.looking_for == "BOTH":
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
    # Profiles ordered by signed up date for 'Newcomers' section
    if request.user.profile.looking_for == "BOTH":
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
    else:
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

    context = {
        'page_ref': 'home',
        'card_profiles_exists' : card_profiles_exists,
        'closest_profiles':closest_profiles,
        'active_profiles':active_profiles,
        'newest_profiles': newest_profiles,
        'card_profiles': card_profiles
    }
    
    return render(request, 'home.html', context)
    
# Home page before logged in/registered
def preregister(request):
    profiles = {
        'dberzons0' : {'citylong':-2.351248,'citylan':51.638025,'location':'Wotton-under-Edge'},
        'bcorringham1' : {'citylong':-1.04281,'citylan':51.85339,'location':'Ludgershall'},
        'mbumphrey2' : {'citylong':-0.902918,'citylan':51.451652,'location':'Woodley'},
        'kalcoran3' : {'citylong':-0.902918,'citylan':51.451652,'location':'Redditch'},
        'chedderly4' : {'citylong':-2.12882,'citylan':52.586973,'location':'Wolverhampton'},
        'ogetley5' : {'citylong':-6.04172,'citylan':54.51006,'location':'Lisburn'},
        'aroback6' : {'citylong':-1.88394,'citylan':54.73256,'location':'Wolsingham'},
        'kbatkin7' : {'citylong':-2.59168,'citylan':51.45379,'location':'Bristol'},
        'ghabishaw8' : {'citylong':0.965274,'citylan':51.857997,'location':'Wivenhoe'},
        'zdutnall9' : {'citylong':-5.8316,'citylan':54.46048,'location':'Saintfield'},
        'kfaersa' : {'citylong':0.709554,'citylan':50.924972,'location':'Winchelsea'},
        'abadcockb' : {'citylong':-6.25419,'citylan':54.10116,'location':'Warrenpoint'},
        'mkellerc' : {'citylong':-1.983,'citylan':50.800465,'location':'Wimborne Minster'},
        'lgetchd' : {'citylong':-3.7527,'citylan':56.10769,'location':'Clackmannan'},
        'pfawdriee' : {'citylong':-2.40123,'citylan':51.593722,'location':'Wickwar'},
        'gstivensf' : {'citylong':-2.34873,'citylan':54.47327,'location':'Kirkby Stephen'},
        'pabramchikg' : {'citylong':-0.739779,'citylan':51.761877,'location':'Wendover'},
        'jnielsonh' : {'citylong':-2.02208,'citylan':52.552888,'location':'Wednesbury'},
        'asurridgei' : {'citylong':-0.342274,'citylan':51.588142,'location':'Harrow'},
        'drigglesfordj' : {'citylong':-1.865449,'citylan':50.878978,'location':'Verwood'},
        'ldelavaletteparisotk' : {'citylong':-3.506101,'citylan':51.659719,'location':'Treorchy'},
        'bmacallasterl' : {'citylong':-4.194344,'citylan':50.37529,'location':'Torpoint'},
        'xgierckem' : {'citylong':-3.491207,'citylan':50.902049,'location':'Tiverton'},
        'bmyrtlen' : {'citylong':-2.525153,'citylan':51.608306,'location':'Thornbury'},
        'tgairdnero' : {'citylong':-3.02666,'citylan':53.184872,'location':'Hawarden'},
        'shaydockp' : {'citylong':-1.328982,'citylan':54.570455,'location':'Stockton-on-Tees'},
        'rreinq' : {'citylong':-1.023942,'citylan':53.69109,'location':'Snaith'},
        'qoneilr' : {'citylong':-3.22333,'citylan':53.2747,'location':'Holywell'},
        'koverys' : {'citylong':0.101108,'citylan':50.773467,'location':'Seaford'},
        'kcastanost' : {'citylong':-3.59423,'citylan':55.978371,'location':'Linlithgow'},
        'tbradlaughu' : {'citylong':0.505078,'citylan':51.56491,'location':'Pitsea'},
        'gbalmv' : {'citylong':-3.15219,'citylan':55.880638,'location':'Loanhead'},
        'hmcurew' : {'citylong':-2.576585,'citylan':51.531653,'location':'Patchway'},
        'mburnardx' : {'citylong':-3.05374,'citylan':55.94215,'location':'Musselburgh'},
        'arichmonty' : {'citylong':-2.428085,'citylan':53.418359,'location':'Partington'},
        'ssmithez' : {'citylong':-3.23048,'citylan':56.06002,'location':'Burntisland'},
        'fupward10' : {'citylong':-4.939017,'citylan':50.542062,'location':'Padstow'},
        'jbushe11' : {'citylong':-3.18395,'citylan':56.21168,'location':'Collydean'},
        'emanoelli12' : {'citylong':0.242756,'citylan':51.709531,'location':'Ongar'},
        'ikrier13' : {'citylong':-3.34329,'citylan':56.110222,'location':'Cowdenbeath'},
        'speyntue14' : {'citylong':-5.69317,'citylan':54.591379,'location':'Newtownards'},
        'tcommuzzo15' : {'citylong':-1.35614,'citylan':53.72591,'location':'Castleford'},
        'jpitkeathley16' : {'citylong':-3.750323,'citylan':50.671082,'location':'Moretonhampstead'},
        'scomberbeach17' : {'citylong':-1.71354,'citylan':53.723049,'location':'Cleckheaton'},
        'mlough18' : {'citylong':-2.489453,'citylan':51.862693,'location':'Mitcheldean'},
        'mrallinshaw19' : {'citylong':-1.89452,'citylan':53.80236,'location':'Denholme'},
        'lcribbott1a' : {'citylong':-2.936639,'citylan':50.725156,'location':'Lyme Regis'},
        'megell1b' : {'citylong':-2.530504,'citylan':51.72913,'location':'Lydney'},
        'lprendeguest1c' : {'citylong':-1.63284,'citylan':53.691551,'location':'Dewsbury'},
        'djumonet1d' : {'citylong':-6.933676,'citylan':55.045456,'location':'Limavady'},
        'aroussell1e' : {'citylong':-2.03484,'citylan':52.568981,'location':'Darlaston'},
        'hcicullo1f' : {'citylong':0.00878,'citylan':50.873872,'location':'Lewes'},
        'dravilious1g' : {'citylong':-2.08734,'citylan':52.508671,'location':'Dudley'},
        'njovis1h' : {'citylong':-1.549077,'citylan':53.800755,'location':'Leeds'},
        'kbunning1i' : {'citylong':-1.338362,'citylan':53.01827,'location':'Langley Mill'},
        'jbilbie1j' : {'citylong':-2.279823,'citylan':56.84495,'location':'Inverbervie'},
        'jmilan1k' : {'citylong':-1.74484,'citylan':52.48758,'location':'Fordbridge'},
        'eguyonnet1l' : {'citylong':-1.786292,'citylan':53.571744,'location':'Holmfirth'},
        'dfranck1m' : {'citylong':-0.46804,'citylan':52.135712,'location':'Bedford'},
        'nquincee1n' : {'citylong':1.260297,'citylan':51.934731,'location':'Harwich'},
        'mcantillion1o' : {'citylong':-1.56756,'citylan':54.94226,'location':'Windy Nook'},
        'atoplin1p' : {'citylong':0.35792,'citylan':51.873148,'location':'Great Dunmow'},
        'mpickaver1q' : {'citylong':-1.86827,'citylan':52.217049,'location':'Alcester'},
        'mlegerton1r' : {'citylong':-0.876381,'citylan':53.702941,'location':'Goole'},
        'czupo1s' : {'citylong':-0.10193,'citylan':51.24061,'location':'Beltchingley'},
        'hcarding1t' : {'citylong':-2.238156,'citylan':51.864245,'location':'Gloucester'},
        'lwims1u' : {'citylong':-2.718454,'citylan':51.147427,'location':'Glastonbury'},
        'dduran1v' : {'citylong':-1.899776,'citylan':50.807364,'location':'Ferndown'},
        'cryburn1w' : {'citylong':-2.40396,'citylan':53.545838,'location':'Farnworth'},
        'lodowgaine1x' : {'citylong':-0.7444,'citylan':51.340248,'location':'Camberley'},
        'bandres1y' : {'citylong':-2.897404,'citylan':53.279812,'location':'Ellesmere Port'},
        'adoe1z' : {'citylong':-0.50776,'citylan':51.388168,'location':'Chertsey'},
        'lkenchington20' : {'citylong':-6.26031,'citylan':53.349805,'location':'Dublin'},
        'sferrara21' : {'citylong':1.44002,'citylan':52.454632,'location':'Bungay'},
        'tholtham22' : {'citylong':1.234845,'citylan':51.927088,'location':'Dovercourt'},
        'sewington23' : {'citylong':0.710493,'citylan':52.242924,'location':'Bury St Edmunds'},
        'bhiseman24' : {'citylong':-1.968243,'citylan':51.718495,'location':'Cirencester'},
        'bolphert25' : {'citylong':1.69417,'citylan':52.45145,'location':'Carlton Colville'},
        'mranby26' : {'citylong':-2.214115,'citylan':53.394361,'location':'Cheadle'},
        'nspalding27' : {'citylong':-0.52313,'citylan':51.887619,'location':'Dunstable'},
        'tthoresby28' : {'citylong':-1.912923,'citylan':53.323988,'location':'Chapel-en-le-Frith'},
        'ltourle29' : {'citylong':-3.47952,'citylan':51.64522,'location':'Rhondda'},
        'oloyndon2a' : {'citylong':-3.17909,'citylan':51.481581,'location':'Cardiff'},
        'jswaton2b' : {'citylong':0.121817,'citylan':52.205337,'location':'Cambridge'},
        'mnunson2c' : {'citylong':-0.52028,'citylan':51.90461,'location':'Houghton Regis'},
        'awrightim2d' : {'citylong':0.814539,'citylan':51.628347,'location':'Burnham-on-Crouch'},
        'dmisk2e' : {'citylong':-3.943646,'citylan':51.621441,'location':'Swansea'},
        'msaye2f' : {'citylong':-3.779342,'citylan':50.481799,'location':'Buckfastleigh'},
        'rlaxston2g' : {'citylong':1.021399,'citylan':51.816142,'location':'Brightlingsea'},
        'mhuff2h' : {'citylong':-0.24846,'citylan':52.573391,'location':'Peterborough'},
        'mwhitechurch2i' : {'citylong':-2.57864,'citylan':53.58736,'location':'Blackrod'},
        'mmaffi2j' : {'citylong':-5.35325,'citylan':36.14491,'location':'Ramsey'},
        'gbugg2k' : {'citylong':-1.890401,'citylan':52.486243,'location':'Birmingham'},
        'nmajor2l' : {'citylong':-0.26422,'citylan':52.086938,'location':'Biggleswade'},
        'celsay2m' : {'citylong':0.33713,'citylan':52.334099,'location':'Soham'},
        'dbree2n' : {'citylong':-0.529209,'citylan':52.062739,'location':'Bedfordshire'},
        'dlangan2o' : {'citylong':-0.644241,'citylan':51.602396,'location':'Beaconsfield'},
        'kyare2p' : {'citylong':-1.092396,'citylan':51.26654,'location':'Basingstoke'},
        'dbambrough2q' : {'citylong':-0.265103,'citylan':52.230083,'location':'St Neots'},
        'ngrave2r' : {'citylong':-3.218894,'citylan':54.108967,'location':'Barrow-in-Furness'},
    }
    
    for k, v in profiles.items():
        profile = Profile.objects.get(user__username=k)
        profile.citylong = v['citylong']
        profile.citylat = v['citylan']
        profile.location = v['location']

        profile.save()
        
    return render(request, 'index.html')