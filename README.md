# ProTag
ProTag leverages Genius' API to provide users data visualizations of their 
favorite song, performer, album, or producer.

## Table of Contents
* [Overview](#overview)</br>
* [Tech Stack](#techstack)</br>
* [Setup/Installation](#installation)</br>
* [Demo](#demo)</br>
* [Future Development](#future)</br>

<a name="overview"/></a>
## Overview
ProTag was inspired by the need for production information of songs.  The major 
components of song production are:

* The recording of the performer delivering her lyrics.
* The making of the beat (song's instrumental, non-lyrical/non-vocal rhythmic 
backing track) by the producer.  A producer's beat is often identified by the 
producer's signature, aka tag.

<a name="techstack"/></a>
## Tech Stack
**Frontend:** JavaScript (AJAX, JSON, React), Jinja, jQuery, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>
**Libraries:** D3, Chart.js, Pandas, Scikit-learn<br/>
**API:** Genius<br/>

<a name="installation"/></a>
## Setup/Installation
On local machine, go to desired directory.  Clone protag repository:
```
$ git clone https://github.com/rbarner14/protag.git
```
Create a virtual environment in the directory:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database:
```
$ createdb music
```
Build database:
```
$ python3 -i model.py
>>> db.create_all()
```
Seed database:
```
$ python3 -i seed.py
```
Run app:
```
$ python3 server.py
```
Navigate to localhost:5000 in browser.

<a name="demo"/></a>
## Demo

**Enter a song, performer, album, or producer.  Select desired result.**
<br/><br/>
![Homepage](/static/images/readme/homepage.gif)
<br/>

**If song selected, view song's title, album, performer, Apple Music player, and producers.**
<br/><br/>
![Song](/static/images/readme/song.gif)
<br/>

**If producer selected, view producer's name, image, bio, and data visualizations.  Related producers are provided, generated with a k-means 
machine learning algorithm; nearest neighbors determined by like performers).**
<br/><br/>
![Producer_Landing](/static/images/readme/producer_landing.gif)
<br/>

**If producer has been making songs for at least 10 years, a ProTag Verified Industry Vet tag will accompany their name.**
<br/> <br/>
![Producer_Sidenav](/static/images/readme/producer_sidenav.png)
<br/>

**Chart.js donut graph shows songs producer made by performer.**
<br/><br/>
![Producer_Donut](/static/images/readme/producer_donut.gif)
<br/>

**Chart.js line graph shows songs producer made over his career tenure.**
<br/><br/>
![Producer_Line](/static/images/readme/producer_line.gif)
<br/>

**Similar views are provided for performers, except the frequency at which they work with producers is visualized.**
<br/>

**If album is selected, view album's title, cover art, performer, D3 data visualizations (bubble and web) of songs on album by producer.**
<br/><br/>
![Album](/static/images/readme/album.gif)
<br/>

**Each node represents a producer.  Weights are assigned according to the number of songs that producer has made on that album.**
<br/><br/>
![Album_Bubbles](/static/images/readme/album_bubbles.png)
<br/>

**D3 force directed graph of album's producers.**
<br/><br/>
![Album_Web](/static/images/readme/album_web.gif)
<br/>

**Electric charge on particles is simulated to visualize the 
network of performers and producers.**
<br/><br/>
![Network](/static/images/readme/network.gif)
<br/>

**Thanks for exploring!**

<a name="future"/></a>
## Future Development
* Enable user profile creation for favorites saving.
* Implement algorithm to suggest music to user leveraging their favorites.


