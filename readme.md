# Welcome to BabysitterBuck$!


*BabysitterBuck$ is an implementation of a kata challenge that aligns to the following rules:*

The babysitter...
- starts no earlier than 5:00PM
- leaves no later than 4:00AM
- gets paid $12/hour from start-time to bedtime
- gets paid $8/hour from bedtime to midnight
- gets paid $16/hour from midnight to end of job
- gets paid for full hours (no fractional hours)
- gets paid for only 1 night of work
- receives a calculation for their nightly charge
 
Additional assumptions I made:
- Children should not be asleep before the babysitter arrives
- Children should go to bed before midnight
- Rounding of pay to the next integer occurs at the sub-total level. Babysitters got to make those buck$. 

**Implementation:**
I decided to implement a Flask app (python) to make this kata. Why? Even though a GUI was not meant to be the focus of the app, well, user interfaces are helpful to humans. But making a pretty and human-friendly app wasn't the only reason for this. HTML5 API enables simple implementation of a client-side validation system very quickly, and personally, I preferred that over multiple "input()" entries or a Jupyter Notebook, where I wouldn't necessarily have that validation built-in. In other words, setting up a Flask app enabled me to collect user input quickly and in a predictable format. And yes, I admit. There was a small bonus in that it limited the number of unit tests that I needed to be write...


**Frontend:** This is a pretty minimalistic Bootstrap5/HTML5 frontend and a tiny bit of CSS. There's only 1 HTML file with some Jinja logic and some minor client-side validation from the HTML5 API (as mentioned above). There's one image which I borrowed from FontAwesome ("sack-dollar"). 


**Backend:** Python. No database. App.py contains the routes and app constructor, while logic.py contains the logic. Pytest was used for unit and functional testing. Pytest-cov was the pytest plugin I used to enable creation of coverage reports.  

Overall, this was a lot of fun, and I'm grateful for the opportunity to complete this kata. 

**Documentation:**

(Please forgive me if this is excessive)

Running the app:
Given the python3 is installed and a virtual environment is set up and activated, in the commandline, after navigating to the root folder, run: 
```
pip install -r requirements.txt
python app.py
```
In your browser, navgiate to "localhost:5000", and you will see the app. :-)

Testing with Pytest:
In the commandline, after navigating to the root folder, run: 
```
python -m pytest
```
There, you should see all the tests, unit (logic_test.py) and functional (app_test.py), for this application. 

Interested in the coverage report?
In the commandline, after navigating to the root folder, run: 
```
pytest --cov
```

**Ideas for Improvements/Additional Functionality:**
There would be several things I would like to adjust given a longer timeline, but these would be my thoughts:
- Implement Pytest Fixtures (as seen in conftest.py) in logic_test.py to simplify code, where possible
- Allow users to alter their rate per hour
- Enable users to download a pdf invoice of their charges
- Utilize HTMX on a Server-Side Rendered website
- Converting this app into a SPA, using Flask RESTful API w/ React.js


