# About Us

The onset of COVID-19 has made it extremely hard for people to socialize and make
new friends.

To address this issue of adverse mental health conditions due to decreased social interaction
and to provide a solution in the form of an online platform where people can
find and connect with each other - We have designed a program which would allow
people connect with each other so as to find and make friends based on their
shared interests and compatibility.

# Running The App 📱
Clone the project:
```shell
$ git clone https://github.com/eeshannarula29/Friendify.git
```
Install the required libraries:
```shell
$ pip3 install firebase-admin
$ pip3 install PyInquirer
$ pip3 install cutie
$ pip3 install dash
$ pip3 install dash-cytoscape 
$ pip3 install pyfiglet
```
After cloning the project or downloading it you just have to run this command in the cloned or downloaded directory, in your computer command-line interpreter (cmd/terminal)
```shell
$ python3 main.py
```

⚠️ Before running the app, you should full screen your console.

If you want to run this app on Pycharm then follow these steps:

1) download all the requirements

2) open your project in Pycharm

3) Click on terminal, below the navigation bar on the left side of the screen

4) type ``` $ python3 main.py ``` in the terminal

# Usage


## Welcome Screen 🙏

![alt text](https://github.com/eeshannarula29/assets/blob/main/home.png?raw=true)

On the Welcome Screen the user will get 3 options, About us which does what it's name says, Sign in or register which again does what its name says and Exit ends the app.

## Click Sign In / Register 📄

If you select this option you will see something like this

![alt text](https://github.com/eeshannarula29/assets/blob/main/sign_in_register.png?raw=true)

From here you can go onto signing in or registering. If you press exit you will get to the previous screen.

## Register 

If you go to registration, you would be asked for a new username. After your username you would have to answer some questions about your interests, which would be used to match you up with your new friends 👯‍. This is how it looks (its a gif, if it does not start click on it)

![alt text](https://github.com/eeshannarula29/assets/blob/main/register.gif?raw=true)

If you do something wrong don't worry you can change your answers afterwards 😀. After the registration the home screen will open (coming below ⬇️).

## Sign In

For signing in you would just have to fill in your username with which you registered and your password, and your home screen will open 🚪.

## Home Screen 🏡

Finally, you have entered you home screen. Now you can make new friends 🎉 Yeye !

![alt text](https://github.com/eeshannarula29/assets/blob/main/signedin100.png?raw=true)
### See friend recommendations
if you click on "See friend recommendations" you will get redirected to a screen where you can see the top recommendation for you. You can select anyone of them to see their profiles and add them as your friends.
![alt text](https://github.com/eeshannarula29/assets/blob/main/recc100.png?raw=true)

The recommendations are from the highest to the lowest matching score with you. You can now select anyone of them to see their profile. Let us select the user with the username "nothanks". This is what will pop up 

![alt text](https://github.com/eeshannarula29/assets/blob/main/user_profile_rec.png?raw=true)

From here you can add them as your friend, or not if you don't want to and go back to see other people who were recommended to you.

### View your network
You can view your network by clicking on the option "View your network". Your network shows you who you are friends with who they are friends with, to make a network graph. When you select this option the following screen will pop up

![alt text](https://github.com/eeshannarula29/assets/blob/main/graph_depth.png?raw=true)

After selecting one of the options, your browser will open

![alt text](https://github.com/eeshannarula29/assets/blob/main/graph_2.gif?raw=true)

To close the graph, just go back to your app which would look like this

![alt text](https://github.com/eeshannarula29/assets/blob/main/graph_init_2.png?raw=true)

And press CTRL + c / control + c to end the graph.

### change your preferences
The "change your preferences" option is for changing the answers to the questions you were asked while registrations. These are used to give you your friend recommendations.


### My Friends
You can see your friends list by going to "My Friends". You can select on each one of your friends, to see their profile and unfriend them if you want. 

![alt text](https://github.com/eeshannarula29/assets/blob/main/myfriends.png?raw=true)

### Search for people

You can search for people by their username, using the ""Search for people" option. 

![alt text](https://github.com/eeshannarula29/assets/blob/main/search100.gif?raw=true)

### View profile
To view your profile you have to go to the "your profile" option which has all the information about you, including your preferences and friend list.

![alt text](https://github.com/eeshannarula29/assets/blob/main/profile.png?raw=true)
### Delete account
"Delete account" option deletes your account, need not worry, its asks for conformation. 

![alt text](https://github.com/eeshannarula29/assets/blob/main/delete_account.gif?raw=true)

### Logout
finally, you can logout to register sign in screen by selecting "Logout"



# Working of the App ⚙️

![alt text](https://github.com/eeshannarula29/assets/blob/main/working.jpeg?raw=true)

Our app has four components, the IO and visualization libraries, Screen, Data handler and firebase database. 
All of them work in sync, to make the app work. 

## Data Flow
 - For getting data, signing in and registering, the Screen first sends a request to the IO libraries to return the information of the data which needs to be loaded from the Firebase database. </br>


- Then the libraries return the data to be retrieved, which the Screen requests the Data handler to retrieve. </br>


- The Data handler then sends a request to the firebase and in turn firebase returns the data to the Data handler. </br>


- The data handler then sends this data to our Screen which take an action accordingly.

## Recommendation System

- To recommend friends to a user, we look for people with the same preference ad the user in our app.


- To look for similar people, we first gather all the data our app has, and generate a graph.


- This graph, has the users and the preferences as the vertices. 


- A user to user edge in this graph represents that both the users are friends


- A user to preference edge indicates that the user has that preference.


- We then use this graph to get people with similar preferences as the user. 


- More similar the preference, more is the similarity score between people. 


- We use this similarity score to calculate the order of the recommendations and percentage match. 

### Initial Data

Initially, the app had no users, so if people signed in they would not have been able to find any friends. Thus we conducted a survey in which we asked people about their preferences. Then we registered all of these users to our app.

The dataset is available in the data directory. We have scrapped the host address of the emails that the users have provided us, to maintain privacy.

## Network Visualization

Similar to recommending graphs, first we create a graph of all the users in the app, connected to each other and their preferences.

- We run this graph through a function to get a graph of a user for a certain depth. 


- This user graph is then formatted, as an input to the graphing library


- This graphing library then is given this data, and asked to visualize the data as graph in the browser. 
# Libraries 📚

- [Firebase](https://firebase.google.com/docs/reference/admin/python/firebase_admin)
  
- [PyInquirer](https://github.com/CITGuru/PyInquirer)

- [Cutie](https://pypi.org/project/cutie/)

- [Pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/)

- [Plotly](https://plotly.com/python/network-graphs/)

# Bugs to Fix 🐞

- [x] People who are already friends, should not be shown as recommendations
- [x] Better way to recommend friends

# Todo and Ideas 💡

- [x] Add a "add friends" feature which lets you type users Id to add them as friend.
- [x] customize graph layouts
- [ ] add authentication with password
- [ ] Friendify network, contaning all the users
- [ ] private and public accounts
- [ ] only friends can see their friends' friends or the whole profile
- [ ] friend requests instead of directly adding friends
- [ ] inbuilt chat system
