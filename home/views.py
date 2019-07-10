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
    
    User.objects.create_user(username='dberzons0',email='gbedson0@tuttocitta.it',password='TempPass')
    User.objects.create_user(username='bcorringham1',email='cgreated1@diigo.com',password='TempPass')
    User.objects.create_user(username='mbumphrey2',email='jgreig2@t.co',password='TempPass')
    User.objects.create_user(username='kalcoran3',email='dbinks3@storify.com',password='TempPass')
    User.objects.create_user(username='chedderly4',email='jdoyle4@samsung.com',password='TempPass')
    User.objects.create_user(username='ogetley5',email='fbennoe5@cloudflare.com',password='TempPass')
    User.objects.create_user(username='aroback6',email='cpilling6@independent.co.uk',password='TempPass')
    User.objects.create_user(username='kbatkin7',email='rhaily7@jalbum.net',password='TempPass')
    User.objects.create_user(username='ghabishaw8',email='ahitscher8@google.ca',password='TempPass')
    User.objects.create_user(username='zdutnall9',email='cbernakiewicz9@boston.com',password='TempPass')
    User.objects.create_user(username='kfaersa',email='klodewicka@archive.org',password='TempPass')
    User.objects.create_user(username='abadcockb',email='ttaggertb@sfgate.com',password='TempPass')
    User.objects.create_user(username='mkellerc',email='kwigzellc@chicagotribune.com',password='TempPass')
    User.objects.create_user(username='lgetchd',email='lsaunierd@dropbox.com',password='TempPass')
    User.objects.create_user(username='pfawdriee',email='nffrenche@bing.com',password='TempPass')
    User.objects.create_user(username='gstivensf',email='kbirdenf@bloomberg.com',password='TempPass')
    User.objects.create_user(username='pabramchikg',email='kbinnerg@springer.com',password='TempPass')
    User.objects.create_user(username='jnielsonh',email='lbonnickh@redcross.org',password='TempPass')
    User.objects.create_user(username='asurridgei',email='rdugoodi@ow.ly',password='TempPass')
    User.objects.create_user(username='drigglesfordj',email='gscoulerj@google.com.au',password='TempPass')
    User.objects.create_user(username='ldelavaletteparisotk',email='wstrikek@wsj.com',password='TempPass')
    User.objects.create_user(username='bmacallasterl',email='rbottl@usnews.com',password='TempPass')
    User.objects.create_user(username='xgierckem',email='abrassillm@exblog.jp',password='TempPass')
    User.objects.create_user(username='bmyrtlen',email='ogowthropn@taobao.com',password='TempPass')
    User.objects.create_user(username='tgairdnero',email='flabelo@tinyurl.com',password='TempPass')
    User.objects.create_user(username='shaydockp',email='cosgordbyp@example.com',password='TempPass')
    User.objects.create_user(username='rreinq',email='rcockinq@alibaba.com',password='TempPass')
    User.objects.create_user(username='qoneilr',email='djuhruker@ustream.tv',password='TempPass')
    User.objects.create_user(username='koverys',email='lcopperwaites@wordpress.com',password='TempPass')
    User.objects.create_user(username='kcastanost',email='redlynt@go.com',password='TempPass')
    User.objects.create_user(username='tbradlaughu',email='mferrieru@princeton.edu',password='TempPass')
    User.objects.create_user(username='gbalmv',email='nmaytev@flickr.com',password='TempPass')
    User.objects.create_user(username='hmcurew',email='dmerillw@princeton.edu',password='TempPass')
    User.objects.create_user(username='mburnardx',email='mschapirox@gravatar.com',password='TempPass')
    User.objects.create_user(username='arichmonty',email='wmarkovay@hud.gov',password='TempPass')
    User.objects.create_user(username='ssmithez',email='hsedgez@vistaprint.com',password='TempPass')
    User.objects.create_user(username='fupward10',email='jcornier10@domainmarket.com',password='TempPass')
    User.objects.create_user(username='jbushe11',email='epetrovic11@slideshare.net',password='TempPass')
    User.objects.create_user(username='emanoelli12',email='mbarnson12@e-recht24.de',password='TempPass')
    User.objects.create_user(username='ikrier13',email='blavelle13@linkedin.com',password='TempPass')
    User.objects.create_user(username='speyntue14',email='wmcowis14@tiny.cc',password='TempPass')
    User.objects.create_user(username='tcommuzzo15',email='tfay15@sina.com.cn',password='TempPass')
    User.objects.create_user(username='jpitkeathley16',email='cisakovic16@tumblr.com',password='TempPass')
    User.objects.create_user(username='scomberbeach17',email='ydubarry17@hp.com',password='TempPass')
    User.objects.create_user(username='mlough18',email='gquipp18@sina.com.cn',password='TempPass')
    User.objects.create_user(username='mrallinshaw19',email='kblackstock19@admin.ch',password='TempPass')
    User.objects.create_user(username='lcribbott1a',email='swadelin1a@narod.ru',password='TempPass')
    User.objects.create_user(username='megell1b',email='kfenix1b@unblog.fr',password='TempPass')
    User.objects.create_user(username='lprendeguest1c',email='mvagges1c@usgs.gov',password='TempPass')
    User.objects.create_user(username='djumonet1d',email='dbroke1d@cnn.com',password='TempPass')
    User.objects.create_user(username='aroussell1e',email='rhaquard1e@com.com',password='TempPass')
    User.objects.create_user(username='hcicullo1f',email='fbannerman1f@illinois.edu',password='TempPass')
    User.objects.create_user(username='dravilious1g',email='bjoan1g@ask.com',password='TempPass')
    User.objects.create_user(username='njovis1h',email='csowthcote1h@addthis.com',password='TempPass')
    User.objects.create_user(username='kbunning1i',email='obrennand1i@clickbank.net',password='TempPass')
    User.objects.create_user(username='jbilbie1j',email='cbraunter1j@mapquest.com',password='TempPass')
    User.objects.create_user(username='jmilan1k',email='sionesco1k@hibu.com',password='TempPass')
    User.objects.create_user(username='eguyonnet1l',email='cthunderchief1l@mit.edu',password='TempPass')
    User.objects.create_user(username='dfranck1m',email='bmaior1m@intel.com',password='TempPass')
    User.objects.create_user(username='nquincee1n',email='srafter1n@nps.gov',password='TempPass')
    User.objects.create_user(username='mcantillion1o',email='scousins1o@arizona.edu',password='TempPass')
    User.objects.create_user(username='atoplin1p',email='cpoveleye1p@psu.edu',password='TempPass')
    User.objects.create_user(username='mpickaver1q',email='aclair1q@linkedin.com',password='TempPass')
    User.objects.create_user(username='mlegerton1r',email='aderuggiero1r@biblegateway.com',password='TempPass')
    User.objects.create_user(username='czupo1s',email='bewert1s@dmoz.org',password='TempPass')
    User.objects.create_user(username='hcarding1t',email='dtomasino1t@washington.edu',password='TempPass')
    User.objects.create_user(username='lwims1u',email='opatkin1u@php.net',password='TempPass')
    User.objects.create_user(username='dduran1v',email='gbusher1v@unc.edu',password='TempPass')
    User.objects.create_user(username='cryburn1w',email='espanton1w@opensource.org',password='TempPass')
    User.objects.create_user(username='lodowgaine1x',email='gmorecombe1x@samsung.com',password='TempPass')
    User.objects.create_user(username='bandres1y',email='nflitcroft1y@netvibes.com',password='TempPass')
    User.objects.create_user(username='adoe1z',email='imolineaux1z@freewebs.com',password='TempPass')
    User.objects.create_user(username='lkenchington20',email='rclohissy20@surveymonkey.com',password='TempPass')
    User.objects.create_user(username='sferrara21',email='rlambourne21@blogs.com',password='TempPass')
    User.objects.create_user(username='tholtham22',email='acream22@feedburner.com',password='TempPass')
    User.objects.create_user(username='sewington23',email='hwallbridge23@amazon.co.uk',password='TempPass')
    User.objects.create_user(username='bhiseman24',email='caynscombe24@cargocollective.com',password='TempPass')
    User.objects.create_user(username='bolphert25',email='yspurden25@nasa.gov',password='TempPass')
    User.objects.create_user(username='mranby26',email='rmonier26@eventbrite.com',password='TempPass')
    User.objects.create_user(username='nspalding27',email='jclowser27@si.edu',password='TempPass')
    User.objects.create_user(username='tthoresby28',email='pwinspur28@sohu.com',password='TempPass')
    User.objects.create_user(username='ltourle29',email='lallwright29@jigsy.com',password='TempPass')
    User.objects.create_user(username='oloyndon2a',email='dblance2a@independent.co.uk',password='TempPass')
    User.objects.create_user(username='jswaton2b',email='amarmon2b@yahoo.com',password='TempPass')
    User.objects.create_user(username='mnunson2c',email='bespadater2c@cafepress.com',password='TempPass')
    User.objects.create_user(username='awrightim2d',email='ibracchi2d@bizjournals.com',password='TempPass')
    User.objects.create_user(username='dmisk2e',email='oholwell2e@weebly.com',password='TempPass')
    User.objects.create_user(username='msaye2f',email='wpley2f@1688.com',password='TempPass')
    User.objects.create_user(username='rlaxston2g',email='hbracey2g@macromedia.com',password='TempPass')
    User.objects.create_user(username='mhuff2h',email='dgard2h@plala.or.jp',password='TempPass')
    User.objects.create_user(username='mwhitechurch2i',email='tmocquer2i@technorati.com',password='TempPass')
    User.objects.create_user(username='mmaffi2j',email='gnovkovic2j@youku.com',password='TempPass')
    User.objects.create_user(username='gbugg2k',email='tcaulket2k@surveymonkey.com',password='TempPass')
    User.objects.create_user(username='nmajor2l',email='yohanessian2l@eepurl.com',password='TempPass')
    User.objects.create_user(username='celsay2m',email='wmacauley2m@php.net',password='TempPass')
    User.objects.create_user(username='dbree2n',email='tlamberteschi2n@yolasite.com',password='TempPass')
    User.objects.create_user(username='dlangan2o',email='lcurtois2o@ocn.ne.jp',password='TempPass')
    User.objects.create_user(username='kyare2p',email='tjahan2p@senate.gov',password='TempPass')
    User.objects.create_user(username='dbambrough2q',email='adunlop2q@census.gov',password='TempPass')
    User.objects.create_user(username='ngrave2r',email='pespinel2r@mapy.cz',password='TempPass')
 
    return render(request, 'index.html')