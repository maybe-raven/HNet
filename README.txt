HealthNet is meant to enable their hospitals in the US to be able to manage both employees and patients. The successful implementation should make it easy for users to effortlessly sign-up as patients so that the hospital can, without difficulty, manage their procedures and patient related tasks to optimize day-to-day work-flow.
The HealthNet product is intended to improve hospitals by providing an easy mechanism for managing employees, gathering statistical data on the inner workings of the hospital, signing up patients, making appointments, and allowing ease of transfer of both patients and their information between hospitals.


Installation:
	1) unzip file to target location
	2) open cmd.exe or Terminal.app and navigate to target location where the files have been unzipped
	3) go to the directory with manage.py in it
	4) execute command "python manage.py makemigrations"
	5) execute command "python manage.py migrate"
	6) execute command "python manage.py setupgroups"
	6) execute command "python manage.py createsuperuser"

Known Bugs/Disclaimers:
	- Calendar has not been setup to view a doctors schedule yet to see if it is conflicting
	- only super user (admins) can create location
	- only patient can be made through the website, nurse and doctor need to be added through admin console

Known Bugs/Disclaimers:
	- currently, a super user (admin) is required to use this product, since certain data can only be managed by a super user, including:
	    - hospitals
	    - doctor accounts
	    - nurse accounts
	    - treatment sessions
	    - tests
	    - diagnosis
	    - drugs
	    - prescriptions
	    - locations (for appointments)
    - calendar has not been set up for a patient to view a doctor's available time slots


Known Missing Release-1 features:
	- calendar has not been setup to follow doctors


Once a doctor, patient, nurse has been made, they are able to visit the calendar and view/create appointments.
Logging is handled by the system to display all information regarding signing in and out and other server commands.


Basic execution and usage instructions (logins & passwords):
	To run
	1) find out your device/server ip address
	2) use a text editor and edit the hnet/settings.py file in the project root folder
	3) add your ip address to the `ALLOWED_HOSTS` array, then save and close your text editor
	4) open cmd.exe or Terminal.app and navigate to the project root folder
	5) execute command "python manage.py runserver 0.0.0.0:8080"
	6) now you can access the website at "<your_ip>:8080/"

	Sign in and sign up
	1) navigate to the home page (at "<your_ip>:8000/")
	2) from the home page, you should see the links to the "sign in" and "sign up" page
	7) follow the instructions on the web page to complete the sign in or the sign up process

	To change information associated with your account
	1) login from the home page
	2) after you're logged in you should see a link to go to your dashboard, use it to navigate to your dashboard
	    if you don't see the link, navigate to to home page and you will be redirected to your dashboard
	3) from your dashboard, you should see links to the pages where you can edit your account information

	To view appointments
	1) login from the home page
	2) from your dashboard, you should see a link to the calendar page
	3) in the calendar page, you can view your appointments shown in a calendar view
	4) in the calendar page, you can navigate to the previous month or the next month by clicking on the arrows to the left and right sides of the display of current month
	5) from the calendar page, you can click on the "Today" button located right under the display of current month to see a list of appointments you have for today with more details
	6) from the calendar page, you can also click on any day in the calendar view to see a list of appointments you have for that given day with more details

	To schedule an appointment
	1) login from the home page
	2) from your dashboard, go to the calendar page, then go to "Today" overview page
	3) click on the "Create" button
	4) fill out and submit the form

	To cancel an appointment
	1) login from the home page
	2) from your dashboard, go to the calendar page, then go to overview page of the day of the appointment you want to cancel
	3) under the appointment you want to cancel, locate the "Cancel" button and click it
	4) confirm when prompted
