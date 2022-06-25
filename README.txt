Assignment 2 - 159.352 - Hayden Stimpson - 19032670

To run:
Open cmd in this files directory.
enter: python manage.py runserver
on browser: go to 'localhost:8000'

All data is organized on 2 seperate models, the Customers and the Flights. These are combined with a junction table when applicable. 
Currently the program is set to have 26 weeks of data when the admin account creates a new set of flights. These days use the actual dates.

The landing page is the homepage, which includes a navigation bar to every other page.
The data can be browsed in the 'Book a Flight' navigation button, and on this page the user can filter the data using the form inputs near the top of the screen.
Whenever a flight is booked, the remaining seats on that flight is decremented by one. 
Whenever a flight is cancelled, the remaining seats on that flight is incremented by one,  
Once a flight has been booked, an invoice page will be displayed, with information about the flight, a booking number, and a picture of the route.

Styling of the pages is done via style.css, which is located in myapp/static. Every page uses this css file.

The program handles bookings via an account system. Before accessing certain pages, the user will be asked to login to their account if they haven't already. If they don't have an account,
the 'Create Account' button is always located at the top of the screen. Users also have the option to logout via the 'Logout' button in the navigation bar. 
Whenever a user is logged in, the right side of the navigation bar will display 'Welcome <Username>' to indicate that the user is logged in.
The login button only appears if the user is not logged in, otherwise it changes to a logout button.

One of the buttons in the navigation bar is the 'Our Routes' button. This links to a page where every available route the airline is shown with a picture and a title. 

The program also features an admin page. (The admin account is: User:admin Pass:admin)
Here an admin can see all users accounts, all customers from the Customers model, and all flights from the Flights model. 
The admin is able to add, remove, edit, and read any of these models. For users, their account password is hashed so the admin cannot see it. 
The admin has an added action through the admin page, which is to call the newsched() function in views.py. This function creates all the flights outlined in the assignment for the next
26 weeks from the date set in that function. This is useful if the databse is flushed, so that all the flights can be added quickly. 
This function can be accessed on the admin page through the action submenu on any page. 