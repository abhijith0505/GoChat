GoChat
===================


The terminal chat message application is here!.
Wanted to send messages without leaving your terminal window? This is your answer!

![](https://github.com/abhijith0505/GoChat/blob/master/screenshots/gochat.png)

----------


Installation
-------------

**GoChat** is a *universal* Linux application packaged using [Snappy](https://en.wikipedia.org/wiki/Snappy_%28package_manager%29).

### Install Snapd
- For Debian
	```
	sudo apt install snapd
	```
	 
 - For other distributions please refer [this](http://snapcraft.io/docs/core/install).

Install GoChat using
```
sudo snap install gochat
```

You are done!

Happy messaging!


----------


Usage
-------------------

![](https://github.com/abhijith0505/GoChat/blob/master/screenshots/gochathelp.png)

###Register
You need to register your user to message others. After all, they need to know who is messaging them :P
```
$ gochat --register
Username: tony_stark
Password:
User created!
```

> Note: Current version allows only one user per system

###Delete User
This delete your user, along with all messages. Delete wisely.
```
$ gochat --delete-user
Your computer is free from GoChat accounts now
```

###Version
To know the version of your app.

```
$ gochat --version
gochat 0.1.2
```

###Send Message
You need to know before hand the username of the person you want to message. 
(Yes, we are working on this to make it simpler)
```
$ gochat --send
Username: tony_stark
Message: How you doin'?
Message sent successfully!
```

###To read your unread messages
This shows all your unread messages from all users.

```
$ gochat --unread

```

###To read your messages

For all previous messages
```
$ gochat --messages
```

For all messages from a particular user
```
$ gochat --messages capn_america
```

---------

Issues and Improvements
=====
Please report issues and suggest improvements [here](https://github.com/abhijith0505/GoChat/issues).
