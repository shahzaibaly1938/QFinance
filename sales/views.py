from django.shortcuts import render, redirect
from .models import Ticketsale, Destination, Airline, Adults, Childs, Route , Infants
from customers.models import Customer
from payments.models import Payment
from users.models import Agent
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal

# Create your views here.
def ticket_sale(request):
    tickets = Ticketsale.objects.all().order_by('-reserve_date')
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()

    # Filtering logic
    agent_id = request.GET.get('agent')
    customer_id = request.GET.get('customer')
    pnr = request.GET.get('pnr')
    flight_from_id = request.GET.get('flight_from')
    flight_to_id = request.GET.get('flight_to')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    if agent_id:
        filters['agent_id'] = agent_id
    if customer_id:
        filters['customer_id'] = customer_id
    if pnr:
        filters['pnr'] = pnr
    if flight_from_id:
        filters['flight_from_id'] = flight_from_id
    if flight_to_id:
        filters['flight_to_id'] = flight_to_id
    if start_date:
        filters['reserve_date__gte'] = start_date
    if end_date:
        filters['reserve_date__lte'] = end_date

    if filters:
        tickets = Ticketsale.objects.filter(**filters).order_by('-reserve_date')
        paginator = Paginator(tickets, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'tickets':page_obj,
        'customers':customers,
        'agents':agents,
        'destinations':destinations,
    }
    return render(request, 'sales/ticket_sale.html', context)



def add_ticket(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        commission_agent = request.POST.get('agent')
        manual_commission = request.POST.get('manual_commission')
        pnr = request.POST.get('pnr')
        airline = request.POST.get('airline')
        amount = request.POST.get('amount')
        reserve_date = request.POST.get('reserve_date')
        reference = request.POST.get('reference')
        payment = request.POST.get('payment')
        notes = request.POST.get('notes')
        flight_type = request.POST.get('flight_type')

        # Routes (multi-directional support)
        from_list = request.POST.getlist('from[]')
        to_list = request.POST.getlist('to[]')
        departure_dates = request.POST.getlist('departure_date[]')

        print(f"From List: {from_list}, To List: {to_list}, Departure Dates: {departure_dates}")


        # Passengers
        no_of_adults = int(request.POST.get('adults', 0))
        no_of_children = int(request.POST.get('children', 0))
        no_of_infants = int(request.POST.get('infants', 0))


        # Passenger details (if needed, can be processed here)
        # Example: request.POST.getlist('adult_name[]'), etc.

        # For now, save only the first route (extend as needed for multi-route)
        # Removed unused variables flight_from, flight_to, flight_date

        # Commission calculation (same as before)
        amount_decimal = Decimal(amount)
        agent = None
        final_commission = Decimal('0.00')
        if commission_agent:
            agent = Agent.objects.get(id=commission_agent)
            final_commission = amount_decimal * agent.commission_rate
            if manual_commission:
                final_commission += Decimal(manual_commission)

        ticket = Ticketsale(
            customer=Customer.objects.get(id=customer),
            commission=final_commission,
            manual_commission=Decimal(manual_commission) if manual_commission else Decimal('0.00'),
            pnr=pnr,
            agent=agent,
            airline=Airline.objects.get(id=airline),
            amount=amount_decimal,
            reserve_date=reserve_date,
            reference=reference,
            paid=payment,
            notes=notes,
            flight_type=flight_type,
            no_of_adults=no_of_adults,
            no_of_children=no_of_children,
            no_of_infants=no_of_infants,
        )
        ticket.save()

        # Save routes
        for i in range(len(from_list)):
            route = Route(
                ticket=ticket,
                from_destination=Destination.objects.get(id=from_list[i]),
                to_destination=Destination.objects.get(id=to_list[i]),
                departure_date=departure_dates[i]
            )
            route.save()

        # Save Adults
        adults_objs = []
        if no_of_adults > 0:
            for i in range(1, no_of_adults+1):
                name = request.POST.get(f'adult_name[{i}]')
                dob = request.POST.get(f'adult_dob[{i}]')
                nationality = request.POST.get(f'adult_nationality[{i}]')
                nid = request.POST.get(f'adult_nid[{i}]')
                passport_number = request.POST.get(f'adult_passport[{i}]')
                adult = Adults(
                    ticket=ticket,
                    name=name,
                    dob=dob if dob else None,
                    nationality=nationality if nationality else None,
                    id_number=nid if nid else None,
                    passport_number=passport_number if passport_number else None,
                )
                adult.save()
                adults_objs.append(adult)

        # Save Children
        children_objs = []
        if no_of_children > 0:
            for i in range(1, no_of_children+1):
                name = request.POST.get(f'child_name[{i}]')
                dob = request.POST.get(f'child_dob[{i}]')
                nationality = request.POST.get(f'child_nationality[{i}]')
                nid = request.POST.get(f'child_nid[{i}]')
                passport_number = request.POST.get(f'child_passport[{i}]')
                child = Childs(
                    ticket=ticket,
                    name=name,
                    dob=dob if dob else None,
                    nationality=nationality if nationality else None,
                    id_number=nid if nid else None,
                    passport_number=passport_number if passport_number else None,
                )
                child.save()
                children_objs.append(child)

        # Save Infants
        infants_objs = []
        if no_of_infants > 0:
            for i in range(1, no_of_infants+1):
                name = request.POST.get(f'infant_name[{i}]')
                dob = request.POST.get(f'infant_dob[{i}]')
                infant = Infants(
                    ticket=ticket,
                    name=name,
                    dob=dob if dob else None,
                )
                infant.save()
                infants_objs.append(infant)

        # For multi-directional, you may want to save multiple Ticketsale objects or related route objects

        # Redirect to payment step (pass ticket.id if ticket is created)
        return redirect('payment_process', ticket.id)
        # return redirect('ticket_sale')

    customers = Customer.objects.all()
    commission_agent = Agent.objects.all()
    destinations = Destination.objects.all()
    airlines = Airline.objects.all()

    context = {
        'customers': customers,
        'commission_agent': commission_agent,
        'destinations': destinations,
        'airlines': airlines,
    }
    return render(request, 'sales/add_ticket.html', context)
def payment_process(request, id):
    ticket = Ticketsale.objects.get(id=id)
    return render(request, 'sales/payment_step.html', {'ticket':ticket})

def ticket_detail(request, id):
    ticket = Ticketsale.objects.get(id=id)
    return render(request, 'sales/ticket_detail.html', {'ticket':ticket})

def delete_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    ticket.delete()
    messages.success(request, f'Ticket: {ticket.pnr} of {ticket.customer.name} is deleted successfully!')
    return redirect('ticket_sale')

def edit_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    if request.method == 'POST':
        customer = request.POST.get('customer')
        commission_agent = request.POST.get('agent')
        manual_commission = request.POST.get('manual_commission')
        pnr = request.POST.get('pnr')
        airline = request.POST.get('airline')
        amount = request.POST.get('amount')
        reserve_date = request.POST.get('reserve_date')
        reference = request.POST.get('reference')
        payment = request.POST.get('payment')
        notes = request.POST.get('notes')
        flight_type = request.POST.get('flight_type')

        # Routes (multi-directional support)
        from_list = request.POST.getlist('from[]')
        to_list = request.POST.getlist('to[]')
        departure_dates = request.POST.getlist('departure_date[]')

        no_of_adults = int(request.POST.get('adults', 0))
        no_of_children = int(request.POST.get('children', 0))
        no_of_infants = int(request.POST.get('infants', 0))

        amount_decimal = Decimal(amount)
        agent = None
        final_commission = Decimal('0.00')
        if commission_agent:
            agent = Agent.objects.get(id=commission_agent)
            final_commission = amount_decimal * agent.commission_rate
            if manual_commission:
                final_commission += Decimal(manual_commission)
                

        ticket.customer = Customer.objects.get(id=customer)
        ticket.agent = agent
        ticket.commission = final_commission
        ticket.manual_commission = Decimal(manual_commission) if manual_commission else Decimal('0.00')
        ticket.pnr = pnr
        ticket.airline = Airline.objects.get(id=airline)
        ticket.amount = amount_decimal
        ticket.reserve_date = reserve_date
        ticket.reference = reference
        ticket.paid = payment
        ticket.notes = notes
        ticket.flight_type = flight_type
        ticket.no_of_adults = no_of_adults
        ticket.no_of_children = no_of_children
        ticket.no_of_infants = no_of_infants
        ticket.save()

        # Update routes: delete old and add new
        Route.objects.filter(ticket=ticket).delete()
        for i in range(len(from_list)):
            route = Route(
                ticket=ticket,
                from_destination=Destination.objects.get(id=from_list[i]),
                to_destination=Destination.objects.get(id=to_list[i]),
                departure_date=departure_dates[i]
            )
            route.save()

        # Update Adults
        Adults.objects.filter(ticket=ticket).delete()
        for i in range(1, no_of_adults+1):
            name = request.POST.get(f'adult_name[{i}]')
            dob = request.POST.get(f'adult_dob[{i}]')
            nationality = request.POST.get(f'adult_nationality[{i}]')
            nid = request.POST.get(f'adult_nid[{i}]')
            passport_number = request.POST.get(f'adult_passport[{i}]')
            adult = Adults(
                ticket=ticket,
                name=name,
                dob=dob if dob else None,
                nationality=nationality if nationality else None,
                id_number=nid if nid else None,
                passport_number=passport_number if passport_number else None,
            )
            adult.save()

        # Update Children
        Childs.objects.filter(ticket=ticket).delete()
        for i in range(1, no_of_children+1):
            name = request.POST.get(f'child_name[{i}]')
            dob = request.POST.get(f'child_dob[{i}]')
            nationality = request.POST.get(f'child_nationality[{i}]')
            nid = request.POST.get(f'child_nid[{i}]')
            passport_number = request.POST.get(f'child_passport[{i}]')
            child = Childs(
                ticket=ticket,
                name=name,
                dob=dob if dob else None,
                nationality=nationality if nationality else None,
                id_number=nid if nid else None,
                passport_number=passport_number if passport_number else None,
            )
            child.save()

        # Update Infants
        Infants.objects.filter(ticket=ticket).delete()
        for i in range(1, no_of_infants+1):
            name = request.POST.get(f'infant_name[{i}]')
            dob = request.POST.get(f'infant_dob[{i}]')
            infant = Infants(
                ticket=ticket,
                name=name,
                dob=dob if dob else None,
            )
            infant.save()

        return redirect('ticket_sale')

    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()
    airlines = Airline.objects.all()

    context = {
        'customers': customers,
        'customer': ticket.customer,
        'agents': agents,
        'destinations': destinations,
        'airlines': airlines,
        'ticket': ticket,
    }
    return render(request, 'sales/edit_ticket.html', context)



# Airlines Views :

def airlines(request):
    airlines = Airline.objects.all()
    context = {
        'airlines':airlines,
    }
    return render(request, 'sales/airlines.html', context)


def add_airline(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        airline = Airline(name=name)
        airline.save()
        messages.success(request, 'Airline added successfully!')
        return redirect('airlines')
    return render(request, 'sales/add_airlines.html')


def edit_airline(request, id):
    airline = Airline.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        airline.name = name
        airline.save()
        messages.success(request, f'{airline.name} is updated successfully!')
        return redirect('airlines')
    return render(request, 'sales/edit_airline.html', {'airline':airline})

def delete_airline(request, id):
    airline = Airline.objects.get(id=id)
    if request.method == "POST":
        airline.delete()
    return redirect('airlines')

# Destinations Views :

def destinations(request):
    destinations = Destination.objects.all()
    context = {
        'destinations':destinations,
    }
    return render(request, 'sales/destinations.html', context)

def add_destination(request):
    # Store the referring URL (if any) to use after adding a destination
    if request.method == 'GET':
        next_url = request.META.get('HTTP_REFERER')
        if next_url:
            request.session['add_destination_next'] = next_url
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = Destination(name=name)
        destination.save()
        messages.success(request, 'Destination added successfully!')
        # Redirect to the referring page if available, otherwise to destinations
        return redirect(request.session.get('add_destination_next', 'destinations'))
    return render(request, 'sales/add_destinations.html')

def edit_destination(request, id):
    destination = Destination.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        destination.name = name
        destination.save()
        messages.success(request, f'{destination.name} is updated successfully!')
        return redirect('destinations')
    return render(request, 'sales/edit_destination.html', {'destination':destination})

def delete_destination(request, id):
    destination = Destination.objects.get(id=id)
    if request.method == "POST":
        destination.delete()
    return redirect('destinations')


# Cancel Ticket View

def cancel_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    
    return render(request, 'sales/cancel_ticket.html', {'ticket':ticket})

def auto_cancel_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    
    ticket.notes += f"\nTicket auto-cancelled by system.\n Amount: {ticket.amount} \n PNR: {ticket.pnr} \n commission: {ticket.commission} \n mannual_commission: {ticket.manual_commission} \n commission_percentage: {ticket.agent.commission_rate if ticket.agent else 0} \n payment_status: {ticket.paid} \n"
    ticket.amount = 0
    ticket.commission = 0
    ticket.manual_commission = 0
    ticket.paid = 'unpaid'
    payment = Payment.objects.filter(ticket=ticket).first()
    if payment:
        payment.delete()  
    ticket.status = 'auto_cancelled'  
    ticket.save()
    messages.success(request, f'Ticket: {ticket.pnr} of {ticket.customer.name} is auto-cancelled successfully!')
    return redirect('ticket_sale')


def self_cancel_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    
    ticket.notes += f"\nTicket self-cancelled by user.\n Amount: {ticket.amount} \n PNR: {ticket.pnr} \n commission: {ticket.commission} \n mannual_commission: {ticket.manual_commission} \n commission_percentage: {ticket.agent.commission_rate if ticket.agent else 0} \n payment_status: {ticket.paid} \n"
    ticket.amount = 0
    ticket.commission = 0
    ticket.manual_commission = 0
    ticket.paid = 'unpaid'
    payment = Payment.objects.filter(ticket=ticket).first()
    if payment:
        payment.delete()  
    ticket.status = 'self_cancelled'  
    ticket.save()
    messages.success(request, f'Ticket: {ticket.pnr} of {ticket.customer.name} is self-cancelled successfully!')
    return redirect('ticket_sale')

def no_show_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    
    ticket.notes += f"\nTicket marked as no-show.\n Amount: {ticket.amount} \n PNR: {ticket.pnr} \n commission: {ticket.commission} \n mannual_commission: {ticket.manual_commission} \n commission_percentage: {ticket.agent.commission_rate if ticket.agent else 0} \n payment_status: {ticket.paid} \n"
    ticket.amount = 0
    ticket.commission = 0
    ticket.manual_commission = 0
    ticket.paid = 'unpaid'
    payment = Payment.objects.filter(ticket=ticket).first()
    if payment:
        payment.delete()  
    ticket.status = 'no_show'  
    ticket.save()
    messages.success(request, f'Ticket: {ticket.pnr} of {ticket.customer.name} is marked as no-show successfully!')
    return redirect('ticket_sale')