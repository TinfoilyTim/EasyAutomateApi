My journey as a junior programmer building a mobile app that aims to simplify the creation and execution of running tasks on a server.

Easy Automate Api aims to simplify task execution and creation sush as bash scipts and python code on a remotre server. It runs all over Fast Api for easy javasript intergration.

My personal goal is to explore how an app is "supposed" to be built, learning react or another framework, learning how to create and use apis to communicate with servers. 

31/7/26
You can now create tasks and specify what variables are needed and whats expected inside them. So for ive only been specifying bool and string, as well as "movies|shows" which I intend to use as multiple choice selection. This will be handled on the client side. Will add support for python code later, for now it only creates bash script in userdeffs files. 

To see all tasks when you open the client it would go to / (only a get request), which lists all stored filenames in the userdeffs excluding .json files.

To run a task the client would get a json list from /prepare containing the name of the task as well as a nested json list of what variables are expected, this is loaded straight from the tasks corresponding .json file. This is so the client knows what to prompt the user for, either text input, true or false button or other multi choice. Then the client sends the updated json payload to /prepare/run which reaches the server where it reads through all the variable names and replaces all variables in the script with its corresponding json value.

Now the hard part, building the app. Wish me luck!
