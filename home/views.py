from django.shortcuts import render
from profiles.models import Profile, ProfileImage
from django.db.models import Q, F
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import datetime as DT
from django.contrib.auth.models import User
import datetime



# Create your views here.
@login_required
def index(request):
    
    profiles = {
    'sborell22' : {'citylong':-2.351248,'citylan':51.638025,'location':'Wotton-under-Edge'},
    'nbouldsx' : {'citylong':-1.04281,'citylan':51.85339,'location':'Ludgershall'},
    'schallice2i' : {'citylong':-0.902918,'citylan':51.451652,'location':'Woodley'},
    'kconeley1d' : {'citylong':-0.902918,'citylan':51.451652,'location':'Redditch'},
    'rgutman2q' : {'citylong':-2.12882,'citylan':52.586973,'location':'Wolverhampton'},
    'dcolly1l' : {'citylong':-6.04172,'citylan':54.51006,'location':'Lisburn'},
    'krodder2f' : {'citylong':-1.88394,'citylan':54.73256,'location':'Wolsingham'},
    'lswayne1a' : {'citylong':-2.59168,'citylan':51.45379,'location':'Bristol'},
    'rballingal1x' : {'citylong':0.965274,'citylan':51.857997,'location':'Wivenhoe'},
    'hmacvays' : {'citylong':-5.8316,'citylan':54.46048,'location':'Saintfield'},
    'rwinney1r' : {'citylong':0.709554,'citylan':50.924972,'location':'Winchelsea'},
    'aratcliffm' : {'citylong':-6.25419,'citylan':54.10116,'location':'Warrenpoint'},
    'afairchild1n' : {'citylong':-1.983,'citylan':50.800465,'location':'Wimborne Minster'},
    'pburbagei' : {'citylong':-3.7527,'citylan':56.10769,'location':'Clackmannan'},
    'jledgerton1z' : {'citylong':-2.40123,'citylan':51.593722,'location':'Wickwar'},
    'mdickonsu' : {'citylong':-2.34873,'citylan':54.47327,'location':'Kirkby Stephen'},
    'mround7' : {'citylong':-0.739779,'citylan':51.761877,'location':'Wendover'},
    'dnisius2r' : {'citylong':-2.02208,'citylan':52.552888,'location':'Wednesbury'},
    'nkinnach1m' : {'citylong':-0.342274,'citylan':51.588142,'location':'Harrow'},
    'itouhigh' : {'citylong':-1.865449,'citylan':50.878978,'location':'Verwood'},
    'dpleass1' : {'citylong':-3.506101,'citylan':51.659719,'location':'Treorchy'},
    'bhebditch8' : {'citylong':-4.194344,'citylan':50.37529,'location':'Torpoint'},
    'tbicke' : {'citylong':-3.491207,'citylan':50.902049,'location':'Tiverton'},
    'acollcott21' : {'citylong':-2.525153,'citylan':51.608306,'location':'Thornbury'},
    'ashapcotew' : {'citylong':-3.02666,'citylan':53.184872,'location':'Hawarden'},
    'kmcgorley9' : {'citylong':-1.328982,'citylan':54.570455,'location':'Stockton-on-Tees'},
    'apeetermann1o' : {'citylong':-1.023942,'citylan':53.69109,'location':'Snaith'},
    'wstorckj' : {'citylong':-3.22333,'citylan':53.2747,'location':'Holywell'},
    'jbeddard1q' : {'citylong':0.101108,'citylan':50.773467,'location':'Seaford'},
    'cdominkal' : {'citylong':-3.59423,'citylan':55.978371,'location':'Linlithgow'},
    'rconsidine1w' : {'citylong':0.505078,'citylan':51.56491,'location':'Pitsea'},
    'bhurleyr' : {'citylong':-3.15219,'citylan':55.880638,'location':'Loanhead'},
    'kcossum20' : {'citylong':-2.576585,'citylan':51.531653,'location':'Patchway'},
    'dbartodv' : {'citylong':-3.05374,'citylan':55.94215,'location':'Musselburgh'},
    'cdobbie28' : {'citylong':-2.428085,'citylan':53.418359,'location':'Partington'},
    'cstratiff13' : {'citylong':-3.23048,'citylan':56.06002,'location':'Burntisland'},
    'ckenyam2g' : {'citylong':-4.939017,'citylan':50.542062,'location':'Padstow'},
    'smcowen1b' : {'citylong':-3.18395,'citylan':56.21168,'location':'Collydean'},
    'ebabar2a' : {'citylong':0.242756,'citylan':51.709531,'location':'Ongar'},
    'nridolfi15' : {'citylong':-3.34329,'citylan':56.110222,'location':'Cowdenbeath'},
    'xgazzard2m' : {'citylong':-5.69317,'citylan':54.591379,'location':'Newtownards'},
    'teakeley1h' : {'citylong':-1.35614,'citylan':53.72591,'location':'Castleford'},
    'aebrall2d' : {'citylong':-3.750323,'citylan':50.671082,'location':'Moretonhampstead'},
    'brobben18' : {'citylong':-1.71354,'citylan':53.723049,'location':'Cleckheaton'},
    'srime1y' : {'citylong':-2.489453,'citylan':51.862693,'location':'Mitcheldean'},
    'mlatcht' : {'citylong':-1.89452,'citylan':53.80236,'location':'Denholme'},
    'kmiddlewickg' : {'citylong':-2.936639,'citylan':50.725156,'location':'Lyme Regis'},
    'dmactrustie25' : {'citylong':-2.530504,'citylan':51.72913,'location':'Lydney'},
    'cswainson10' : {'citylong':-1.63284,'citylan':53.691551,'location':'Dewsbury'},
    'aheater2n' : {'citylong':-6.933676,'citylan':55.045456,'location':'Limavady'},
    'bfleckness1i' : {'citylong':-2.03484,'citylan':52.568981,'location':'Darlaston'},
    'akarczinski1p' : {'citylong':0.00878,'citylan':50.873872,'location':'Lewes'},
    'bchadburnk' : {'citylong':-2.08734,'citylan':52.508671,'location':'Dudley'},
    'qbentame5' : {'citylong':-1.549077,'citylan':53.800755,'location':'Leeds'},
    'cbleesingc' : {'citylong':-1.338362,'citylan':53.01827,'location':'Langley Mill'},
    'tgrishakov2o' : {'citylong':-2.279823,'citylan':56.84495,'location':'Inverbervie'},
    'qgianiello1j' : {'citylong':-1.74484,'citylan':52.48758,'location':'Fordbridge'},
    'jhazelton2p' : {'citylong':-1.786292,'citylan':53.571744,'location':'Holmfirth'},
    'scosgrove1k' : {'citylong':-0.46804,'citylan':52.135712,'location':'Bedford'},
    'cbarrick1v' : {'citylong':1.260297,'citylan':51.934731,'location':'Harwich'},
    'nlittrellq' : {'citylong':-1.56756,'citylan':54.94226,'location':'Windy Nook'},
    'rspinney1u' : {'citylong':0.35792,'citylan':51.873148,'location':'Great Dunmow'},
    'cedmonstonp' : {'citylong':-1.86827,'citylan':52.217049,'location':'Alcester'},
    'ggodley2c' : {'citylong':-0.876381,'citylan':53.702941,'location':'Goole'},
    'cmonget17' : {'citylong':-0.10193,'citylan':51.24061,'location':'Beltchingley'},
    'sbellson4' : {'citylong':-2.238156,'citylan':51.864245,'location':'Gloucester'},
    'zortiger6' : {'citylong':-2.718454,'citylan':51.147427,'location':'Glastonbury'},
    'yhallibonef' : {'citylong':-1.899776,'citylan':50.807364,'location':'Ferndown'},
    'oainge23' : {'citylong':-2.40396,'citylan':53.545838,'location':'Farnworth'},
    'nmushety' : {'citylong':-0.7444,'citylan':51.340248,'location':'Camberley'},
    'mbalfour2h' : {'citylong':-2.897404,'citylan':53.279812,'location':'Ellesmere Port'},
    'cskullet1c' : {'citylong':-0.50776,'citylan':51.388168,'location':'Chertsey'},
    'cspoward2j' : {'citylong':-6.26031,'citylan':53.349805,'location':'Dublin'},
    'belcoate1e' : {'citylong':1.44002,'citylan':52.454632,'location':'Bungay'},
    'wpickburn1t' : {'citylong':1.234845,'citylan':51.927088,'location':'Dovercourt'},
    'wgowdridgeo' : {'citylong':0.710493,'citylan':52.242924,'location':'Bury St Edmunds'},
    'mragdale29' : {'citylong':-1.968243,'citylan':51.718495,'location':'Cirencester'},
    'cdonovin14' : {'citylong':1.69417,'citylan':52.45145,'location':'Carlton Colville'},
    'igallego26' : {'citylong':-2.214115,'citylan':53.394361,'location':'Cheadle'},
    'broulston11' : {'citylong':-0.52313,'citylan':51.887619,'location':'Dunstable'},
    'ehulcoop2e' : {'citylong':-1.912923,'citylan':53.323988,'location':'Chapel-en-le-Frith'},
    'smatyugin19' : {'citylong':-3.47952,'citylan':51.64522,'location':'Rhondda'},
    'admin1' : {'citylong':-3.17909,'citylan':51.481581,'location':'Cardiff'},
    'bpentelo2l' : {'citylong':0.121817,'citylan':52.205337,'location':'Cambridge'},
    'mquigley1g' : {'citylong':-0.52028,'citylan':51.90461,'location':'Houghton Regis'},
    'kbeaford2b' : {'citylong':0.814539,'citylan':51.628347,'location':'Burnham-on-Crouch'},
    'tinglese16' : {'citylong':-3.943646,'citylan':51.621441,'location':'Swansea'},
    'olamped' : {'citylong':-3.779342,'citylan':50.481799,'location':'Buckfastleigh'},
    'jsich1s' : {'citylong':1.021399,'citylan':51.816142,'location':'Brightlingsea'},
    'ecrocetton' : {'citylong':-0.24846,'citylan':52.573391,'location':'Peterborough'},
    'hpardue24' : {'citylong':-2.57864,'citylan':53.58736,'location':'Blackrod'},
    'mshelmerdinez' : {'citylong':-5.35325,'citylan':36.14491,'location':'Ramsey'},
    'kcompfort3' : {'citylong':-1.890401,'citylan':52.486243,'location':'Birmingham'},
    'kbebbell2k' : {'citylong':-0.26422,'citylan':52.086938,'location':'Biggleswade'},
    'batheis1f' : {'citylong':0.33713,'citylan':52.334099,'location':'Soham'},
    'tshewery0' : {'citylong':-0.529209,'citylan':52.062739,'location':'Bedfordshire'},
    'santrack2' : {'citylong':-0.644241,'citylan':51.602396,'location':'Beaconsfield'},
    'sgorcke27' : {'citylong':-1.092396,'citylan':51.26654,'location':'Basingstoke'},
    'dlaba12' : {'citylong':-0.265103,'citylan':52.230083,'location':'St Neots'},
    'ttownsenda' : {'citylong':-3.218894,'citylan':54.108967,'location':'Barrow-in-Furness'},
    'ecarabineb' : {'citylong':-1.676171,'citylan':53.215207,'location':'Bakewell'},
    }
    
    for k, v in profiles.items():
        user = User.objects.get(username=k)
        user.citylong = v['citylong']
        user.citylat = v['citylan']
        user.location = v['location']
        print(user.citylat)
        user.save()

    # Change limit
    # 'or' needed in gender check https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
    # Exclude current user
    # Nearby Profiles
    if request.user.profile.looking_for == "BOTH":
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
    else:
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
    # Profiles for quick match finder
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
    # Filter date_joined
    # Profiles for active most recently  
    if request.user.profile.looking_for == "BOTH":
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
    # Profiles for newest
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
    
def preregister(request):
        
    return render(request, 'index.html')