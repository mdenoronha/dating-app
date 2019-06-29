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
        1 : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        2 : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        3 : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        4 : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        5 : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        6 : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        7 : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        8 : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        9 : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        10 : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        11 : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        12 : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        13 : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        14 : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        15 : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        16 : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        17 : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        18 : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        19 : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        20 : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        21 : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        22 : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        23 : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        24 : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        25 : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        26 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        27 : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        28 : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        29 : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        30 : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        31 : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        32 : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        33 : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        34 : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        35 : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        36 : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        37 : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        38 : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        39 : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        40 : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        41 : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        42 : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        43 : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        44 : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        45 : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        46 : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        47 : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        48 : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        49 : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        50 : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        51 : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        52 : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        53 : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        54 : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        55 : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        56 : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        57 : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        58 : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        59 : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        60 : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        61 : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        62 : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        63 : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        64 : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        65 : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        66 : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        67 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        68 : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        69 : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        70 : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        71 : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        72 : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        73 : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        74 : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        75 : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        76 : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        77 : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        78 : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        79 : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        80 : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        81 : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        82 : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        83 : {'citylong':-1.865449,'citylang':50.878978,'location':'Verwood'},
        84 : {'citylong':-2.936639,'citylang':50.725156,'location':'Lyme Regis'},
        85 : {'citylong':-1.899776,'citylang':50.807364,'location':'Ferndown'},
        86 : {'citylong':-3.491207,'citylang':50.902049,'location':'Tiverton'},
        87 : {'citylong':-3.779342,'citylang':50.481799,'location':'Buckfastleigh'},
        88 : {'citylong':-1.338362,'citylang':53.01827,'location':'Langley Mill'},
        89 : {'citylong':-1.676171,'citylang':53.215207,'location':'Bakewell'},
        90 : {'citylong':-3.218894,'citylang':54.108967,'location':'Barrow-in-Furness'},
        91 : {'citylong':-1.328982,'citylang':54.570455,'location':'Stockton-on-Tees'},
        92 : {'citylong':-4.194344,'citylang':50.37529,'location':'Torpoint'},
        93 : {'citylong':-0.739779,'citylang':51.761877,'location':'Wendover'},
        94 : {'citylong':-2.718454,'citylang':51.147427,'location':'Glastonbury'},
        95 : {'citylong':-1.549077,'citylang':53.800755,'location':'Leeds'},
        96 : {'citylong':-2.238156,'citylang':51.864245,'location':'Gloucester'},
        97 : {'citylong':-1.890401,'citylang':52.486243,'location':'Birmingham'},
        98 : {'citylong':-0.644241,'citylang':51.602396,'location':'Beaconsfield'},
        99 : {'citylong':-3.506101,'citylang':51.659719,'location':'Treorchy'},
        100 : {'citylong':-0.529209,'citylang':52.062739,'location':'Bedfordshire'},
        101 : {'citylong':-3.17909,'citylang':51.481581,'location':'Cardiff'},
        102 : {'citylong':0.485678,'citylang':51.574245,'location':'Essex'},
        103 : {'citylong':-2.796721,'citylang':56.339775,'location':'St Andrews'},
        104 : {'citylong':-82.331395,'citylang':28.835451,'location':'Inverness'},
        105 : {'citylong':-3.188267,'citylang':55.953252,'location':'Edinburgh'},
        106 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
    }
    
    for k, v in profiles.items():
        user = Profile.objects.get(pk=k)
        user.citylong = v['citylong']
        user.citylang = v['citylang']
        user.location = v['location']
        user.save()
        
    return render(request, 'preregister.html')