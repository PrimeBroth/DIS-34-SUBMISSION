# Group 34's DIS project submission

# Acknowledgement
- This project is released under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007, see `LICENSE` for more information
- This project is based on the nft-crypto-punk which is also GPL v.3
- The project was written by
	- Nicholas Wood | sfx355@alumni.ku.dk
	- Ludvig Viktor Lindmark | hsm508@alumni.ku.dk
	- Martin Grønlykke Wassman | bxq225@alumni.ku.dk
- Pokemon is the intellectual property of nintendo. The DIKUMON project falls under fair use in the EU, as it is for educational purposes and not for profit.

![](tmp/dikupic.PNG)

# running dikudex:

Assumes a working Python 3 installation (with python=python3 and pip=pip3).
Assumes a working psql installation callable from commandline.

(1) Run the code below to install the dependencies.
`>$ pip install -r requirements.txt`

(2) Make sure you are in the root directory of dikudex. Run the `init_project.py`. It *SHOULD* determine all the filepaths on your system correctly
`>$ python init_project.py <dbname> <user> <host> <password>`

(3) You will be prompted for your db password again by db

(4) Script will generate `init_db_test.sql` which sets up the database. Finally the script calls `python src/app.py <dbname> <user> <host> <password>` with the same values as you specified earlier

*OPTIONAL IF ABOVE FAILS*
(!) If for some reason the init script can't run `init_db_test.sql` from psql or can't start the app, please run the sql manually from psql/ pgAdmin and start `python src/app.py <dbname> <user> <host> <password>` from your terminal/ commandline to suit your system requirements

# How to use the application:
We suggest the following course throught the project to convince the TA that the project satisfies the criteria

(1) *Login*
There is no standard user, so please press create account. Once done, enter credentials.

(2) *Create account*
Choose username and password. The authors favourites during testing were username: 'a' and password '1' because it was fast.
This makes an `INSERT` in the `USERS` table.
Will redirect to login.

(3) *Home*
Once logged in, 10 random DIKUMON will be displayed. 
This is done via a `SELECT` from the `DIKUMON` table.
Press any image to go to the page related to the particular DIKUMON

(4) DIKUMON page
Here you can see all the stats pertaining to a DIKUMON.
If you feel strongly about a DIKUMON, you can review it. Enter a number in the rating and maximum 256 characters into the review field. Press post and see it appear in the column showing all users reviews of the DIKUMON.
This is also `INSERT`

(5) Create
Now you may feel inspired to create your own _original_ DIKUMON.
Press `Create` in the navbar. Fill out the form and choose an image to represent your creation. Post it. 
This is also `INSERT`

(6) DikuList
In the DikuList you may filter DIKUMON by entering a series of characters into the input field and pressing `go`.
Only DIKUMON whose names contain these characters will appear.
This satisfies the regex criterion.

(7) Profile
Finally, you can look back on all your fine work in the DIKUMON community by going to your `Profile` page.
Here you can see all your created DIKUMON and the reviews written by you.
If you don't feel it represents you accurately any more, you may delete your DIKUMON or reviews individually or all of them with the buttons at the bottom of the page.
This is `DELETE`
At the end of the day, if you feel that you have finally outgrown you beloved DIKUMON and it is time to leave the community for good, you may delete your user and all data pertaining to it by pressing `delete my profile` (remember to mark the checkbox)
This is also `DELETE`



