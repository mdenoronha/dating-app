from django.db import models
from django.contrib.auth.models import User
from chat.models import Conversations
from checkout.models import Subscription
from django.db.models.signals import post_save, pre_delete
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
import os
import math
from django.db.models.expressions import RawSQL
import stripe
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import os


"""
Only necessary for local and testing sqlite databases
As SQLite does not support math functions, the following function adds the
capability for it to do so
"""
if "DEVELOPMENT" in os.environ or "TESTING" in os.environ:
    @receiver(connection_created)
    def extend_sqlite(connection=None, **kwargs):
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)

class LocationManager(models.Manager):
    
    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, citylat, citylong, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        gcd_formula = "6371 * acos(cos(radians(%s)) * \
        cos(radians(citylat)) \
        * cos(radians(citylong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(citylat)))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (citylat, citylong, citylat)
        )
    
        if max_distance is not None:
            return self.annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
        else:
            return self.annotate(distance=distance_raw_sql)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='', blank=False)
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A LITTLE EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
        ('BOTH', 'Both'),
    )
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
    
    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved')
    )
    ETHNICITY = (
        ('WHITE', 'White'),
        ('ASIAN: INDIAN', 'Asian: Indian'),
        ('ASIAN: PAKISTANI', 'Asian: Pakistani'),
        ('ASIAN: BANGLADESHI', 'Asian: Bangladeshi'),
        ('ASIAN: CHINESE', 'Asian: Chinese'),
        ('BLACK', 'Black'),
        ('MIXED', 'Mixed'),
        ('OTHER ETHNICITY', 'Other Ethnicity')
    )
    RELATIONSHIP_STATUS = (
        ('NEVER MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated')
    )
    EDUCATION = (
    ('HIGH SCHOOL', 'High School'),
    ('COLLEGE', 'College'),
    ('BACHELORS DEGREE', 'Bachelors Degree'),
    ('MASTERS', 'Masters'),
    ('PHD / POST DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"))

    gender = models.CharField(choices=GENDER, default="MALE", max_length=6)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER MARRIED", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10)
    body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='', blank=False)
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)
    
    objects = LocationManager()
    
    # Assistance from https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

# Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)
    
class ProfileImage(models.Model):
    
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
    
    user = models.ForeignKey(User, default=None)
    image = models.ImageField(upload_to=image_filename, blank=True)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)

def pre_delete_user(sender, instance, **kwargs):
    # Before user deleted, delete all conversations they were participants of
    conversations = Conversations.objects.filter(participants=instance.id)
    for conversation in conversations:
        conversation.delete()
    
    # Before user deleted, cancel all subscriptions
    customer = Subscription.objects.filter(user_id=instance.id).first()
    try:
        if customer:
            stripe_customer = stripe.Customer.retrieve(customer.customer_id)
            for sub in stripe_customer.subscriptions.data:
                stripe.Subscription.modify(
                    sub.id,
                    cancel_at_period_end=True
                )
    except:
        print('Pre-delete user failed')
        
pre_delete.connect(pre_delete_user, sender=User)
