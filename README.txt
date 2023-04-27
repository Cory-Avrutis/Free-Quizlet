Developed by Cory Avrutis, Mariela Badillo, and William Steven Matiz

# Free-Quizlet
This is our web application to simulate certain aspects of quizlet, !

A description of the problem you are trying to solve:
Recently, Quizlet has made their services a paid service. We believe that studying is hard enough and that users should continue to have a free experience to the learning environment that Quizlet has always made at a free price.

Any details regarding instructions for the user interface that is beyond the obvious:
  The user has a simple user interface and everything is fairly obvious. The user is first prompted to login/sign up. From there, there is a navigation bar at the top that at any point can redirect the user to wherever they want to go. The features that the user can click are: create set, view set, modify set. Additional features including learning features such as quiz mode and write mode. Quiz mode has a built-in tutorial, while write mode has minimalist instructions, as it is a simple feature.

A list of Python libraries you are using:
-pymongo[srv]
-bcrypt
-flask
-certifi

We are also using html and copy, but these two libraries do not require a pip install.

List of resources:
- Main website body (setting up the flask manager, logging in, setting up a basic home html) : https://www.youtube.com/watch?v=dam0GPOAvVI by Tech with Tim
- Write mode (heavily inspired by the type racing website. this video helps sets up that type racing affect) : https://www.youtube.com/watch?v=Hg80AjDNnJk
- Modal (pop-up) : https://www.youtube.com/watch?v=MBaw_6cPmAw&t=473s
- Flip cards affect : https://www.w3schools.com/howto/howto_css_flip_card.asp

Description of extra features: N/A. We developed the original requirements and no new features from that list were implemented.

Include a description of the separation of work (who was responsible for what piecesof the program):

Cory:
- Database (MongoDB)
- Flask manager
- Encryption / decryption (authorization)
- Set up the skeleton of the website (home html, css style reference sheet, nav bar)

Mariela:
- View set
- Quiz mode
- Set up screen that allows user to pick a set based off title
- Front end of the edit feature and handled error checking / input validation with database requests

Steven:
- Modals (pop-ups)
- Backend of the edit feature
- Create set

Description of how would we host the website for distrubition:
- To distribute we could either create an Azure or AWS instance to act as our web server, and allot the necessary RAM and proper OS. We would then use the apache HTPP server software to host the website.
The AWS/Azure instances would enable scaling of the virtual hardware resources dependent on user load, and Apache would secure many different aspects of our websites backend.
