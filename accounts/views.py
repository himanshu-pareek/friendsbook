from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from accounts.models import UserProfile, Friends, Message
import datetime
from django.db import connection

# Create your views here.
def home (request):
    return render (request, 'accounts/home.html')

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')

        else:
            #request.method ='GET'
            form =RegistrationForm(request.GET)
            args = {'form': form}
            args['dub']=1
            return render(request, 'accounts/reg_form.html', {'args': args})
    else:
        form =RegistrationForm()
        args = {'form': form}
        args['dub']=0
        for field in form:
            print ('-------------------')
            print (field.id_for_label)
        return render(request, 'accounts/reg_form.html', {'args': args})

# def register(request):
#     if request.method =='POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/accounts/login')
#
#     else:
#         form =RegistrationForm()
#
#         args = {'form': form}
#         return render(request, 'accounts/reg_form.html', args)

def view_profile (request):

    args = {
        'user': request.user
    }
    print ('user_id', request.user.id)
    if (request.user.id == None):
        return redirect ('/')
    request.session['user_id'] = request.user.id

    user_1_id = request.session['user_id']

    user_profile = {}

    try:
        print ("Starting try")
        p = UserProfile.objects.raw ('SELECT id, description, city, website, phone FROM accounts_userprofile WHERE user_id = %s LIMIT 1', str (user_1_id))[0]
        print ("P: ", p)
        user_profile['description'] = p.description
        user_profile['city'] = p.city
        user_profile['website'] = p.website
        user_profile['phone'] = p.phone
        print ("Inside ttry: ", user_profile)
    except:
        print ("Inside exception: ", user_profile)
        user_profile = {}

    friend_requests = []
    for fr in User.objects.raw ('SELECT u.id, u.first_name, u.last_name, u.username, u.email FROM auth_user u, accounts_friends f WHERE f.user2 = %s AND f.friendship = 1 AND u.id = f.user1', str (user_1_id)):
        friend_requests.append ({
            'user1_id': fr.id,
            'user2_id': user_1_id,
            'username': fr.username,
            'first_name': fr.first_name,
            'last_name': fr.last_name,
            'email': fr.email
        })

    pending_friend_requests = []
    for fr in User.objects.raw ('SELECT u.id, u.first_name, u.last_name, u.username, u.email FROM auth_user u, accounts_friends f WHERE f.user1 = %s AND f.friendship = 1 AND u.id = f.user2', str (user_1_id)):
        pending_friend_requests.append ({
            'user1_id': user_1_id,
            'user2_id': fr.id,
            'username': fr.username,
            'first_name': fr.first_name,
            'last_name': fr.last_name,
            'email': fr.email
        })

    notifications = {}
    notifications['friend_requests'] = friend_requests
    notifications['pending_friend_requests'] = pending_friend_requests

    args['notifications'] = notifications
    args['user_profile'] = user_profile

    print ("ARGS: ", args)

    return render (request, 'accounts/profile.html', {'args': args})

def edit_profile (request):
    my_profile = UserProfile.objects.get(user_id = request.user.id)
    if request.method == 'POST':
        form = EditProfileForm (request.POST, instance = my_profile)

        print ('Form from post: ', form)

        if form.is_valid ():
            form.save ()
            return redirect ('/accounts/profile')

        else:
            print("i am in else")
    else:
        form = EditProfileForm (instance = my_profile)
        args = {
            'form': form
        }
        return render (request, 'accounts/edit_profile.html', args)

# def change_password (request):
#     if request.method == 'POST':
#         form = PasswordChangeForm (request.POST, instance = request.user)
#
#         if form.is_valid ():
#             form.save ()
#             return redirect ('/accounts/profile')
#
#     else:
#         form = PasswordChangeForm ()

def search_results (request):
    # print ("Request", request)
    args = {
        'keyword': request.GET['keyword']
        # 'users': []
    }
    print ("keyword", args['keyword'])
    if (args['keyword'].split () == ''):
        return render ()
    names = args['keyword'].split (' ')
    print ('length of names', len(names))
    if len (names[0]) == 0:
        return redirect ('/accounts/profile')
    users = []
    user_1_id = request.session ['user_id']
    for p in User.objects.raw ('SELECT * FROM auth_user WHERE first_name = "' + str(names[0]) + '" AND id != ' + str (user_1_id)):
        users.append ({
            'id': p.id,
            'username': p.username,
            'first_name': p.first_name,
            'last_name': p.last_name,
            'email': p.email
        })
        #print (p.username, p.first_name, p.last_name)
    args['users'] = users
    for p in args['users']:
        print (p['id'], p['username'], p['first_name'], p['last_name'], p['email'])
    return render (request, 'accounts/search_results.html', {'args': args})

def public_profile (request):
    # print ("Request", request)
    args = {
        'id': request.GET['id']
        # 'first_name': request.GET['first_name']
        # 'last_name': request.GET['last_name']
        # ''
        # 'users': []
    }
    # print ("keyword", args['keyword'])
    # users = []
    user = {}
    user_1_id = request.session['user_id']
    p = User.objects.raw ('SELECT a.first_name, a.last_name, a.email, a.id, a.username FROM auth_user a WHERE a.id = ' + str (args['id']) + ' LIMIT 1')[0]
    user = {
        'id': p.id,
        'username': p.username,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'email': p.email
    }

    p = UserProfile.objects.raw ('SELECT id, description, city, website, phone FROM accounts_userprofile WHERE user_id = ' + str (args['id']) + ' LIMIT 1')[0]
    user['description'] = p.description
    user['city'] = p.city
    user['website'] = p.website
    user['phone'] = p.phone


    friendship_flag = 0

    try:
        q = Friends.objects.raw ('SELECT id, user1, user2, since, friendship FROM accounts_friends WHERE (user1 = ' + str (user_1_id) + ' AND user2 = ' + str (user['id']) + ') OR ( user1 = ' + str (user['id']) + ' AND user2 = ' + str (user_1_id) + ' ) LIMIT 1')[0]
        if q.friendship == 0 or q.friendship == 3:
            friendship_flag = q.friendship
        elif q.user1 == user_1_id:
            friendship_flag = q.friendship
        else:
            friendship_flag = 3 - q.friendship
        user['since'] = q.since
    except:
        pass
    # print ("Q len = ", len(q))
    # print ("friedship:", friendship_flag)

    # print ('user1', request.session['user_id'])

        #print (p.username, p.first_name, p.last_name)
    # args['users'] = users
    # for p in args['users']:
    #     print (p['id'], p['username'], p['first_name'], p['last_name'], p['email'])
    # print ('Id', args['id'])

    print ('user_1_id: ', user_1_id)
    print ('user_2_id: ', args['id'])
    user['is_friend'] = friendship_flag
    print ('User: ', user)
    return render (request, 'accounts/public_profile.html', {'user': user})


def add_friend (request):
    friend_id = request.GET['id']
    user_1_id = request.session['user_id']

    r = Friends(user1=user_1_id, user2 = friend_id, friendship = 1)
    r.save()

    # r = Friends.objects.raw('INSERT INTO accounts_friends VALUES (null, ' + str(user_1_id) + ', ' + str(friend_id) + ', ' + '"2018-05-02", 1)' )
    # print("r = ",r)

    user = {}
    p = User.objects.raw ('SELECT a.first_name, a.last_name, a.email, a.id, a.username FROM auth_user a WHERE id = ' + str (friend_id) + ' LIMIT 1')[0]
    user = {
        'id': p.id,
        'username': p.username,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'email': p.email
    }

    p = UserProfile.objects.raw ('SELECT id, description, city, website, phone FROM accounts_userprofile WHERE user_id = ' + str (friend_id) + ' LIMIT 1')[0]
    user['description'] = p.description
    user['city'] = p.city
    user['website'] = p.website
    user['phone'] = p.phone


    friendship_flag = 0

    try:
        q = Friends.objects.raw ('SELECT id, user1, user2, since, friendship FROM accounts_friends WHERE (user1 = ' + str (user_1_id) + ' AND user2 = ' + str (user['id']) + ') OR ( user1 = ' + str (user['id']) + ' AND user2 = ' + str (user_1_id) + ' ) LIMIT 1')[0]

        if q.friendship == 0 or q.friendship == 3:
            friendship_flag = q.friendship
        elif q.user1 == user_1_id:
            friendship_flag = q.friendship
        else:
            friendship_flag = 3 - q.friendship
        user['since'] = q.since
    except:
        pass
    # print ("Q len = ", len(q))
    # print ("friedship:", friendship_flag)

    # print ('user1', request.session['user_id'])

        #print (p.username, p.first_name, p.last_name)
    # args['users'] = users
    # for p in args['users']:
    #     print (p['id'], p['username'], p['first_name'], p['last_name'], p['email'])
    # print ('Id', args['id'])

    user['is_friend'] = friendship_flag
    print ('User: ', user)
    return render (request, 'accounts/public_profile.html', {'user': user})

def confirm_request (request):
    friend_id = request.GET['id']
    user_1_id = request.session['user_id']

    print("dat = ",datetime.date.today())

    with connection.cursor () as cursor:
        cursor.execute ("UPDATE accounts_friends SET friendship = 3, since = %s WHERE user1 = %s AND user2 = %s", [datetime.date.today(), friend_id, user_1_id])
        row = cursor.fetchone ()
        print ("Row: ", row)

    # r = Friends(user1=user_1_id, user2 = friend_id, friendship = 1)
    # r.save()

    # r = Friends.objects.raw('INSERT INTO accounts_friends VALUES (null, ' + str(user_1_id) + ', ' + str(friend_id) + ', ' + '"2018-05-02", 1)' )
    # print("r = ",r)

    user = {}
    p = User.objects.raw ('SELECT a.first_name, a.last_name, a.email, a.id, a.username FROM auth_user a WHERE id = ' + str (friend_id) + ' LIMIT 1')[0]
    user = {
        'id': p.id,
        'username': p.username,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'email': p.email
    }

    p = UserProfile.objects.raw ('SELECT id, description, city, website, phone FROM accounts_userprofile WHERE user_id = ' + str (friend_id) + ' LIMIT 1')[0]
    user['description'] = p.description
    user['city'] = p.city
    user['website'] = p.website
    user['phone'] = p.phone


    friendship_flag = 0

    try:
        q = Friends.objects.raw ('SELECT id, user1, user2, since, friendship FROM accounts_friends WHERE (user1 = ' + str (user_1_id) + ' AND user2 = ' + str (user['id']) + ') OR ( user1 = ' + str (user['id']) + ' AND user2 = ' + str (user_1_id) + ' ) LIMIT 1')[0]

        if q.friendship == 0 or q.friendship == 3:
            friendship_flag = q.friendship
        elif q.user1 == user_1_id:
            friendship_flag = q.friendship
        else:
            friendship_flag = 3 - q.friendship
        user['since'] = q.since
    except:
        pass
    # print ("Q len = ", len(q))
    # print ("friedship:", friendship_flag)

    # print ('user1', request.session['user_id'])

        #print (p.username, p.first_name, p.last_name)
    # args['users'] = users
    # for p in args['users']:
    #     print (p['id'], p['username'], p['first_name'], p['last_name'], p['email'])
    # print ('Id', args['id'])

    user['is_friend'] = friendship_flag
    print ('User: ', user)
    return render (request, 'accounts/public_profile.html', {'user': user})


def chat (request):
    print("user : ",request.user)
    if (request.user.id == None):
        return redirect ('/')
    request.session['user_id'] = request.user.id

    user_1_id = request.session['user_id']
    friends = []
    for p in User.objects.raw ('SELECT u.id, u.first_name, u.last_name FROM auth_user u , accounts_friends f WHERE  (f.user1 =' + str(user_1_id) + ' AND f.user2 = u.id AND f.friendship = 3 ) OR  (f.user2 =' + str(user_1_id) + ' AND f.user1 = u.id AND f.friendship = 3 )'):

        friends.append({
            'id' : p.id,
            'first_name': p.first_name,
            'last_name': p.last_name,
        })

    for p in friends:
        print("friend :",p)

    return render (request, 'accounts/chat.html', {'friends': friends})

# def save_message (request):
#     print ("Request: ", request)
#     return render (request, 'accounts/send_chat.html', {'order': 10})


def chat_box(request):
    # print("top args : ", args)
    # if args == None:
    print("user : ",request.user)
    if (request.user.id == None):
        return redirect ('/')
    request.session['user_id'] = request.user.id

    user_1_id = request.session['user_id'] # My mine

    print ("Request-GET: ", request.GET)
    print ("Request-POST: ", request.POST)

    user_2_id = -1
    friend_name = "Anonymous"

    try:
        user_2_id = request.GET['id'] # Id of  friend chhating with
        friend_name = request.GET['friend_name']
        request.session['friend_id'] = user_2_id
        request.session['friend_name'] = friend_name
    except:
        user_2_id = request.session['friend_id'] # Id of  friend chhating with
        friend_name = request.session['friend_name']


    args = {
        'user_1_id': user_1_id,
        'user_2_id': user_2_id,
        'my_name': request.user.first_name,
        'friend_name': friend_name
    }

    messages =[]
    for p in Message.objects.raw('SELECT * FROM accounts_message WHERE ( sender = ' + str(user_1_id) + ' AND receiver = ' + str(user_2_id) + ') OR ( sender = ' + str(user_2_id) + ' AND receiver = ' + str(user_1_id) + ') ORDER BY send_time DESC LIMIT 10'):
        messages.append({
            'sender' : p.sender,
            'receiver' : p.receiver,
            'message' : p.message,
            'send_time' : p.send_time,
            'receive_time' : p.receive_time,
            'read_status' : p.read_status,
        })

    args['messages'] = reversed(messages)
    for p in messages :
        print("message : ",p)
        print("args : ", args)

    l = []
    for p in Message.objects.raw('SELECT id FROM accounts_message WHERE  sender = ' + str(user_2_id) + ' AND receiver = ' + str(user_1_id) + ' AND read_status = 0'):
        l.append(p.id)

    print ("l = ", l);

    for i  in l :
        message = Message.objects.get(id = i) # object to update
        message.receive_time = datetime.datetime.now ()
        message.read_status = 1 # update name
        message.save() # save objec


    return render (request, 'accounts/chat_box.html', {'args': args})

def save_message (request):
    print("user : ",request.user)
    if (request.user.id == None):
        return redirect ('/')
    request.session['user_id'] = request.user.id

    sender= request.user.id
    receiver = request.POST['receiver']
    message_text = request.POST['message-text']

    args = {
        'user_1_id': sender,
        'user_2_id':receiver,
        'my_name': request.user.first_name,
        'friend_name': request.POST['friend_name']
    }

    request.session['friend_id'] = receiver
    request.session['friend_name'] = args['friend_name']

    m = Message(sender=sender, receiver = receiver, message = message_text, send_time = datetime.datetime.now (), receive_time = None, read_status = 0)
    m.save()

    # request.method = 'GET'
    # request.GET['id'] = args['user_2_id']
    # request.GET['friend_name'] = args['friend_name']

    # messages =[]
    # for p in Message.objects.raw('SELECT * FROM accounts_message WHERE ( sender = ' + str(sender) + ' AND receiver = ' + str(receiver) + ') OR ( sender = ' + str(receiver) + ' AND receiver = ' + str(sender) + ') LIMIT 10'):
    #     messages.append({
    #         'sender' : p.sender,
    #         'receiver' : p.receiver,
    #         'message' : p.message,
    #         'send_time' : p.send_time,
    #         'receive_time' : p.receive_time,
    #         'read_status' : p.read_status,
    #     })
    #
    # args['messages'] = messages
    #
    # for p in messages :
    #     print("message : ",p)
    #
    # print("args : ", args)
    #
    # print ('Request: ', request)

    return redirect ('../../accounts/chat_box')
