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
        'card_profiles_exists' : card_profiles_exists,
        'closest_profiles':closest_profiles,
        'active_profiles':active_profiles,
        'newest_profiles': newest_profiles,
        'card_profiles': card_profiles
    }
    
    return render(request, 'index.html', context)
    
def preregister(request):
    
    profiles = {
        'dnisius2r' : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        'rgutman2q' : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        'jhazelton2p' : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        'tgrishakov2o' : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        'aheater2n' : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        'xgazzard2m' : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        'bpentelo2l' : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        'kbebbell2k' : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        'cspoward2j' : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        'schallice2i' : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        'mbalfour2h' : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        'ckenyam2g' : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        'krodder2f' : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        'ehulcoop2e' : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        'aebrall2d' : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        'ggodley2c' : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        'kbeaford2b' : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        'ebabar2a' : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        'mragdale29' : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        'cdobbie28' : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        'sgorcke27' : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        'igallego26' : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        'dmactrustie25' : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        'hpardue24' : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        'oainge23' : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        'sborell22' : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        'acollcott21' : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        'kcossum20' : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        'jledgerton1z' : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        'srime1y' : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        'rballingal1x' : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        'rconsidine1w' : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        'cbarrick1v' : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        'rspinney1u' : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        'wpickburn1t' : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        'jsich1s' : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        'rwinney1r' : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        'jbeddard1q' : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        'akarczinski1p' : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        'apeetermann1o' : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        'afairchild1n' : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        'nkinnach1m' : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        'dcolly1l' : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        'scosgrove1k' : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        'qgianiello1j' : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        'bfleckness1i' : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        'teakeley1h' : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        'mquigley1g' : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        'batheis1f' : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        'belcoate1e' : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        'kconeley1d' : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        'cskullet1c' : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        'smcowen1b' : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        'lswayne1a' : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        'smatyugin19' : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        'brobben18' : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        'cmonget17' : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        'tinglese16' : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        'nridolfi15' : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        'cdonovin14' : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        'cstratiff13' : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        'dlaba12' : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        'broulston11' : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        'cswainson10' : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        'mshelmerdinez' : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        'nmushety' : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        'nbouldsx' : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        'ashapcotew' : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        'dbartodv' : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        'mdickonsu' : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        'mlatcht' : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        'hmacvays' : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        'bhurleyr' : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        'nlittrellq' : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        'cedmonstonp' : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        'wgowdridgeo' : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        'ecrocetton' : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        'aratcliffm' : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        'cdominkal' : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        'bchadburnk' : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        'wstorckj' : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        'pburbagei' : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        'itouhigh' : {'citylong':-1.865449,'citylang':50.878978,'location':'Verwood'},
        'kmiddlewickg' : {'citylong':-2.936639,'citylang':50.725156,'location':'Lyme Regis'},
        'yhallibonef' : {'citylong':-1.899776,'citylang':50.807364,'location':'Ferndown'},
        'tbicke' : {'citylong':-3.491207,'citylang':50.902049,'location':'Tiverton'},
        'olamped' : {'citylong':-3.779342,'citylang':50.481799,'location':'Buckfastleigh'},
        'cbleesingc' : {'citylong':-1.338362,'citylang':53.01827,'location':'Langley Mill'},
        'ecarabineb' : {'citylong':-1.676171,'citylang':53.215207,'location':'Bakewell'},
        'ttownsenda' : {'citylong':-3.218894,'citylang':54.108967,'location':'Barrow-in-Furness'},
        'kmcgorley9' : {'citylong':-1.328982,'citylang':54.570455,'location':'Stockton-on-Tees'},
        'bhebditch8' : {'citylong':-4.194344,'citylang':50.37529,'location':'Torpoint'},
        'mround7' : {'citylong':-0.739779,'citylang':51.761877,'location':'Wendover'},
        'zortiger6' : {'citylong':-2.718454,'citylang':51.147427,'location':'Glastonbury'},
        'qbentame5' : {'citylong':-1.549077,'citylang':53.800755,'location':'Leeds'},
        'sbellson4' : {'citylong':-2.238156,'citylang':51.864245,'location':'Gloucester'},
        'kcompfort3' : {'citylong':-1.890401,'citylang':52.486243,'location':'Birmingham'},
        'santrack2' : {'citylong':-0.644241,'citylang':51.602396,'location':'Beaconsfield'},
        'dpleass1' : {'citylong':-3.506101,'citylang':51.659719,'location':'Treorchy'},
        'tshewery0' : {'citylong':-0.529209,'citylang':52.062739,'location':'Bedfordshire'},
        'admin1' : {'citylong':-3.17909,'citylang':51.481581,'location':'Cardiff'},
    }
    
    for k, v in profiles.items():
        user = Profile.objects.get(user__username=k)
        user.citylong = v['citylong']
        user.citylang = v['citylang']
        user.location = v['location']
        user.save()
        
    return render(request, 'preregister.html')