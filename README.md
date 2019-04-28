## ikabot ~ Ikariam Bot

_Ikabot is a program written in python that grants the iqual and even more functionality than a premium account in ikariam, without spending ambrosia!_

### Features

0. Exit

	Closes the main menu, returning to the normal console. You can also use `ctrl-c`. When closing _ikabot_, all the actions that you configured will continue running in the background. You can list them with `ps aux | grep ikabot`.

1. Construction list

	The user selects a building, the number of levels to upload, _ikabot_ calculates if it has enough resources and uploads the selected number of levels.
	
2. Send resources
 
	It sends unlimited amount of resources from one city to another. It doesn't matter how many boats you have, _ikabot_ will send all the trips that were necessary. The destination city can be own by the user or by other.

3. Send wine

	It sends wine from cities in wine, to cities that are not in wine. The maximum amount to send is equal to the total amount of wine that is stored in cities in wine, divided by the number of cities that are not in wine.

4. Account status

	It shows information such as levels of the buildings, time until the wine runs out, resources among other things from all the cities.
	
5. Donate

	It allows one to donate.
	
6. Search for new spaces

	This functionality alerts by telegram, if a city disappears or if someone founded in any of the islands where the user has at least one city founded.
	
7. Login daily

	For those who do not want to spend a day without their account login.
	
8. Alert attacks

	It alerts by telegram if you are going to be attacked.

9. Donate automatically

	It enters once a day and donate all available wood from all cities to the luxury good or the forest.

10. Alert wine running out

	It warns by Telegram when less than N hours are needed for a city to run out of wine. The number of hours is specified by the user.

11. Buy resources

	It allows you to choose what type of resource to buy and what quantity. It automatically purchases the different offers from the cheapest to the most expensive.

12. Update Ikabot

	It updates _ikabot_
	

When you set an action in _ikabot_, you can enter and play ikariam without any problems. The only drawback that you may have is that the session expires, this is normal and if it happens simply re-enter.

### Install

```
sudo python3 -m pip install ikabot
```
with the `ikabot` command you access the main menu.

### Uninstall

```
sudo python3 -m pip uninstall ikabot
```
### Dependencies

In order to install and use _ikabot_, python3 and pip must be installed. It must be run on **Linux**, it does not work on **Windows**.

#### - Python 3
It is probably installed by default in your system.

To check if it is installed by default, just run `python3 --version`.

If it is not installed, visit the [official website](https://www.python.org/) 

#### - Pip
It is a tool to install python packages.

To check if it is installed by default, just run `python3 -m pip -V`.

To install it, you must download the _get-pip.py_ file from [this page](https://pip.pypa.io/en/stable/installing/) and run `python3 get-pip.py`.

Or just excecute:
```
curl https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
```

### Telegram

Some features (such as alerting attacks) communicate with you via Telegram messages.

This messages are visible to you and nobody else.

Setting this up is highly recommended, since it allows one to enjoy all the functionality of _ikabot_.

Para configurarlo necesitaremos simplemente ingresar dos datos:
To configure this, you simply need to enter two pieces of information:

1) The token of the bot you are going to use

	If you want to use the 'official' bot of _ikabot_, enter Telegram and search with the magnifying glass @DaHackerBot, talk to it and you will see that a /start is sent. Once this is done you can close Telegram.
	
	Then, when _ikabot_ asks you to enter the bot's token, use the following: `409993506: AAFwjxfazzx6ZqYusbmDJiARBTl_Zyb_Ue4`.
	
	If you want to use your own bot, you can create it with the following instructions: https://core.telegram.org/bots.

2) Your chat_id

	This identifier is unique to each Telegram user and you can get it by talking by telegram to @get_id_bot (the one with the bow in the photo).

When you want to use a functionality that requires Telegram, such as _Alert attacks_, _ikabot_ will ask you for the bot's token and your chat_id. Once entered, they will be saved in a file and will not be asked again.


### Advanced

If there is a ikabot process that we identified with `ps aux | grep ikabot`, we can get a description of what it does with `kill -SIGUSR1 <pid>`. The description will arrive via Telegram.

### Windows

_Ikabot_ does not work in Windows, although in the future it might work in the Ubuntu bash of Windows 10.
