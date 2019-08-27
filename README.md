# Friendsbook - A Social Networkng App
Created using <b>Django Web Framework</b><br/>
We are living in the age of Social Networking like Facebook, LinkedIn, Google + etc. The objective is to develop a social networking application, which has the following basic features:

# Operations:

1. User can register into the application with their name, email id and password.
2. Registered user can login into the application.
3. There are options to get the basic information like date of birth, address, phone no, education, upload his/her picture, professional information, hobby etc.
4. After login, user can see their profile information.
5. User can add new friends by sending friend requests.
6. User can also make friends by accepting friend requests.
7. Users can see the basic profile information of their friends.
8. User can send messages to their friends

# Front End View:

1. Signup Page : This page helps a new user to register into the app by providing their details. It contains fields for Name, DOB, Gender, EmailID, Phone Number and Password.
2. Login Page : This page helps a registered user to login into their account by providing their credentials. It contains fields for EmailID and Password.
3. Home Page : This page is the viewing page for the user. Here user can see all his friends, pending friend requests, status of sent friend requests, search people registered in the app by their details, view messages sent to him and can send messages.
4. Profile Page : This page shows the user the details of people searched by him. It also contains option for sending friend request to that person in case he is not a friend with him.

# Database and Tables:

1. User : It contains details of all the users.
2. Friends : It contains list of all the friends. It will be a symmetric table.
3. Friend_Request : It contains all those friend requests which are not yet accepted. Once accepted, the entry will be deleted from this table and a corresponding entry will be made in the 'Friends' Table.
4. Message : It contains all the messages exchanged among the users.
