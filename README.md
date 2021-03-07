# Friendify

## About US

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

After cloning the project or downloading it you just have to run this command 
```shell
$ Python3 main.py
```

⚠️ Before running the app, you should full screen your console. And this app does not run on pycharm's console so you have to use your systems console. 

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

- if you click on "See friend recommendations" you will get redirected to a screen where you can see the top recommendation for you. You can select anyone of them to see their profiles and add them as your friends.

- The "change your preferences" option is for changing the answers to the questions you were asked while registrations. These are used to give you your friend recommendations.

- If you want to Un friend people, you can go the "Edit profile" option, where you can select multiple people at once, who you want to unfriend. 

- To view your profile you have to go to the "your profile" option which has all the information about you, including your preferences and friend list.

- finally, you can logout to register sign in screen by selecting "Logout"


Further Documentation Coming Soon ...
