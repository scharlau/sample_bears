

# This is a short guide to free Django deployments on Render

This example focuses on deploying a Django application in python to http://render.com This should cover most of the issues you find, even if your app is done in something else like Flask. By following this example you should avoid the 'quick start' documents on Render, which point you down a different path using poetry, which leads you to the paid plans.

This version uses the sqlite3 database. The postgresql database at render.com is only free for a limited time. That is not covered in this version of the guide. 

### Confirm db.sqlite3 is in your repository
If you are using a .gitignore file to keep extra things out of your repository, as is good practice, then you might find that your db.sqlite3 database is included in the gitignore file. This means, while you have a database locally, you do not have one in your repository. This would also mean, that you'll find the database is missing when you deploy to Render. Use these simple steps to fix this:
* comment out the line mentioning db.sqlite3
*  add the db.sqlite3 file to your repository with the 'git add ' command
*  make a new commit to your repository
*  push the commit to GitHub with the git push command

## Do the setup work
First, go create an account at Render. If you create an account using your GitHub username/password, then you automatically link that account to render and you can make use of this later.
Second, if you haven't already created the repository you're going to deploy to render, then do that. Be sure to use an account with some static files such as CSS, or some images.
We're now ready to start preparation work for our application.

## Do the preparation work for the application
In this section we assemble the components that you need to deploy your application on Render. This means a few new files need to be created, a few changes to your settings.py file, and you need some specific libraries added too.
First, we need to add a webserver for our application as you should not expect the built-in one for Django to work in production. It's not designed for that. We'll use gunicorn, so install that with the command:

    pip install gunicorn
    
Gunicorn is a simple server and we don't need to do anything else for now.

Second, we need to add the whitenoise library to our application so that it can serve up any files in our static folder. Be sure that your 'static' folder is set up correctly, as detailed here: https://github.com/scharlau/polar_bears_django_visuals After you have that correctly in place then use:

    pip install whitenoise

We can now open mysite/settings.py to tell the Django application that we're using whitenoise by adding this line to the 'Middleware' section in settings:

    'whitenoise.middleware.WhiteNoiseMiddleware',
    
Third, we need to generate a requirements.txt file in order for our application to know which libraries to install as dependencies. We can do that with the command:

    pip freeze ->requirements.txt
    
 This will create a new file with the relevant libraries and version numbers that you're using in your virtual environment.
 
 Fourth, you should now be able to make a new commit for your application. Be sure to add the requirements.txt file to the commit. Push this up to GitHub too.
 
 ## Setting up Render
 Go to your Dashboard and then add a new 'Web Service'. 
 Fill in the 'name' section as you wish - this becomes the name of the url you'll deploy too. 
 Let it choose the region.
 Point to the relevant GitHub repository that it should deploy from. 
 Leave root directory empty. 
 The build command should be this: pip install -r requirements.txt
 The start command should be: gunicorn mysite.wsgi:application
 Autodeploy should be 'yes' - although you'll need to keep triggering manual builds until it successfully deploys.
 
 Next, go to the 'environment' menu using the navigation on the left. We need to add some 'environment variables'. Add these ones - all in capitals:
 * ALLOWED_HOSTS and put the name of your app along with onreder.com as here: sample-bears.onrender.com
 * CSRF_TRUSTED_ORIGINS which is the name you put in the line above with the https:// preceding it, so https://sample-bears.onrender.com
 * PYTHON_VERSION where you can put 3.10.7 or whatever you're using.
 
 That should be everything you need for this part. We now need to return to our application and make a few final changes.
 
 ## Changing the settings.py file
 Now that we know the name and URL of our application we can modify the settings file to put the url in the 'ALLOWED_HOSTS' of our application. Go to that section and add the one you put in the ALLOWED_HOSTS of the environment variables.
 Also add in the one for CSRF_TRUSTED_ORIGINS too.
 Save the file.
 Make a new commit and push this to GitHub.
 
 ## Try the manual build/deploy on Render
 With all of this now in place you should go back to your web service in Render and use the 'Manual Deploy' option in the top right corner to pull in the latest commit from GitHub.
This is sloow. This is what you get on the 'free tier'. Do something else for a bit and then come back to see the log.
If you find errors, then fix your settings.py file, or whatever, make a new commit, push that to GitHub, and then use the 'Manual Deploy' again.
Eventually, it will all work and you'll see your application running on Render.com

