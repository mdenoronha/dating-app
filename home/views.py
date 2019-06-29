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
    from django.db.models.expressions import RawSQL
    
    gcd_formula = "6371 * acos(cos(radians(%s)) * \
        cos(radians(profiles_profile.cityLat)) \
        * cos(radians(profiles_profile.cityLong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(profiles_profile.cityLat)))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (30, 20, 30)
    )
    
    closest_profiles = Profile.objects.annotate(distance=distance_raw_sql)
    print(closest_profiles)

    return render(request, 'preregister.html')