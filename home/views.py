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
        'nbouldsx' : {'citylong':-1.04281,'citylang':51.85339,'location':'Ludgershall'},
        'kconeley1d' : {'citylong':-0.902918,'citylang':51.451652,'location':'Redditch'},
        'dcolly1l' : {'citylong':-6.04172,'citylang':54.51006,'location':'Lisburn'},
        'lswayne1a' : {'citylong':-2.59168,'citylang':51.45379,'location':'Bristol'},
        'hmacvays' : {'citylong':-5.8316,'citylang':54.46048,'location':'Saintfield'},
        'aratcliffm' : {'citylong':-6.25419,'citylang':54.10116,'location':'Warrenpoint'},
        'pburbagei' : {'citylong':-3.7527,'citylang':56.10769,'location':'Clackmannan'},
        'mdickonsu' : {'citylong':-2.34873,'citylang':54.47327,'location':'Kirkby Stephen'},
        'nkinnach1m' : {'citylong':-0.342274,'citylang':51.588142,'location':'Harrow'},
        'ashapcotew' : {'citylong':-3.02666,'citylang':53.184872,'location':'Hawarden'},
        'wstorckj' : {'citylong':-3.22333,'citylang':53.2747,'location':'Holywell'},
        'cdominkal' : {'citylong':-3.59423,'citylang':55.978371,'location':'Linlithgow'},
        'bhurleyr' : {'citylong':-3.15219,'citylang':55.880638,'location':'Loanhead'},
        'dbartodv' : {'citylong':-3.05374,'citylang':55.94215,'location':'Musselburgh'},
        'cstratiff13' : {'citylong':-3.23048,'citylang':56.06002,'location':'Burntisland'},
        'smcowen1b' : {'citylong':-3.18395,'citylang':56.21168,'location':'Collydean'},
        'nridolfi15' : {'citylong':-3.34329,'citylang':56.110222,'location':'Cowdenbeath'},
        'teakeley1h' : {'citylong':-1.35614,'citylang':53.72591,'location':'Castleford'},
        'brobben18' : {'citylong':-1.71354,'citylang':53.723049,'location':'Cleckheaton'},
        'mlatcht' : {'citylong':-1.89452,'citylang':53.80236,'location':'Denholme'},
        'cswainson10' : {'citylong':-1.63284,'citylang':53.691551,'location':'Dewsbury'},
        'bfleckness1i' : {'citylong':-2.03484,'citylang':52.568981,'location':'Darlaston'},
        'bchadburnk' : {'citylong':-2.08734,'citylang':52.508671,'location':'Dudley'},
        'qgianiello1j' : {'citylong':-1.74484,'citylang':52.48758,'location':'Fordbridge'},
        'scosgrove1k' : {'citylong':-0.46804,'citylang':52.135712,'location':'Bedford'},
        'nlittrellq' : {'citylong':-1.56756,'citylang':54.94226,'location':'Windy Nook'},
        'cedmonstonp' : {'citylong':-1.86827,'citylang':52.217049,'location':'Alcester'},
        'cmonget17' : {'citylong':-0.10193,'citylang':51.24061,'location':'Beltchingley'},
        'nmushety' : {'citylong':-0.7444,'citylang':51.340248,'location':'Camberley'},
        'cskullet1c' : {'citylong':-0.50776,'citylang':51.388168,'location':'Chertsey'},
        'belcoate1e' : {'citylong':1.44002,'citylang':52.454632,'location':'Bungay'},
        'wgowdridgeo' : {'citylong':0.710493,'citylang':52.242924,'location':'Bury St Edmunds'},
        'cdonovin14' : {'citylong':1.69417,'citylang':52.45145,'location':'Carlton Colville'},
        'broulston11' : {'citylong':-0.52313,'citylang':51.887619,'location':'Dunstable'},
        'smatyugin19' : {'citylong':-3.47952,'citylang':51.64522,'location':'Rhondda'},
        'mquigley1g' : {'citylong':-0.52028,'citylang':51.90461,'location':'Houghton Regis'},
        'tinglese16' : {'citylong':-3.943646,'citylang':51.621441,'location':'Swansea'},
        'ecrocetton' : {'citylong':-0.24846,'citylang':52.573391,'location':'Peterborough'},
        'mshelmerdinez' : {'citylong':-5.35325,'citylang':36.14491,'location':'Ramsey'},
        'batheis1f' : {'citylong':0.33713,'citylang':52.334099,'location':'Soham'},
        'dlaba12' : {'citylong':-0.265103,'citylang':52.230083,'location':'St Neots'},
    }
    
    for k, v in profiles.items():
        user = Profile.objects.get(user__username=k)
        user.citylong = v['citylong']
        user.citylang = v['citylang']
        user.location = v['location']
        user.save()
        
    return render(request, 'preregister.html')