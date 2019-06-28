from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms import modelformset_factory
from profiles.forms import UserLoginForm, UserRegistrationForm, ProfileForm, ProfileImageForm, MessagesForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile, ProfileImage
from chat.models import Conversations, Messages, Views

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
    
# Check this works after changing MEN to MALE
def looking_for_check(request, user_one, user_two):
    if not user_one == user_two:
        if user_one.looking_for == "MALE":
            if not user_two.gender == "MALE":
                return redirect(reverse('index'))
        elif user_one.looking_for == "FEMALE":
            if not user_two.gender == "FEMALE":
                return redirect(reverse('index'))

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect(reverse('preregister'))
    
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                messages.success(request, "Logged In Successfully")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else: 
                login_form.add_error(None, "Username or password is incorrect")
    else:
        login_form = UserLoginForm()
            
    context = {
        'login_form':login_form
    }
    return render(request, 'login.html', context)
    

def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            if user:
                messages.success(request, "Your account had been created")
                auth.login(user=user, request=request)
                return redirect(reverse('create_profile'))
            else:
                messages.error(request, "We have been unable to create your account")
    else:
        registration_form = UserRegistrationForm()
        

    context = {
        'registration_form':registration_form
    }
    return render(request, 'register.html', context)

@login_required
def user_profile(request):
    user = User.objects.get(email=request.user.email)
    user.profileimage_set.all()
    context = {
        'profile':user,
    }
    return render(request, 'profile.html', context)
 
@login_required  
def create_profile(request):
    # user = User.objects.get(email=request.user.email)
    # profile_user_id = user.profile.id
    
    # https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)

    if request.method == "POST":
        # Why doesn't instance work?
        
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES)
        
        formset = ImageFormSet(request.POST, request.FILES,
                              queryset=ProfileImage.objects.filter(user_id=request.user.id).all())
                        

        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.is_verified = 'TO BE APPROVED'
            instance.save()
            
            # Delete checked images
            deleted_images = request.POST.getlist('delete')
            print(deleted_images)
            for image in deleted_images:
                if not image == "None":
                    ProfileImage.objects.get(pk=image).delete()
            
            for form in formset:
                if form.is_valid() and form.has_changed():
                    instance_image = form.save(commit=False)
                    instance_image.user = request.user
                    instance_image.is_verified = False
                    instance_image.save()
                    
                    # image = form['image']
                    # profile_photo = ProfileImage(user=request.user, image=image, is_verified=False)
                    # profile_photo.save()
                    # Add progress bar
            
            return redirect(reverse('index'))
            
    else:
        # user_profile = Profile.objects.get(pk=profile_user_id)
        profile_form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        initial_images = [{'image_url': i.image} for i in ProfileImage.objects.filter(user_id=request.user.id).all() if i.image]
        formset = ImageFormSet(queryset=ProfileImage.objects.filter(user_id=request.user.id).all(), initial=initial_images)
        
    # AIzaSyAMjDIJJGvw9xwl6n-0Gbm2961UDo9Jato

        
        
    context = {
        'profile_form':profile_form,
        'image_form':image_form,
        'formset': formset
    }
        
    return render(request, 'create-profile.html', context)    
    
@login_required 
def member_profile(request, id):
    # Add check if correct gender prefernce (for both)

    # Add check member is current user
    member = User.objects.get(id=id)
    
    if not member == request.user:
        current_user = False
    
        result = looking_for_check(request, request.user.profile, member.profile)
        if result:
            return result
        result = looking_for_check(request, member.profile, request.user.profile)
        if result:
            return result
        
        # Add view if last view is not read or user hasn't view member before
        last_view = Views.objects.filter(receiver_id=id).filter(sender_id=request.user.id).last()
        if not last_view or last_view.is_read:
            view = Views(receiver=member, sender=request.user)
            view.save()

        if request.method == "POST" and 'message_submit' in request.POST:
            message_form = MessagesForm(request.POST)
            if message_form.is_valid():
                conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=id)
                if conversation.exists():
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = User.objects.get(pk=id)
                    message.conversation = conversation[0]
                    message.save()
                    return redirect('/chat/%s' % conversation[0].id )
                else:
                    receiver = User.objects.get(pk=id)
                    conversation = Conversations()
                    conversation.save()
                    conversation.participants.add(request.user.id)
                    conversation.participants.add(receiver)
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = receiver
                    message.conversation = conversation
                    message.save()
                    return redirect('/chat/%s' % conversation.id )
        else:
            message_form = MessagesForm()
    else:
        message_form = MessagesForm()
        current_user = True
        
    context = {
        'member':member,
        'message_form': message_form,
        'current_user': current_user
    }
    return render(request, 'member.html', context)