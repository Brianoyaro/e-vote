# e_vote v1.00
---
### Introduction
---
e_vote is an application which allows voters to vote from the comfort of their home without the hassle of making long queues. It has been created with security in mind that it prevents fraudulous voting in the sense of:
- voting multile times using a validated account
- misusing the url to vote as an unidentified user
- Offering redundancy of tally scores in different locations 
- Each validated user is permited to vote in a limited time i.e 10 minutes ater which they'll have to login and start the entire process again

On the contestants side, they get to see their tally results in real time while the voting process is ongoing which reduces discrepancies.

e_vote has a nice UX which is easy to use.

### setup
---
- First, clone the application and git pull on your local machine.
- Install necessary dependencies in the requirements.txt file. If you are on a linux/unix system, pip install -r requirements.txt will do.
- Start the application using flask run then use a suitable application server to serve the website to your clients

### Architecture
---
e_vote was created with security in mind. Users have to login using credential in their national ID cards which helps distinguish candidate positions based on locality such as governors and MPs. Users have an option of changing their voting location simulating real world scenarios where they relocate to diferent regions to the ones recorded in their ID cards.
Users have a time limit of 10 minutes to vote upon which on exhaustion requires them to relogin and vote again incase they did not submit their results.
![alt text](https://github.com/Brianoyaro/e-vote/blob/main/app/static/logo.png "Logo")

### /API
---
e_vote incorporates an api which allows one see vting results as they trickle in realtime. The api was desgned for candidates to have live feeds of results. It provides data in json format which can be intergrated to external services of choices for visual appeals as one might need.
- /api/tally
This endpoint shows tally results for all candidates in the entire system

- /api/president/tally
Shows tally results for presidential candidates

- /api/governor/tally
Shows tally results for governor candidates

- /api/mp/tally
Shows tally results for mp candidates

- /api/candidates
Shows all candidates competting in the voting process

- /api/presidents
Shows all presidential candidates competing

- /api/governors/<county>
Shows all governor candidates competing in a given county

- /api/mps/<constituency>
Shows all MP candidates competing in a given constitueny

- /api/counties
Shows all counties

- /api/<county>/constituency
Shows all constituencies in a given county

### Related projects
---
- [Maji](https://github.com/Brianoyaro/Maji) : An application that connects water vendors and water buyers with an aim of tackling water shortage.
- [Simple shell](https://github.com/Brianoyaro/simple_shell) :  A custom command line interprator written in C.

### Team
---
- Brian Mokua [Twitter](https://twitter.com/Brianoyaro9)
