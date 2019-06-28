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
    'user1':{"username":"tshewery0","email":"aygoe0@go.com","password":"TempPass"},
    'user2':{"username":"dpleass1","email":"hjordon1@tuttocitta.it","password":"TempPass"},
    'user3':{"username":"santrack2","email":"hgerrish2@chron.com","password":"TempPass"},
    'user4':{"username":"kcompfort3","email":"crarity3@infoseek.co.jp","password":"TempPass"},
    'user5':{"username":"sbellson4","email":"ahalkyard4@usnews.com","password":"TempPass"},
    'user6':{"username":"qbentame5","email":"jmaystone5@adobe.com","password":"TempPass"},
    'user7':{"username":"zortiger6","email":"eilive6@qq.com","password":"TempPass"},
    'user8':{"username":"mround7","email":"srobertz7@tuttocitta.it","password":"TempPass"},
    'user9':{"username":"bhebditch8","email":"lmountcastle8@harvard.edu","password":"TempPass"},
    'user10':{"username":"kmcgorley9","email":"rcaines9@ebay.com","password":"TempPass"},
    'user11':{"username":"ttownsenda","email":"nbiglya@europa.eu","password":"TempPass"},
    'user12':{"username":"ecarabineb","email":"jlanktreeb@chronoengine.com","password":"TempPass"},
    'user13':{"username":"cbleesingc","email":"skynstonc@odnoklassniki.ru","password":"TempPass"},
    'user14':{"username":"olamped","email":"mmistryd@cmu.edu","password":"TempPass"},
    'user15':{"username":"tbicke","email":"mjorie@google.fr","password":"TempPass"},
    'user16':{"username":"yhallibonef","email":"jmillichapf@amazon.co.uk","password":"TempPass"},
    'user17':{"username":"kmiddlewickg","email":"tbrackeng@hp.com","password":"TempPass"},
    'user18':{"username":"itouhigh","email":"esainsburybrownh@usa.gov","password":"TempPass"},
    'user19':{"username":"pburbagei","email":"ssiddelli@theglobeandmail.com","password":"TempPass"},
    'user20':{"username":"wstorckj","email":"jfolkesj@blogtalkradio.com","password":"TempPass"},
    'user21':{"username":"bchadburnk","email":"ashoweringk@goo.gl","password":"TempPass"},
    'user22':{"username":"cdominkal","email":"asticklandl@guardian.co.uk","password":"TempPass"},
    'user23':{"username":"aratcliffm","email":"bsutterfieldm@nhs.uk","password":"TempPass"},
    'user24':{"username":"ecrocetton","email":"aswiersn@yandex.ru","password":"TempPass"},
    'user25':{"username":"wgowdridgeo","email":"rwoehlero@ezinearticles.com","password":"TempPass"},
    'user26':{"username":"cedmonstonp","email":"jaylingp@e-recht24.de","password":"TempPass"},
    'user27':{"username":"nlittrellq","email":"jwardleyq@fotki.com","password":"TempPass"},
    'user28':{"username":"bhurleyr","email":"sedworthyr@topsy.com","password":"TempPass"},
    'user29':{"username":"hmacvays","email":"kromneys@youtube.com","password":"TempPass"},
    'user30':{"username":"mlatcht","email":"olaxont@japanpost.jp","password":"TempPass"},
    'user31':{"username":"mdickonsu","email":"mmanzellu@oaic.gov.au","password":"TempPass"},
    'user32':{"username":"dbartodv","email":"zpepperellv@acquirethisname.com","password":"TempPass"},
    'user33':{"username":"ashapcotew","email":"lbeckittw@etsy.com","password":"TempPass"},
    'user34':{"username":"nbouldsx","email":"cchildx@washington.edu","password":"TempPass"},
    'user35':{"username":"nmushety","email":"lkiessely@usgs.gov","password":"TempPass"},
    'user36':{"username":"mshelmerdinez","email":"tspaldinz@ifeng.com","password":"TempPass"},
    'user37':{"username":"cswainson10","email":"lamorts10@google.com.au","password":"TempPass"},
    'user38':{"username":"broulston11","email":"blandeg11@51.la","password":"TempPass"},
    'user39':{"username":"dlaba12","email":"ccalken12@trellian.com","password":"TempPass"},
    'user40':{"username":"cstratiff13","email":"aiannazzi13@photobucket.com","password":"TempPass"},
    'user41':{"username":"cdonovin14","email":"abigham14@squarespace.com","password":"TempPass"},
    'user42':{"username":"nridolfi15","email":"twyeld15@newsvine.com","password":"TempPass"},
    'user43':{"username":"tinglese16","email":"rbrizland16@meetup.com","password":"TempPass"},
    'user44':{"username":"cmonget17","email":"aclynman17@netscape.com","password":"TempPass"},
    'user45':{"username":"brobben18","email":"mszwarc18@elegantthemes.com","password":"TempPass"},
    'user46':{"username":"smatyugin19","email":"dclara19@sina.com.cn","password":"TempPass"},
    'user47':{"username":"lswayne1a","email":"vwittke1a@fda.gov","password":"TempPass"},
    'user48':{"username":"smcowen1b","email":"vmarcam1b@webmd.com","password":"TempPass"},
    'user49':{"username":"cskullet1c","email":"bfinlan1c@fotki.com","password":"TempPass"},
    'user50':{"username":"kconeley1d","email":"htaffs1d@yelp.com","password":"TempPass"},
    'user51':{"username":"belcoate1e","email":"cquodling1e@networkadvertising.org","password":"TempPass"},
    'user52':{"username":"batheis1f","email":"amolson1f@nature.com","password":"TempPass"},
    'user53':{"username":"mquigley1g","email":"gfolshom1g@illinois.edu","password":"TempPass"},
    'user54':{"username":"teakeley1h","email":"tlittefair1h@va.gov","password":"TempPass"},
    'user55':{"username":"bfleckness1i","email":"vbrackpool1i@behance.net","password":"TempPass"},
    'user56':{"username":"qgianiello1j","email":"hjoscelin1j@4shared.com","password":"TempPass"},
    'user57':{"username":"scosgrove1k","email":"bnoddings1k@guardian.co.uk","password":"TempPass"},
    'user58':{"username":"dcolly1l","email":"ftomson1l@google.com.hk","password":"TempPass"},
    'user59':{"username":"nkinnach1m","email":"dlegat1m@over-blog.com","password":"TempPass"},
    'user60':{"username":"afairchild1n","email":"rundrill1n@msn.com","password":"TempPass"},
    'user61':{"username":"apeetermann1o","email":"rtidcomb1o@rambler.ru","password":"TempPass"},
    'user62':{"username":"akarczinski1p","email":"gdamp1p@storify.com","password":"TempPass"},
    'user63':{"username":"jbeddard1q","email":"tmarcone1q@issuu.com","password":"TempPass"},
    'user64':{"username":"rwinney1r","email":"emenlow1r@pinterest.com","password":"TempPass"},
    'user65':{"username":"jsich1s","email":"fshoard1s@bbc.co.uk","password":"TempPass"},
    'user66':{"username":"wpickburn1t","email":"jbrownsword1t@dedecms.com","password":"TempPass"},
    'user67':{"username":"rspinney1u","email":"alouca1u@mayoclinic.com","password":"TempPass"},
    'user68':{"username":"cbarrick1v","email":"wchristofol1v@quantcast.com","password":"TempPass"},
    'user69':{"username":"rconsidine1w","email":"jmessager1w@google.com.au","password":"TempPass"},
    'user70':{"username":"rballingal1x","email":"akubanek1x@is.gd","password":"TempPass"},
    'user71':{"username":"srime1y","email":"jsharrock1y@newsvine.com","password":"TempPass"},
    'user72':{"username":"jledgerton1z","email":"rreeken1z@drupal.org","password":"TempPass"},
    'user73':{"username":"kcossum20","email":"icheetham20@wordpress.org","password":"TempPass"},
    'user74':{"username":"acollcott21","email":"kmcspirron21@reference.com","password":"TempPass"},
    'user75':{"username":"sborell22","email":"cskates22@earthlink.net","password":"TempPass"},
    'user76':{"username":"oainge23","email":"dwemm23@statcounter.com","password":"TempPass"},
    'user77':{"username":"hpardue24","email":"zandries24@zdnet.com","password":"TempPass"},
    'user78':{"username":"dmactrustie25","email":"obellam25@feedburner.com","password":"TempPass"},
    'user79':{"username":"igallego26","email":"pemlen26@4shared.com","password":"TempPass"},
    'user80':{"username":"sgorcke27","email":"bgeal27@arstechnica.com","password":"TempPass"},
    'user81':{"username":"cdobbie28","email":"tbeare28@sakura.ne.jp","password":"TempPass"},
    'user82':{"username":"mragdale29","email":"egarrow29@phpbb.com","password":"TempPass"},
    'user83':{"username":"ebabar2a","email":"zsaunier2a@businesswire.com","password":"TempPass"},
    'user84':{"username":"kbeaford2b","email":"orattenbury2b@ted.com","password":"TempPass"},
    'user85':{"username":"ggodley2c","email":"psharrard2c@sphinn.com","password":"TempPass"},
    'user86':{"username":"aebrall2d","email":"agrealish2d@canalblog.com","password":"TempPass"},
    'user87':{"username":"ehulcoop2e","email":"pbroom2e@chicagotribune.com","password":"TempPass"},
    'user88':{"username":"krodder2f","email":"ccomar2f@umn.edu","password":"TempPass"},
    'user89':{"username":"ckenyam2g","email":"ogarbar2g@mozilla.com","password":"TempPass"},
    'user90':{"username":"mbalfour2h","email":"hklimkovich2h@themeforest.net","password":"TempPass"},
    'user91':{"username":"schallice2i","email":"eobradden2i@is.gd","password":"TempPass"},
    'user92':{"username":"cspoward2j","email":"aatling2j@hc360.com","password":"TempPass"},
    'user93':{"username":"kbebbell2k","email":"mthorley2k@live.com","password":"TempPass"},
    'user94':{"username":"bpentelo2l","email":"ggisbourn2l@sun.com","password":"TempPass"},
    'user95':{"username":"xgazzard2m","email":"khume2m@tripadvisor.com","password":"TempPass"},
    'user96':{"username":"aheater2n","email":"mhowson2n@delicious.com","password":"TempPass"},
    'user97':{"username":"tgrishakov2o","email":"kbusby2o@amazon.co.uk","password":"TempPass"},
    'user98':{"username":"jhazelton2p","email":"nbeecham2p@devhub.com","password":"TempPass"},
    'user99':{"username":"rgutman2q","email":"lwillgoss2q@sciencedirect.com","password":"TempPass"},
    'user100':{"username":"dnisius2r","email":"cpietasch2r@wikipedia.org","password":"TempPass"}
    }
    
    for k,v in profiles.items():
        k = User.objects.create_user(username=v["username"],
                                    email=v["email"],
                                    password=v["password"]
        )
    
    return render(request, 'preregister.html')