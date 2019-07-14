Dating Site
=============

[![Build Status](https://travis-ci.org/mdenoronha/dating-app.svg?branch=master)](https://travis-ci.org/mdenoronha/dating-app)

A milestone project displaying capabilities in HTML, CSS, Javascript, Python, the Django framework.</br>
The project is a website which allows users to create accounts, edit profiles and search and engage with other users.</br>
The project makes use of Bootstrap framwork for front end styling and functionality.</br>

The project can be found [here](https://dating-app-mvd.herokuapp.com/)

The project makes use of a verification system to verify or reject new profiles 
and profile images. A user account with sufficient permission is required to access
the verification system. The following user can be used for this:</br>
Username: verification</br>
Password: veripass</br>
Verification platform can be accessed [here](https://dating-app-mvd.herokuapp.com/admin/)

Verification staff can approve or reject profiles by following these steps:
1. Access the verification platform [here](https://dating-app-mvd.herokuapp.com/admin/)
2. Navigate to Profile
![Navigate to Profile](https://github.com/mdenoronha/dating-app/blob/master/media/instruction-images/verification-1.png?raw=true)
3. Select the profiles you wish to approve or reject
![Select the profiles you wish to approve or reject](https://github.com/mdenoronha/dating-app/blob/master/media/instruction-images/verification-2.png?raw=true)
4. Under actions select the appropriate action and click Go
![Under actions select the appropriate action and click Google](https://github.com/mdenoronha/dating-app/blob/master/media/instruction-images/verification-3.png?raw=true)
5. Verifying Profile Images using the same process however select Profile images instead of Profile for step 2


UX
---------------
The intended users are as follows:
* The main intended user is one who is looking to meet other individuals - primarily for dating
    * The site messages the 'dating' aspect of the site frequently and offers a range of functionality (explained below) to facilitate this
* Users looking to express their personal information to other users
    * Users are able to create profiles, not only displaying a range of preselected personal criteria but also a custom bio
* Users who are looking to send 'flirtatious' notifications to users but not specifically have conversations
    * The site makes use of a 'winks' feature which allows users to engage with other individuals without having to send text messages
* Users who are looking to have conversations with other users
    * The site makes use of a messaging functionality which allows users to send text messages to one another. This requires a premium subscription (explained below)
* Users looking to search through many members quickly - most likely to find a potential relationship partner
    * The site makes use of a 'quick match' feature, which allows users to view many profiles quickly, swiping to indicate an intent to engage with the user or not
* Users looking to search through many members quickly based on a range of criteria
    * All preselected profile aspects can be used in search filters, helping users to find members based on a range of criteria - most likely to match ideal romantic traits
* Users looking to search through members based on their sexuality preferences
    * In order to not display unwanted romantic interests to users, all members shown to a user match their gender preferences (and the same for the displayed user). A homosexual male user won't be shown to a female user. A heterosexual female user won't see a female user.
* Users who wish to see which profiles have viewed them
    * Views are tracked allowing users to see which members have viewed them - a desired interaction for a dating site user
* Users who wish to see which profiles have 'winked' at them - indicating a subtle romantic interest intent
    * 'Winks' are tracked allowing users to see which members have 'winked' at them - a desired interaction for a dating site user
* Users who wish to see which profiles have 'messaged' them
    * 'Messages' are tracked allowing users to see which members have 'messaged' them - a desired interaction for a dating site user
* Users who want to find members 'serious' about dating
    * The subscriptions required to engage with users (excluding winks) helps to filter out users not 'serious' about dating online 

Wireframes can be found [here](https://github.com/mdenoronha/dating-app/tree/master/media/wireframes)

The following alterations were made after the mock-up phase:
* 1 profile shown per line on mobile. 4 profiles shown per line on desktop
* Change of icons used on menu
* Change of footer shape for mobile


Features
---------------
### Existing Features ###
*Creating a User*
* Users are able to enter their username, email and password to create an account
* Usernames are unique, stopping users from creating accounts with the same details
* Using Django's authentication system, user's remain logged after leaving the site

*Creating a profile*
* On creating an account, a profile is created for each user. They are directed to a profile edit page on registering
* Users are able to a custom bio to their profile
* Users are able to select options on a number of predefined attributes for their profile
* Users are able to select the location they reside, assisted from Google Maps API
* Users are able to add a number of profile photos to their profile
* On submitting, users are informed they have been sent to the verification team

*Verification*
* Users are marked as 'to be approved' on profile creation/update. This limits what content is displayed on their member profile
* Members of the verification team can approve or reject profiles using the above instructions
* Members of the verification team only have sufficient permissions to make verification changes
* Users are emailed with the status of their verification

*Home*
* The logged in homepage offers a snapshot of users to encourage interaction quickly. These include most active, most recent and closest profiles (using the location information submitted on profile creation)
* The quick swipe feature allows users to swipe in a specific direction to either engage with (wink) or reject profiles
* Interaction icons (winks and messaging) are below each profile, allowing the user to quickly engage with users

*Subscribe*
* A subscribe paywall limits use of the view and messaging functionality. Users are able to use the subscribe page to select and subscribe to different payment plans

*Views*
* When viewing another profile, a view record is created (if no previous view records are unseen)
* Users can see a list of all members that have viewed them on the view page, with new view records being highlighted accordingly

*Winks*
* Users are able to create a wink record (as long as no previous wink records are unseen) by clicking the wink icon on a member's profile or profile card
* Users can see a list of all members that have winked at them on the wink page, with new wink records being highlighted accordingly

*Messages*
* Users are able to create a conversation record between themselves and another user, by sending a first message to them on the member's profile or profile card
* Messaging allows for custom text to be shown to another user
* The chat home displays all conversation a user currently has, with conversations with new messages (not sent by them) highlighted accordingly
* The specific conversation page displays all messages between themselves and another user, with new messages (not sent by them) highlighted accordingly
* A new message alert is displayed when a user recieves a message whilst in a conversation with that member
![Navigate to Profile](https://github.com/mdenoronha/dating-app/blob/master/media/instruction-images/new-message.png?raw=true)
* From a specific conversation, users are able to view or wink at the member they are in discussion with

*Members*
* Users are able to view other member profiles, displaying their profile images, bio and personal details (if they are verified)
* Sexuality checks (outlined above) limit users from visiting members outside of their (or the other member's) sexual preferences
* From the members page, users are able to wink or message that specific member
* When visiting their own profile, users are able to see how their profile will appear (with engagement features disabled)
* When visiting their own profile, users are provided a link to make changes to their profile. This takes users to the edit profile page seen after registering
* Users are able to make changes to their bio, personal details as well as delete or add profile photos from the edit profile page

*Search*
* The search page lists all personal features as search options. Users are able to select attributes such as hair length, sexuality, distance, etc. to filter profiles
* Similarly to viewing members, members with contradticting sexuality preferences won't be shown
* Users are able to reset their search criteria at any time using the Reset button

*Account*
* Users are able to view their account details (passwords are not displayed) from the account page
* Users are able to edit their account details from the account page
* After subscribing, payment cards are shown on the account page
* After subscribing, any currently live subscriptions are displayed on the account page. These are removed in the subscription is no longer active
* Users are able to cancel or reactivate a subscription from the account page, updating their Stripe records
* Users are able to logout by using the link on the account page
* Users are able to delete their account (and all engagement and profile records) by using the link on the account page

### Features Left to Implement ###
* The site makes use of a reject record for the quick swipe feature, this can be expanded to allow users to 'block' certain members
* The check for new messages is not realtime and is instead an AJAX request running periodically. Under larger use this would need replacing with a realtime solution
* Users are currently not able to delete engagmeent records, this can be implemented
* Only three sexuality prefrences and two gender options are currently available, this can be expanded to accomadate more users
* If a user's subscription has ended, the user is still premium until they try to complete a premium action - then they are downgraded. Ideally this would update on subscription end date.

Technologies Used
---------------
* Python was used extensively in the creation of the app
* The Django framework was used in creation of the app
* the django-filters package was used to faciliate the search functionality
* The Stripe platform and stripe.js is used to faciliate the subscription feature
* Heroku was used for public hosting the application
* Heroku Postgres was used as the SQL database management system
* AWS S3 was used for data storage of profile photos
* boto3 was used to faciliate the connection to the S3 bucket
* jQuery was used extensively to aid front end functionality
* Bootstrap was used extensively for front end styling
* Popper.js and bootstrap-select are used to support Bootstrap's dropdown feature
* datepicker.js is used for the edit profile date option
* jQuery-ui is used for the draggable and droppable elements on the quick swipe section and user's profile photos
* touch-punch.js is used to faciliate jQuery-ui on mobile
* Fontawesome is used for icons

Testing
---------------
Testing can be run using the command 'python3 manage.py test'
Travis has been used for testing updates

### Testing through Django's testing suite ###
Test  | Status
------------- | -------------
**Account** | 
Account page returns account.html and 200 response | Successful
Submitting user form changes user's email address | Successful
Submitting password form changes user's password | Successful
Selecting cancel cancels subscription and redirects to account | Successful
Selecting reactivate reactivates subscription and redirects to account | Successful
**Chat and User Interaction** |
Chat conversation page returns chat.html and 200 respons (when conditions are met) | Successful
Submitting a message creates a message record and redirect to chat | Successful
Chat home returns chat_home.html and 200 response (when no conversations are created) | Successful
Chat home returns chat_home.html and 200 response (with message received) | Successful
Chat home returns chat_home.html and 200 response (with message sent) | Successful
Winks chat returns winks.html and 200 response | Successful
Views chat returns views.html and 200 response (when conditions are met) | Successful
new_message_check AJAX returns object with conversation key | Successful
Wink page's AJAX request returns correct message if last wink has not been read | Successful
Wink page's AJAX request returns correct message if last wink has been read | Successful
Reject AJAX request creates a reject record | Successful
Chat AJAX request creates conversation and message record returns correct message (if conditions are met) (if no previous conversations exist) | Successful
Chat AJAX request creates message record returns correct message (if conditions are met) (if a previous conversations exist) | Successful
read_messages AJAX request reads all messages in a conversation (for current user) and returns correct message | Successful
read_wink AJAX request returns 204 response | Successful
read_view AJAX request returns a redirect directive (if user is not premium) | Successful
read_view AJAX request returns 204 response (user is premium) | Successful
**Subscribe** |
Submit payment form creates subscription (no previous subscription) | Successful
Submit payment form creates subscription (previous subscription) | Successful
**Profiles** |
Login page returns login.html and 200 response (user not authenticated) | Successful
Login page redirects user to home (user authenticated) | Successful
Logout redirects user to preregister | Successful
Delete redirects user to preregister | Successful
Register page returns register.html and 200 response | Successful
Submit register form creates user | Successful
Create profile page returns create-profile.html and 200 response | Successful
Submit profile form creates profile record and redirects to verification page | Successful
Login page authenticates user (if details are correct) | Successful
Member page returns member.html and 200 response | Successful
Submit message form on member page redirects user to subscribe page (not premium) | Successful
Submit message form on member page redirects user to corresponding conversation page (premium) | Successful
Member page redirects to home if users' sexuality do not correlate | Successful
Logout page logs user out | Successful
Verification page returns verification-message.html and 200 response | Successful
**Search** |
Search page returns search.html and 200 response | Successful

### Manual Testing ###
Test  | Status
------------- | -------------
**Register** |
All fields are required | Successful
Username is limited to 12 characters | Successful
Password fields must match | Successful
Submitting register form with valid values creates user and profile record | Successful
**Create Profile** |
All fields (except profile photos) are required | Successful
Bio is limited to 200 characters | Successful
Dropdown options display a dropdown as intended | Successful
Location options provides Google Maps API autocomplete | Successful
Hidden long and lat fields are updated correctly in accordance with location option | Successful
Selecting date activates the datepicker | Successful
Selecting profile photo block allows user to upload a photo | Successful
Photo is displayed in input block | Successful
Selecting delete removes image from input block | Successful
Clicking submit creates a profile record with corresponding values | Successful
Clicking submit adds inputted images to S3 bucket | Successful
On returning to create profile to make edits, submitted edits change profile values | Successful
On returning to create profile to make edits, deleting a profile photo removes Profile Image record | Successful
**Home** | 
Profiles shown are within users' sexuality prefernces | Successful
Closest profiles displays profiles in distance order | Successful
Active recently displays profiles within most recent activity | Successful
Newcomers displays profiles in register order | Successful
On quick swipe, profiles are draggable and disappear when dropped | Successful
When dropped right, wink record is created | Successful
When dropped left, reject record is created | Successful
Clicking wink on profile creates a wink record | Successful
Clicking message on profile opens message modal | Successful
Submitting message when not premium redirects user to subscribe | Successful
Submitting message when premium creates message record | Successful
After reciving an engagement, if it is not read the menu option's styling is changed | Successful
Distance displayed reflects distance between profile's submitted long and lat (through Google Maps API) | Successful
**Verification** |
On all displays of a users profile image which isn't approved (exc their own profile), a placeholder alternative is shown | Successful
On members page profile bio and personal details are not shown until they are approved | Successful
On admin page, a user with correct permissions can select multiple profiles to approve | Successful
On admin page, a user with correct permissions can select multiple profiles to reject | Successful
On admin page, a user with correct permissions can select multiple profile image to approve | Successful
On admin page, a user with correct permissions can select multiple profile image to reject and delete | Successful
On profile approval, an email is sent to the user | Successful
On profile rejection, an email is sent to the user | Successful
On profile image approval, an email is sent to the user | Successful
On profile image rejection, an email is sent to the user | Successful
After updating a profile, the user's profile and profile images are set to 'to be approved' | Successful
**Member Profile** |
Member profile displays profile record data accordingly | Successful
Clicking wink on profile page creates a wink record | Successful
Submitting message when not premium redirects user to subscribe | Successful
Submitting message when premium creates message record | Successful
When viewing own profile, chat and wink are disabled | Successful
When viewing own profile, edit profile button is visible | Successful
**Winks** |
If no winks are received, winks page indicates as such | Successful
If winks are received, winks page displays all winks | Successful
Winks previously not seen are given different styling | Successful
If a wink has been sent to a user, another wink cannot be sent unless they have viewed the last wink | Successful
If a wink has not been read, the styling indicates as such | Successful
**Views** |
Viewing views page redirects user to subscribe (not premium) | Successful
If no views are received, views page indicates as such | Successful
If views are received, views page displays all views| Successful
If a view has been sent to a user, another view cannot be sent unless they have viewed the last view | Successful
If a view has not been read, the styling indicates as such | Successful
**Chat home** |
Viewing chat home page redirects user to subscribe (not premium) | Successful
Viewing chat home with no messages received indicates as such | Successful
Viewing chat home with messages received displays all conversations | Successful
All conversations with received unread messages have different styling | Successful
**Chat** |
Chat page lists all messages in corresponding conversation | Successful
Messages received and messages sent have different styling to distinguish them | Successful
Received messages that are unread have different styling | Successful
Submitting the message creates a message record and updates the conversation | Successful
Messages received whilst viewing the conversation page produce a 'Message received' alert | Successful
The options dropdown lists other engagement options on click | Successful
Selecting send wink creates a wink record to the corresponding user | Successful
**Account** | 
Account page displays user details | Successful
Selecting an edit button opens the corresponding edit account form | Successful
Submitting the edit email/username form edits the user's account | Successful
Submitting the edit email/username form edits the user's Stripe details (if they exist) | Successful
Submitting the edit email/username form fails to edit the user's account when incorrect password is provided | Successful
Submitting the edit password form edits the user's password | Successful
Submitting the edit password form fails to edit the user account when incorrect current password is provided | Successful
Edit profile links takes user to edit profile page | Successful
Logout logs user out of session | Successful
Delete deletes user account and all associated engagement (inc manytomany conversations record) | Successful
Subscription info displays all subscriptions currently active | Successful
All subscriptions past expiration date are not shown | Successful
Subscription info displays user's submitted credit card information | Successful
Selecting cancel cancels subscription in Stripe | Successful
Selecting reactivate reactivates subscription in Stripe | Successful
**Subscribe** |
Selecting a plan updates the total | Successful
Submitting incorrect payment information displays relevant message | Successful
Submitting payment form correctly creates order and subscription record | Successful
Submitting payment form correctly creates Stripe customer and subscription (no customer already) | Successful
Submitting payment form correctly creates Stripe subscription (customer already) | Successful
Accessing premium features while profile is premium but subscriptions are inactive downgrades the user | Successful
**Search** |
All search results are filtered to exclude contrasting sexuality preferences | Successful
Non-bisexual users do not see the gender option in search | Successful
Select a search option shows the corresponding dropdown | Successful
Selecting an option(s) on the dropdown updates the search option text | Successful
Selecting reset resets all options to default | Successful
Selecting search option filters in django-filters result based on selected option | Successful
Selecting multiple search options in django-filters form filters result based on selected options | Successful
Selecting sexuality option(s) filters result based on selected options | Successful
Selecting min height option filters result based on selected options | Successful
Selecting max height option filters result based on selected options | Successful
Selecting distance option filters result based on selected options | Successful

Deployment
---------------
Project has been deployed to Heroku and is accessible [here](https://dating-app-mvd.herokuapp.com/).
The process for deployment was as follows:
* Accessed the Heroku platform and clicked Create New App
* Add an app name, location and click Add App
* Create a new git repository using $ git init
* Add all files to git using $ git add <file-name>
* Commit all files to git using $ git commit -m <custom-message>
* In Github, create a new repository and follow instructions to push to created repository
* In Heroku, access Deploy panel
* Under Deployment Method select Github 
* If not done so already connect Github account to Heroku
* Select Github repository and click Connect
* Within the terminal created requirements.txt file with dependencies
* Create Procfile with the following text 'web: gunicorn dating_app.wsgi:application'
* In Heroku under Settings add the app's secret key
* Add, commit any changes and push files to Github

Credits
---------------

* Assistance from [here](https://stackoverflow.com/questions/27472663/how-to-use-djangos-assertjsonequal-to-verify-response-of-view-returning-jsonres) for setting JSON responses
* Assistance from Django docs on [pagination](https://docs.djangoproject.com/en/1.11/topics/pagination/)
* Assistance from [here](https://stackoverflow.com/questions/26029862/django-ajax-call-not-working-in-chrome-working-in-firefox?rq=1) with using CSRF token on AJAX request on Firefox
* Assistance from [here](https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable) on writing a custom template filter to accessing key and value in loops
* Assistance from [Strip docs](https://stripe.com/docs/api/customers/create) for Stripe functionality
* Assistance from [here](https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template) on outputting ages
* Assistance from [here](https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django) on creating unique file names
* Assistance from [here](https://stackoverflow.com/questions/19703975/django-sort-by-distance) on using long/lat distance formula and extending sqlite's query capabilities
* Assistance from [here](https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django) on using FormSet to upload multiple images
* Assistance from [here](https://getbootstrap.com/docs/4.0/components/modal/#varying-modal-content) on Bootstrap's modal
* Assistance from [here](https://stackoverflow.com/questions/8376525/get-value-of-a-string-after-a-slash-in-javascript) on accessing elements in URL
* Assistance from [here](https://stackoverflow.com/questions/210717/using-jquery-to-center-a-div-on-the-screen) on using jQuery to centre an element 
* Assistance form [here](https://ctrlq.org/code/19616-detect-touch-screen-javascript) on determining if a touch screen is being used
* Assistance from [here](https://stackoverflow.com/questions/5603745/jquery-draggable-revert-is-not-pixel-perfect) on addressing jQueryUI's draggable revery bug
* Profile and background images provided by [Unsplash](https://unsplash.com/)