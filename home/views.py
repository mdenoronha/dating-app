from django.shortcuts import render
from profiles.models import Profile
from django.db.models import Q, F
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import datetime as DT
from django.contrib.auth.models import User


# Create your views here.
@login_required
def index(request):

    # Change limit
    # 'or' needed in gender check https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
    # Exclude current user
    # Nearby Profiles
    if request.user.profile.looking_for == "BOTH":
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
    else:
        closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
    # Profiles for quick match finder
    if request.user.profile.looking_for == "BOTH":
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).all()
    else:
        card_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).all()
    
    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)
    # Filter date_joined
    # Profiles for active most recently  
    if request.user.profile.looking_for == "BOTH":
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
    # Profiles for newest
    if request.user.profile.looking_for == "BOTH":
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
    else:
        newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.cityLat), float(request.user.profile.cityLong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

    context = {
        'closest_profiles':closest_profiles,
        'active_profiles':active_profiles,
        'newest_profiles': newest_profiles,
        'card_profiles': card_profiles
    }
    
    return render(request, 'index.html', context)
    
def preregister(request):

    profiles = { 
    'maleuser1' = Profileimage(image='images/male1.jpg', user_id=1),
    'maleuser2' = Profileimage(image='images/male2.jpg', user_id=2),
    'maleuser3' = Profileimage(image='images/male3.jpg', user_id=4),
    'maleuser4' = Profileimage(image='images/male4.jpg', user_id=11),
    'maleuser5' = Profileimage(image='images/male5.jpg', user_id=13),
    'maleuser6' = Profileimage(image='images/male6.jpg', user_id=14),
    'maleuser7' = Profileimage(image='images/male7.jpg', user_id=17),
    'maleuser8' = Profileimage(image='images/male8.jpg', user_id=18),
    'maleuser9' = Profileimage(image='images/male9.jpg', user_id=19),
    'maleuser10' = Profileimage(image='images/male10.jpg', user_id=22),
    'maleuser11' = Profileimage(image='images/male11.jpg', user_id=23),
    'maleuser12' = Profileimage(image='images/male12.jpg', user_id=25),
    'maleuser13' = Profileimage(image='images/male13.jpg', user_id=26),
    'maleuser14' = Profileimage(image='images/male14.jpg', user_id=30),
    'maleuser15' = Profileimage(image='images/male15.jpg', user_id=31),
    'maleuser16' = Profileimage(image='images/male16.jpg', user_id=34),
    'maleuser17' = Profileimage(image='images/male17.jpg', user_id=38),
    'maleuser18' = Profileimage(image='images/male18.jpg', user_id=39),
    'maleuser19' = Profileimage(image='images/male19.jpg', user_id=40),
    'maleuser20' = Profileimage(image='images/male20.jpg', user_id=43),
    'maleuser21' = Profileimage(image='images/male21.jpg', user_id=44),
    'maleuser22' = Profileimage(image='images/male22.jpg', user_id=46),
    'maleuser23' = Profileimage(image='images/male23.jpg', user_id=48),
    'maleuser24' = Profileimage(image='images/male24.jpg', user_id=49),
    'maleuser25' = Profileimage(image='images/male25.jpg', user_id=56),
    'maleuser26' = Profileimage(image='images/male26.jpg', user_id=57),
    'maleuser27' = Profileimage(image='images/male27.jpg', user_id=60),
    'maleuser28' = Profileimage(image='images/male28.jpg', user_id=63),
    'maleuser29' = Profileimage(image='images/male29.jpg', user_id=66),
    'maleuser30' = Profileimage(image='images/male30.jpg', user_id=67),
    'maleuser31' = Profileimage(image='images/male31.jpg', user_id=68),
    'maleuser32' = Profileimage(image='images/male32.jpg', user_id=71),
    'maleuser33' = Profileimage(image='images/male33.jpg', user_id=72),
    'maleuser34' = Profileimage(image='images/male34.jpg', user_id=73),
    'maleuser35' = Profileimage(image='images/male35.jpg', user_id=74),
    'maleuser36' = Profileimage(image='images/male36.jpg', user_id=75),
    'maleuser37' = Profileimage(image='images/male37.jpg', user_id=76),
    'maleuser38' = Profileimage(image='images/male38.jpg', user_id=78),
    'maleuser39' = Profileimage(image='images/male39.jpg', user_id=79),
    'maleuser40' = Profileimage(image='images/male40.jpg', user_id=80),
    'maleuser41' = Profileimage(image='images/male41.jpg', user_id=81),
    'maleuser42' = Profileimage(image='images/male42.jpg', user_id=86),
    'maleuser43' = Profileimage(image='images/male43.jpg', user_id=87),
    'maleuser44' = Profileimage(image='images/male44.jpg', user_id=89),
    'maleuser45' = Profileimage(image='images/male45.jpg', user_id=95),
    'maleuser46' = Profileimage(image='images/male46.jpg', user_id=96),
    'maleuser47' = Profileimage(image='images/male47.jpg', user_id=97),
    'maleuser48' = Profileimage(image='images/male48.jpg', user_id=99),
    'maleuser49' = Profileimage(image='images/male49.jpg', user_id=101),
    'maleuser50' = Profileimage(image='images/male49.jpg', user_id=1),
    'maleuser51' = Profileimage(image='images/male48.jpg', user_id=2),
    'maleuser52' = Profileimage(image='images/male47.jpg', user_id=4),
    'maleuser53' = Profileimage(image='images/male46.jpg', user_id=11),
    'maleuser54' = Profileimage(image='images/male45.jpg', user_id=13),
    'maleuser55' = Profileimage(image='images/male44.jpg', user_id=14),
    'maleuser56' = Profileimage(image='images/male43.jpg', user_id=17),
    'maleuser57' = Profileimage(image='images/male42.jpg', user_id=18),
    'maleuser58' = Profileimage(image='images/male41.jpg', user_id=19),
    'maleuser59' = Profileimage(image='images/male40.jpg', user_id=22),
    'maleuser60' = Profileimage(image='images/male39.jpg', user_id=23),
    'maleuser61' = Profileimage(image='images/male38.jpg', user_id=25),
    'maleuser62' = Profileimage(image='images/male37.jpg', user_id=26),
    'maleuser63' = Profileimage(image='images/male36.jpg', user_id=30),
    'maleuser64' = Profileimage(image='images/male35.jpg', user_id=31),
    'maleuser65' = Profileimage(image='images/male34.jpg', user_id=34),
    'maleuser66' = Profileimage(image='images/male33.jpg', user_id=38),
    'maleuser67' = Profileimage(image='images/male32.jpg', user_id=39),
    'maleuser68' = Profileimage(image='images/male31.jpg', user_id=40),
    'maleuser69' = Profileimage(image='images/male30.jpg', user_id=43),
    'maleuser70' = Profileimage(image='images/male29.jpg', user_id=44),
    'maleuser71' = Profileimage(image='images/male28.jpg', user_id=46),
    'maleuser72' = Profileimage(image='images/male27.jpg', user_id=48),
    'maleuser73' = Profileimage(image='images/male26.jpg', user_id=49),
    'maleuser74' = Profileimage(image='images/male25.jpg', user_id=56),
    'maleuser75' = Profileimage(image='images/male24.jpg', user_id=57),
    'maleuser76' = Profileimage(image='images/male23.jpg', user_id=60),
    'maleuser77' = Profileimage(image='images/male22.jpg', user_id=63),
    'maleuser78' = Profileimage(image='images/male21.jpg', user_id=66),
    'maleuser79' = Profileimage(image='images/male20.jpg', user_id=67),
    'maleuser80' = Profileimage(image='images/male19.jpg', user_id=68),
    'maleuser81' = Profileimage(image='images/male18.jpg', user_id=71),
    'maleuser82' = Profileimage(image='images/male17.jpg', user_id=72),
    'maleuser83' = Profileimage(image='images/male16.jpg', user_id=73),
    'maleuser84' = Profileimage(image='images/male15.jpg', user_id=74),
    'maleuser85' = Profileimage(image='images/male14.jpg', user_id=75),
    'maleuser86' = Profileimage(image='images/male13.jpg', user_id=76),
    'maleuser87' = Profileimage(image='images/male12.jpg', user_id=78),
    'maleuser88' = Profileimage(image='images/male11.jpg', user_id=79),
    'maleuser89' = Profileimage(image='images/male10.jpg', user_id=80),
    'maleuser90' = Profileimage(image='images/male9.jpg', user_id=81),
    'maleuser91' = Profileimage(image='images/male8.jpg', user_id=86),
    'maleuser92' = Profileimage(image='images/male7.jpg', user_id=87),
    'maleuser93' = Profileimage(image='images/male6.jpg', user_id=89),
    'maleuser94' = Profileimage(image='images/male5.jpg', user_id=95),
    'maleuser95' = Profileimage(image='images/male4.jpg', user_id=96),
    'maleuser96' = Profileimage(image='images/male3.jpg', user_id=97),
    'maleuser97' = Profileimage(image='images/male2.jpg', user_id=99),
    'maleuser98' = Profileimage(image='images/male1.jpg', user_id=101),
    'femaleuser1' = Profileimage(image='images/female1.jpg', user_id=3),
    'femaleuser2' = Profileimage(image='images/female2.jpg', user_id=5),
    'femaleuser3' = Profileimage(image='images/female3.jpg', user_id=6),
    'femaleuser4' = Profileimage(image='images/female4.jpg', user_id=7),
    'femaleuser5' = Profileimage(image='images/female5.jpg', user_id=8),
    'femaleuser6' = Profileimage(image='images/female6.jpg', user_id=9),
    'femaleuser7' = Profileimage(image='images/female7.jpg', user_id=10),
    'femaleuser8' = Profileimage(image='images/female8.jpg', user_id=12),
    'femaleuser9' = Profileimage(image='images/female9.jpg', user_id=15),
    'femaleuser10' = Profileimage(image='images/female10.jpg', user_id=16),
    'femaleuser11' = Profileimage(image='images/female11.jpg', user_id=20),
    'femaleuser12' = Profileimage(image='images/female12.jpg', user_id=21),
    'femaleuser13' = Profileimage(image='images/female13.jpg', user_id=24),
    'femaleuser14' = Profileimage(image='images/female14.jpg', user_id=27),
    'femaleuser15' = Profileimage(image='images/female15.jpg', user_id=28),
    'femaleuser16' = Profileimage(image='images/female16.jpg', user_id=29),
    'femaleuser17' = Profileimage(image='images/female17.jpg', user_id=32),
    'femaleuser18' = Profileimage(image='images/female18.jpg', user_id=33),
    'femaleuser19' = Profileimage(image='images/female19.jpg', user_id=35),
    'femaleuser20' = Profileimage(image='images/female20.jpg', user_id=36),
    'femaleuser21' = Profileimage(image='images/female21.jpg', user_id=37),
    'femaleuser22' = Profileimage(image='images/female22.jpg', user_id=41),
    'femaleuser23' = Profileimage(image='images/female23.jpg', user_id=42),
    'femaleuser24' = Profileimage(image='images/female24.jpg', user_id=45),
    'femaleuser25' = Profileimage(image='images/female25.jpg', user_id=47),
    'femaleuser26' = Profileimage(image='images/female26.jpg', user_id=50),
    'femaleuser27' = Profileimage(image='images/female27.jpg', user_id=51),
    'femaleuser28' = Profileimage(image='images/female28.jpg', user_id=52),
    'femaleuser29' = Profileimage(image='images/female29.jpg', user_id=53),
    'femaleuser30' = Profileimage(image='images/female30.jpg', user_id=54),
    'femaleuser31' = Profileimage(image='images/female31.jpg', user_id=55),
    'femaleuser32' = Profileimage(image='images/female32.jpg', user_id=58),
    'femaleuser33' = Profileimage(image='images/female33.jpg', user_id=59),
    'femaleuser34' = Profileimage(image='images/female34.jpg', user_id=61),
    'femaleuser35' = Profileimage(image='images/female35.jpg', user_id=62),
    'femaleuser36' = Profileimage(image='images/female36.jpg', user_id=64),
    'femaleuser37' = Profileimage(image='images/female37.jpg', user_id=65),
    'femaleuser38' = Profileimage(image='images/female38.jpg', user_id=69),
    'femaleuser39' = Profileimage(image='images/female39.jpg', user_id=70),
    'femaleuser40' = Profileimage(image='images/female40.jpg', user_id=77),
    'femaleuser41' = Profileimage(image='images/female41.jpg', user_id=82),
    'femaleuser42' = Profileimage(image='images/female42.jpg', user_id=83),
    'femaleuser43' = Profileimage(image='images/female43.jpg', user_id=84),
    'femaleuser44' = Profileimage(image='images/female44.jpg', user_id=85),
    'femaleuser45' = Profileimage(image='images/female45.jpg', user_id=88),
    'femaleuser46' = Profileimage(image='images/female46.jpg', user_id=90),
    'femaleuser47' = Profileimage(image='images/female47.jpg', user_id=91),
    'femaleuser48' = Profileimage(image='images/female48.jpg', user_id=92),
    'femaleuser49' = Profileimage(image='images/female49.jpg', user_id=93),
    'femaleuser50' = Profileimage(image='images/female50.jpg', user_id=94),
    'femaleuser51' = Profileimage(image='images/female51.jpg', user_id=98),
    'femaleuser52' = Profileimage(image='images/female52.jpg', user_id=100),
    'femaleuser53' = Profileimage(image='images/female53.jpg', user_id=102),
    'femaleuser54' = Profileimage(image='images/.jpg', user_id=3),
    'femaleuser55' = Profileimage(image='images/.jpg', user_id=5),
    'femaleuser56' = Profileimage(image='images/.jpg', user_id=6),
    'femaleuser57' = Profileimage(image='images/.jpg', user_id=7),
    'femaleuser58' = Profileimage(image='images/.jpg', user_id=8),
    'femaleuser59' = Profileimage(image='images/.jpg', user_id=9),
    'femaleuser60' = Profileimage(image='images/.jpg', user_id=10),
    'femaleuser61' = Profileimage(image='images/.jpg', user_id=12),
    'femaleuser62' = Profileimage(image='images/.jpg', user_id=15),
    'femaleuser63' = Profileimage(image='images/.jpg', user_id=16),
    'femaleuser64' = Profileimage(image='images/.jpg', user_id=20),
    'femaleuser65' = Profileimage(image='images/.jpg', user_id=21),
    'femaleuser66' = Profileimage(image='images/.jpg', user_id=24),
    'femaleuser67' = Profileimage(image='images/.jpg', user_id=27),
    'femaleuser68' = Profileimage(image='images/.jpg', user_id=28),
    'femaleuser69' = Profileimage(image='images/.jpg', user_id=29),
    'femaleuser70' = Profileimage(image='images/.jpg', user_id=32),
    'femaleuser71' = Profileimage(image='images/.jpg', user_id=33),
    'femaleuser72' = Profileimage(image='images/.jpg', user_id=35),
    'femaleuser73' = Profileimage(image='images/.jpg', user_id=36),
    'femaleuser74' = Profileimage(image='images/.jpg', user_id=37),
    'femaleuser75' = Profileimage(image='images/.jpg', user_id=41),
    'femaleuser76' = Profileimage(image='images/.jpg', user_id=42),
    'femaleuser77' = Profileimage(image='images/.jpg', user_id=45),
    'femaleuser78' = Profileimage(image='images/.jpg', user_id=47),
    'femaleuser79' = Profileimage(image='images/.jpg', user_id=50),
    'femaleuser80' = Profileimage(image='images/.jpg', user_id=51),
    'femaleuser81' = Profileimage(image='images/.jpg', user_id=52),
    'femaleuser82' = Profileimage(image='images/.jpg', user_id=53),
    'femaleuser83' = Profileimage(image='images/.jpg', user_id=54),
    'femaleuser84' = Profileimage(image='images/.jpg', user_id=55),
    'femaleuser85' = Profileimage(image='images/.jpg', user_id=58),
    'femaleuser86' = Profileimage(image='images/.jpg', user_id=59),
    'femaleuser87' = Profileimage(image='images/.jpg', user_id=61),
    'femaleuser88' = Profileimage(image='images/.jpg', user_id=62),
    'femaleuser89' = Profileimage(image='images/.jpg', user_id=64),
    'femaleuser90' = Profileimage(image='images/.jpg', user_id=65),
    'femaleuser91' = Profileimage(image='images/.jpg', user_id=69),
    'femaleuser92' = Profileimage(image='images/.jpg', user_id=70),
    'femaleuser93' = Profileimage(image='images/.jpg', user_id=77),
    'femaleuser94' = Profileimage(image='images/.jpg', user_id=82),
    'femaleuser95' = Profileimage(image='images/.jpg', user_id=83),
    'femaleuser96' = Profileimage(image='images/.jpg', user_id=84),
    'femaleuser97' = Profileimage(image='images/.jpg', user_id=85),
    'femaleuser98' = Profileimage(image='images/.jpg', user_id=88),
    'femaleuser99' = Profileimage(image='images/.jpg', user_id=90),
    'femaleuser100' = Profileimage(image='images/.jpg', user_id=91),
    'femaleuser101' = Profileimage(image='images/.jpg', user_id=92),
    'femaleuser102' = Profileimage(image='images/.jpg', user_id=93),
    'femaleuser103' = Profileimage(image='images/.jpg', user_id=94),
    'femaleuser104' = Profileimage(image='images/.jpg', user_id=98),
    'femaleuser105' = Profileimage(image='images/.jpg', user_id=100),
    'femaleuser106' = Profileimage(image='images/.jpg', user_id=102),   
    }
    
    
    for k,v in profiles.items():
        k = ProfileImage(image=v["image"],
                    user_id=v["user_id"],
        )
        
        k.save()
    
    return render(request, 'preregister.html')