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
        12 : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        18 : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        19 : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        20 : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        21 : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        22 : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        23 : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        24 : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        25 : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        26 : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        27 : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        28 : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        29 : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        30 : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        31 : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        32 : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        33 : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        34 : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        35 : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        36 : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        37 : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        38 : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        39 : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        40 : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        41 : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        42 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        43 : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        44 : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        45 : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        46 : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        47 : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        48 : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        49 : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        50 : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        51 : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        52 : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        53 : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        54 : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        55 : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        56 : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        57 : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        58 : {'citylong':-2.02208,'citylang':52.552888,'location':'Wednesbury'},
        59 : {'citylong':-2.12882,'citylang':52.586973,'location':'Wolverhampton'},
        60 : {'citylong':-1.786292,'citylang':53.571744,'location':'Holmfirth'},
        61 : {'citylong':-2.279823,'citylang':56.84495,'location':'Inverbervie'},
        62 : {'citylong':-6.933676,'citylang':55.045456,'location':'Limavady'},
        63 : {'citylong':-5.69317,'citylang':54.591379,'location':'Newtownards'},
        64 : {'citylong':0.121817,'citylang':52.205337,'location':'Cambridge'},
        65 : {'citylong':-0.26422,'citylang':52.086938,'location':'Biggleswade'},
        66 : {'citylong':-6.26031,'citylang':53.349805,'location':'Dublin'},
        67 : {'citylong':-0.902918,'citylang':51.451652,'location':'Woodley'},
        68 : {'citylong':-2.897404,'citylang':53.279812,'location':'Ellesmere Port'},
        69 : {'citylong':-4.939017,'citylang':50.542062,'location':'Padstow'},
        70 : {'citylong':-1.88394,'citylang':54.73256,'location':'Wolsingham'},
        71 : {'citylong':-1.912923,'citylang':53.323988,'location':'Chapel-en-le-Frith'},
        72 : {'citylong':-3.750323,'citylang':50.671082,'location':'Moretonhampstead'},
        73 : {'citylong':-0.876381,'citylang':53.702941,'location':'Goole'},
        74 : {'citylong':0.814539,'citylang':51.628347,'location':'Burnham-on-Crouch'},
        75 : {'citylong':0.242756,'citylang':51.709531,'location':'Ongar'},
        76 : {'citylong':-1.968243,'citylang':51.718495,'location':'Cirencester'},
        77 : {'citylong':-2.428085,'citylang':53.418359,'location':'Partington'},
        78 : {'citylong':-1.092396,'citylang':51.26654,'location':'Basingstoke'},
        79 : {'citylong':-2.214115,'citylang':53.394361,'location':'Cheadle'},
        80 : {'citylong':-2.530504,'citylang':51.72913,'location':'Lydney'},
        81 : {'citylong':-2.57864,'citylang':53.58736,'location':'Blackrod'},
        82 : {'citylong':-2.40396,'citylang':53.545838,'location':'Farnworth'},
        83 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
        84 : {'citylong':-2.525153,'citylang':51.608306,'location':'Thornbury'},
        85 : {'citylong':-2.576585,'citylang':51.531653,'location':'Patchway'},
        86 : {'citylong':-2.40123,'citylang':51.593722,'location':'Wickwar'},
        87 : {'citylong':-2.489453,'citylang':51.862693,'location':'Mitcheldean'},
        88 : {'citylong':0.965274,'citylang':51.857997,'location':'Wivenhoe'},
        89 : {'citylong':0.505078,'citylang':51.56491,'location':'Pitsea'},
        90 : {'citylong':1.260297,'citylang':51.934731,'location':'Harwich'},
        91 : {'citylong':0.35792,'citylang':51.873148,'location':'Great Dunmow'},
        92 : {'citylong':1.234845,'citylang':51.927088,'location':'Dovercourt'},
        93 : {'citylong':1.021399,'citylang':51.816142,'location':'Brightlingsea'},
        94 : {'citylong':0.709554,'citylang':50.924972,'location':'Winchelsea'},
        95 : {'citylong':0.101108,'citylang':50.773467,'location':'Seaford'},
        96 : {'citylong':0.00878,'citylang':50.873872,'location':'Lewes'},
        97 : {'citylong':-1.023942,'citylang':53.69109,'location':'Snaith'},
        98 : {'citylong':-1.983,'citylang':50.800465,'location':'Wimborne Minster'},
        99 : {'citylong':-1.865449,'citylang':50.878978,'location':'Verwood'},
        100 : {'citylong':-2.936639,'citylang':50.725156,'location':'Lyme Regis'},
        101 : {'citylong':-1.899776,'citylang':50.807364,'location':'Ferndown'},
        102 : {'citylong':-3.491207,'citylang':50.902049,'location':'Tiverton'},
        103 : {'citylong':-3.779342,'citylang':50.481799,'location':'Buckfastleigh'},
        104 : {'citylong':-1.338362,'citylang':53.01827,'location':'Langley Mill'},
        105 : {'citylong':-1.676171,'citylang':53.215207,'location':'Bakewell'},
        106 : {'citylong':-3.218894,'citylang':54.108967,'location':'Barrow-in-Furness'},
        107 : {'citylong':-1.328982,'citylang':54.570455,'location':'Stockton-on-Tees'},
        108 : {'citylong':-4.194344,'citylang':50.37529,'location':'Torpoint'},
        109 : {'citylong':-0.739779,'citylang':51.761877,'location':'Wendover'},
        110 : {'citylong':-2.718454,'citylang':51.147427,'location':'Glastonbury'},
        111 : {'citylong':-1.549077,'citylang':53.800755,'location':'Leeds'},
        112 : {'citylong':-2.238156,'citylang':51.864245,'location':'Gloucester'},
        113 : {'citylong':-1.890401,'citylang':52.486243,'location':'Birmingham'},
        114 : {'citylong':-0.644241,'citylang':51.602396,'location':'Beaconsfield'},
        115 : {'citylong':-3.506101,'citylang':51.659719,'location':'Treorchy'},
        116 : {'citylong':-0.529209,'citylang':52.062739,'location':'Bedfordshire'},
        117 : {'citylong':-3.17909,'citylang':51.481581,'location':'Cardiff'},
        118 : {'citylong':0.485678,'citylang':51.574245,'location':'Essex'},
        119 : {'citylong':-2.796721,'citylang':56.339775,'location':'St Andrews'},
        120 : {'citylong':-82.331395,'citylang':28.835451,'location':'Inverness'},
        121 : {'citylong':-3.188267,'citylang':55.953252,'location':'Edinburgh'},
        122 : {'citylong':-2.351248,'citylang':51.638025,'location':'Wotton-under-Edge'},
    }
    
    for k, v in profiles.items():
        user = Profile.objects.get(pk=k)
        user.citylong = v['citylong']
        user.citylang = v['citylang']
        user.location = v['location']
        user.save()
        
    return render(request, 'preregister.html')