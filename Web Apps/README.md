# Backend Projects

CallTime is completed, however I will likely continue adding updates. The complete code is on a cloud server and you can view the results of the code in the link below.

# CallTime

CallTime is a web app created with the Django framework that allows for easily creating daily schedules for performing artists and stage managers.

The site is up and running on a cloud server. To test out the web app follow this link and start making schedules!
https://dylanelza.pythonanywhere.com/getdata/home/

Video Demo: https://youtu.be/Jsc_MZOkz2A

GitHub Repo: https://github.com/bluelegacy12/CallTime

Features:
- Two account types: Artist and Company
- Company accounts can create Shows, Roles, Call Blocks (Schedules), Conflicts for Artists, Staff members, Venues with addresses for rehearsal and performance locations
- Company accounts can upload Documents for Artists to view - files are stored in a secure google drive for space management
- API endpoints for all CRUD operations for each table
- Artist accounts can be linked to Company accounts in order to view relevant schedules
- **_Pdf can be automatically generated from schedule data, and emailed to all Artists and Staff emails linked to the Company account at the push of a button_**
- Company accounts can send mass emails to Artists and Staff linked to Company
- Company accounts can create Categories to assign to Artist roles for quick selection later when making schedules and scheduling Artists
- Artist profile allows for basic user setting changes like email and phone number privacy
- Artist profile shows user-specific schedule information and an option to view the full schedule
- **_When creating a schedule, if a date is selected that is the same day as an Artist Conflict, a modal will immediately display, showing all Artists with a schedule conflict on that day_**
- QR code for mobile app


# TranspoCentral

This is a social platform intended to provide a space to share resources and job opportunities, communicate, and filter information for truck drivers and relevant clients.
This idea was proposed by a specialist in the field who saw a need for a "facebook-like" platform for truck drivers to find valuable resources and information.
The project is incomplete and currently has only a few features:
- Posting text, videos, and images
- Filter posts by most trending hashtags
- Filter posts by searched hashtags
- A Profile page that shows only the user's posts
- A page that filters video posts

Other smaller features can be found on the web app as well


# Sweet Abundance

This is a web app designed to be a platform for a specific business to sell their product. In this case the client is selling cookies.
The app is close to completion but has key features missing such as charging credit/debit cards.
Feaures so far:
-A Neat and professional homepage
-A shop page that lists products pulled from the backend
-An admin page to add or edit products
-A detailed page of each product and their reviews, showing stars for each personal review and 
javascript to average the review score and show an appropriate star count
-A signed-in user can leave a review
-A unique referral code is randomly generated on account creation and shown in profile page
-If user created an account with a referral code, the user assigned to that referral code is shown on their profile paged as "Referred By:"
-When a referral code is used in account creation, both parties gain 50 reward points and their point total displayed in their profile page
