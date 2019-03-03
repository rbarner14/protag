# ProTag
ProTag leverages Genius' API to provide users data visualizations of their 
favorite rap songs.  

A user can search their favorite song, performer, album, or producer to return a 
data visualization for it.

## Table of Contents
* [Overview](#overview)</br>
* [Tech Stack](#techstack)</br>
* [Setup/Installation](#installation)</br>
* [Demo](#demo)</br>
* [Future Development](#future)</br>

<a name="overview"/></a>
## Overview
ProTag was inspired by the need for production information of songs.  The major 
components of hip hop song production are:

* The recording of the rapper (performer) delivering his lyrics.
* The making of the beat (song's instrumental, non-lyrical/non-vocal rhythmic 
backing track) by the producer.  A producer's beat is often identified by the 
producer's signature, aka tag.

<a name="techstack"/></a>
## Tech Stack
**Frontend:** Javascript, Jinja, jQuery, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>
**Libraries:** D3, Chart.js<br/>
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
Seed database:
```
$ python3 -i seed.py
```
Build database:
```
$ python3 model.py
```
Run app:
```
$ python3 server.py
```
Navigate to localhost:5000 in browser.

<a name="demo"/></a>
## Demo

**Enter a song, performer, album, or producer.**
<br/><br/>
![Homepage](/static/images/readme/homepage.gif)
<br/>

**Select desired result.**
<br/><br/>
![Select Search Result](/static/images/readme/search_result.gif)
<br/>

**If song selected, view song's title, album, performer, Apple Music player, and producers.**
<br/><br/>
![Song](/static/images/readme/song.gif)
<br/>

**If performer selected, view performer's name, image, bio, Chart.js donut data visualization of songs performer made by producer, albums and singles.**
<br/><br/>
![Performer](/static/images/readme/performer.gif)
<br/>

**If album selected, view album's title, cover art, performer, D3 data visualizations (bubble and web) of songs on album by producer.**
<br/><br/>
![Album](/static/images/readme/album.gif)
<br/>

**If producer selected, view producer's name, image, bio, Chart.js donut and line data visualizations of songs producer made by performer, albums and singles.**
<br/><br/>
![Producer](/static/images/readme/performer.gif)
<br/>

**Thanks for exploring!**
<br/><br/>
![Network](/static/images/readme/network.gif)
<br/>

<a name="future"/></a>
## Future Development
* Enable user profile creation for favorites saving.
* Implement algorithm to suggest music to user leveraging their favorites.


