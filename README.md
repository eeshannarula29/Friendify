# Friendify

## About Us

Friendify is an app used to make friends in these hard times when
it is so difficult to do so. Friendify takes into note the interests
of the user, and find people with the common interests.

The app uses firebase to store all the data of the users. The data is
used to make decision trees, to get people who have the common interests
as the user.

The app takes into consideration the movies, food, music and games the
user likes and create trees accordingly with the leaf nodes being all
the users of the app.

User can then add friends, according to the recommendations, and edit them
afterwards. They can visualize their friends and their friends' friends
using a graph, where the user and the friends are the vertices and their
friendship is a edge between them.

We are using PyInquirer and cutie to get inputs from the terminal, which is
used to navigate through the app.

## Running The App 📱
Cloning the project:
```shell
$ git clone https://github.com/eeshannarula29/Friendify.git
```
After cloning the project or downloading it you just have to run this command in the cloned or downloaded directory, in your computer command-line interpreter (cmd/terminal)
```shell
$ Python3 main.py
```

⚠️ Before running the app, you should full screen your console, and this app does not run on Pycharm's console so you have to use your system's command-line interpreter. 

## Usage


### Welcome Screen 🙏

![alt text](https://github.com/eeshannarula29/assets/blob/main/home.png?raw=true)

On the Welcome Screen the user will get 3 options, About us which does what it's name says, Sign in or register which again does what its name says and Exit ends the app.

### Click Sign In / Register 📄

If you select this option you will see something like this

![alt text](https://github.com/eeshannarula29/assets/blob/main/sign_in_register.png?raw=true)

From here you can go onto signing in or registering. If you press exit you will get to the previous screen.

### Register 

If you go to registration, you would be asked for a new username. After your username you would have to answer some questions about your interests, which would be used to match you up with your new friends 👯‍. This is how it looks (its a gif, if it does not start click on it)

![alt text](https://github.com/eeshannarula29/assets/blob/main/register.gif?raw=true)

If you do something wrong don't worry you can change your answers afterwards 😀. After the registration the home screen will open (coming below ⬇️).

### Sign up

For signing up you would just have to fill in your username with which you registered and your home screen will open 🚪.

### Home Screen 🏡

Finally, you have entered you home screen. Now you can make new friends 🎉 Yeye !

![alt text](https://github.com/eeshannarula29/assets/blob/main/signed_in.png?raw=true)
#### See friend recommendations
if you click on "See friend recommendations" you will get redirected to a screen where you can see the top recommendation for you. You can select anyone of them to see their profiles and add them as your friends.


#### View your network
...


#### change your preferences
The "change your preferences" option is for changing the answers to the questions you were asked while registrations. These are used to give you your friend recommendations.


#### Unfriend people
If you want to Un friend people, you can go the "Edit friends" option, where you can select multiple people at once, who you want to unfriend. 


#### View profile
To view your profile you have to go to the "your profile" option which has all the information about you, including your preferences and friend list.


#### Delete account
"Delete account" option deletes your account, need not worry, its asks for conformation. 


#### Logout
finally, you can logout to register sign in screen by selecting "Logout"



## Working of the App ⚙️

![alt text](https://github.com/eeshannarula29/assets/blob/main/working.jpeg?raw=true)

Our app has four components, the IO and visualization libraries, Screen, Data handler and firebase database. 
All of them work in sync, to make the app work. 

### Data Flow
 - For getting data, signing in and registering, the Screen first sends a request to the IO libraries to return the information of the data which needs to be loaded from the Firebase database. </br>


- Then the libraries return the data to be retrieved, which the Screen requests the Data handler to retrieve. </br>


- The Data handler then sends a request to the firebase and in turn firebase returns the data to the Data handler. </br>


- The data handler then sends this data to our Screen which take an action accordingly. 

### Friend Recommendations
![alt text](https://github.com/eeshannarula29/assets/blob/main/tree.jpeg?raw=true)

- Friend recommendations are given using modified decision trees. The internal nodes are the preferences the users choose, and the root nodes are the users. </br>


- As a user can choose at most 3 subcategories for all the 4 categories (movies, music, games and food), so the user can be a root value at most 3 to the power 4 times in the tree. 


- For recommendation of friends, first this tree is created with all the data we initially have for all the users of the app.


- This tree is then searched for with all the possible 81 (3 to the power 4) preference sequences of a user, and all the users at the end of those Sequence are stored in a collection.


- Then we count how frequently the users are appearing in this collection, and sort the accordingly. 


- The user is shown the top 10 users who have appeared most frequently, as friend recommendations. 

#### Initial Data

Initially, the app had no users, so if people signed in they would not have been able to find any friends. Thus we conducted a survey in which we asked people about their preferences. Then we registered all of these users to our app.


The dataset is available in the data directory. We have scrapped the host address of the emails that the users have provided us, to maintain privacy.


### Network Visualization
...

## Documentation of libraries used 📚

- [Firebase](https://firebase.google.com/docs/reference/admin/python/firebase_admin) 

- [PyInquirer](https://github.com/CITGuru/PyInquirer)

- [Cutie](https://pypi.org/project/cutie/)

- [Pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/)

- [Plotly](https://plotly.com/python/network-graphs/)
