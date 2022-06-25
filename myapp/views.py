import datetime
from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Flights
from myapp.models import Customers
from itertools import chain
from django.utils import timezone
from django.shortcuts import redirect
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#Function to return the homepage
def homepage(request):
    return render(request, 'homepage.html', {})

#Function to return confirmation page of booking
@login_required
def form(request):
    number = request.POST.get('flightNo')
    return render(request, 'form.html', {'data':Flights.objects.get(flightNo=number)})

#Function to return total list of available flights
def flights(request):
    return render(request, 'flights.html', {})

#Function to input all required flights - activate in admin page
def newsched(request, request2, request3):
    currentTime = datetime.datetime.now()
    #How many weeks of flights
    weeks = 26
    datetimeInitial = datetime.datetime(2022, 6, 10, 6, 0) #Set up using Friday as day 0 (10 June - Y M D H M)
    #Every flight on its corresponding days, multiplied by amount of weeks entered above (weeks = )
    for week in range(weeks):
        #Sydney and Sydney return
        #Create new flight with parameters, and save
        sydney = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=7*week), arrivalDate=datetimeInitial + datetime.timedelta(days=7*week, hours=3),  #4 hours + 1 hour for picking up passengers - 2 hours from timezones
                         fromAirport='NZNE', toAirport='YSSY', planeType='SyberJet', remainingSeats='6', flightNo=10000+week,
                         price='3500', stopOvers='1 - Rotorua')
        sydney.save()

        sydneyreturn = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=2+7*week, hours=9), arrivalDate=datetimeInitial + datetime.timedelta(days=2+7*week, hours=14, minutes=30), #3.5 hour flight + 2 hours from timezones
                               fromAirport="YSSY", toAirport='NZNE', planeType='SyberJet', remainingSeats='6', flightNo=20000+week, price='3000', stopOvers='0')
        sydneyreturn.save()

        #Lake Tekapo and Lake Tekapo return
        tekapo = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=7*week+3), arrivalDate=datetimeInitial+datetime.timedelta(days=7*week+3, hours=1, minutes=20), #1 hour 20 minute flight
                         fromAirport='NZNE', toAirport='NZTL', planeType='HondaJet', remainingSeats='5', flightNo=90000+week, price='1250', stopOvers='0')
        tekapo.save()
        tekaporeturn = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=7*week), arrivalDate=datetimeInitial+datetime.timedelta(days=7*week, hours=1, minutes=30), #1.5 hour flight
                              fromAirport='NZTL', toAirport='NZNE', planeType='HondaJet', remainingSeats='5', flightNo=100000+week, price='1400', stopOvers='0')
        tekaporeturn.save()


        for day in range(7):
            #Rotorua and Rotorua return
            if day in [0,3,4,5,6]: #0 is a Friday
                rotorua = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, minutes=40), #40 minute flight
                                  fromAirport="NZNE", toAirport='NZRO', planeType='Cirrus', remainingSeats='4', flightNo=30000+10*week+day, price='550', stopOvers='0')
                rotorua.save()
                rotoruaReturn = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=6), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=6, minutes=45), #45 minute flight
                                        fromAirport='NZRO', toAirport='NZNE', planeType='Cirrus', remainingSeats='4', flightNo=40000+10*week+day, price='600', stopOvers='0')
                rotoruaReturn.save()
            #Great Barrier Island
            if day in [0,3,5]:
                claris = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, minutes=40),#40 minute flight
                                 fromAirport='NZNE', toAirport='NZGB', planeType='Cirrus', remainingSeats='4', flightNo=50000+10*week+day, price='550', stopOvers='0')
                claris.save()
            #Great Barrier Island return
            if day in [0,1,4]:
                clarisReturn = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=3), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=3, minutes=45),  #45 minute flight
                                       fromAirport='NZGB', toAirport='NZNE', planeType='Cirrus', remainingSeats='4', flightNo=60000+10*week+day, price='600', stopOvers='0')
                clarisReturn.save()
            #Chatham Islands
            if day in [0,4]:
                tuuta = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=3), #2 hr 15 min flight + 45 mins timezone
                                fromAirport='NZNE', toAirport='NZCI', planeType='HondaJet', remainingSeats='5', flightNo=70000+10*week+day, price='2250', stopOvers='0')
                tuuta.save()
            #Chatham Islands return
            if day in [1,5]:
                tuutaReturn = Flights(leavingDate=datetimeInitial + datetime.timedelta(days=day+7*week), arrivalDate=datetimeInitial + datetime.timedelta(days=day+7*week, hours=1, minutes=15),
                                      fromAirport='NZCI', toAirport='NZNE', planeType='HondaJet', remainingSeats='5', flightNo=80000+10*week+day, price='2000', stopOvers='0') #2 hour flight - 45 minutes timezone
                tuutaReturn.save()

    #Don't include flights that have already left
    for flight in Flights.objects.all():
        if currentTime > flight.leavingDate:
            flight.delete()

    return HttpResponse('<p>Schedule filled</p>')

#Function to return invoice after submitted booking
@login_required
def invoice(request):
    fName = request.user.first_name
    lName = request.user.last_name

    x = Flights.objects.get(flightNo=request.POST.get('flightNo'))
    #If no remaining seats, return error
    if x.remainingSeats > 0:
        #Get next flight number from number.txt file, write next number to file
        file = open('myapp/number.txt', 'r')
        bookNo = File(file)
        bookingNumber = bookNo.read()
        file.close()
        file2 = open('myapp/number.txt', 'w')
        bookNo2 = File(file2)
        bookNo2.write(str(int(bookingNumber) + 1))
        file2.close()

        number = request.POST.get('flightNo')

        #Create new customer object attributed to this flight
        customer = Customers(flightNo=Flights.objects.get(flightNo=number), firstName=fName, lastName=lName, bookingNo=bookingNumber)
        customer.save()

        #Decrement remaining seats on the flight
        x = Flights.objects.get(flightNo=number)
        x.remainingSeats = x.remainingSeats - 1
        x.save()
        return render(request, 'invoice.html', {'data':Flights.objects.get(flightNo=number), 'number':bookingNumber, 'fName':fName, 'lName':lName})
    return render(request, 'error.html', {})

#Function to return list of every available flight, can be filtered by any of the html inputs
def showflights(request):
    dDate = request.POST.get('dDate') #Earliest date you want to leave
    aDate = request.POST.get('aDate') #Latest date you want to arrive
    dAir = request.POST.get('dAir')
    aAir = request.POST.get('aAir')

    data = Flights.objects.all().order_by('leavingDate')

    #Only elements of the form that were filled in can filter the search query
    if dDate != '' and dDate is not None:
        data = data.filter(leavingDate__gte=dDate)
    if aDate != '' and aDate is not None:
        data = data.filter(arrivalDate__lte=aDate)
    if dAir != '' and aAir is not None:
        data = data.filter(fromAirport=dAir)
    if aAir != '' and dAir is not None:
        data = data.filter(toAirport=aAir)

    return render(request, 'flights.html', {'data':data, 'current':datetime.datetime.now()})

#Function to return list of all flights the current account has booked
@login_required
def showBookedFlights(request):
    fName = request.user.first_name
    lName = request.user.last_name
    allData = Customers.objects.select_related('flightNo')
    return render(request, 'bookedFlights.html', {'data':allData.filter(firstName=fName, lastName=lName)})

#Function to return confirmation page for the cancellation of a flight
@login_required
def cancel(request):
    number = request.POST.get('flightNo')
    fName = request.POST.get('fName')
    lName = request.POST.get('lName')

    flight = Flights.objects.get(flightNo=number)

    bookingNo = request.POST.get('bookingNo')

    customer = Customers.objects.get(firstName=fName, lastName=lName, flightNo=flight, bookingNo=bookingNo)

    return render(request, 'confirmation.html', {'customer':customer, 'data':Flights.objects.get(flightNo=number)})

#Function to take cancellation data, delete the customer from the flight and increment the remaining seats on the flight
#Then returns the list of all available flights
@login_required
def confirm(request):
    number = request.POST.get('flightNo')
    fName = request.POST.get('fName')
    lName = request.POST.get('lName')
    bookingNo = request.POST.get('bookingNo')

    flight = Flights.objects.get(flightNo=number)

    customer = Customers.objects.get(firstName=fName, lastName=lName, flightNo=flight, bookingNo=bookingNo)
    customer.delete()

    flight.remainingSeats = flight.remainingSeats + 1
    flight.save()

    allData = Customers.objects.select_related('flightNo')

    return render(request, 'bookedFlights.html', {'data':allData.filter(firstName=fName, lastName=lName)})

#Function to return account creation page
def createAccount(request):
    return render(request, 'createAccount.html', {})

#Once account has been created, return to homepage, take data and create user
def doneAccount(request):
    User.objects.create_user(username=request.POST.get('user'), password=request.POST.get('pass'), first_name=request.POST.get('fName'), last_name=request.POST.get('lName'))
    return render(request, 'homepage.html', {})

#Return login page, authenticate user, show error if credentials are wrong, log in and return to homepage if credentials are correct
def login2(request):
    if request.POST.get('user') == None:
        return render(request, 'login.html', {})
    user = authenticate(request, username=request.POST.get('user'), password=request.POST.get('pass'))
    if user is not None:
        login(request, user)
        return render(request, 'homepage.html', {})
    else:
        return render(request, 'login.html', {'error':'Incorrect Credentials'})

#Function to return logout page
def logout2(request):
    logout(request)
    return render(request, 'homepage.html', {})

#Function to return page showcasing available routes, with picture of each route (stored in static)
def routes(request):
    return render(request, 'routes.html', {})
