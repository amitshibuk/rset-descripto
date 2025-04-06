from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .models import Event, EventDetails
from .forms import EventForm, EventStatusForm, EventUpdateForm
import requests
from django.http import JsonResponse

@login_required
def event_list(request):
    events = Event.objects.all().order_by('-event_id')
    status_filter = request.GET.get('status')
    organizer_filter = request.GET.get('organizer')

    # Apply filters if they are provided
    if status_filter:
        events = events.filter(status=status_filter)
    if organizer_filter:
        events = events.filter(organizer__icontains=organizer_filter)

    return render(request, 'event/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event/event_detail.html', {'event': event})

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.in_charge = request.user
            event.status = 'Pending'
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'event/create_form.html', {'form': form})

@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.in_charge != request.user and not request.user.groups.filter(name='Event Editors').exists():
        return redirect('event_list')

    if request.method == "POST":
        if request.user.groups.filter(name='Event Editors').exists():
            form = EventStatusForm(request.POST, instance=event)
        else:
            form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        if request.user.groups.filter(name='Event Editors').exists():
            form = EventStatusForm(instance=event)
        else:
            form = EventForm(instance=event)
    return render(request, 'event/edit_form.html', {'form': form, 'event': event})

@login_required
def delete_post(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.in_charge != request.user:  # Restrict deletion to the author
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        event.delete()
        return redirect('event_list')

    return render(request, 'event/delete_event.html', {'event': event})

@login_required
def approve_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.groups.filter(name='Moderators').exists():
        event.status = "Approved"
        event.save()
    return redirect('event_detail', pk=pk)

@login_required
def reject_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.groups.filter(name='Moderators').exists():
        event.status = "Rejected"
        event.save()
    return redirect('event_detail', pk=pk)

@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.in_charge != request.user and not request.user.groups.filter(name='Event Editors').exists():
        return redirect('event_list')

    # Get the related EventDetails object or create a new one if it doesn't exist
    event_details, created = EventDetails.objects.get_or_create(event=event)

    if request.method == "POST":
        form = EventUpdateForm(request.POST, request.FILES, instance=event_details)
        if form.is_valid():
            # Set the event field explicitly before saving
            event_details = form.save(commit=False)
            event_details.event = event  # Explicitly set the event field
            event_details.save()
            return redirect('event_detail', pk=event.pk)
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = EventUpdateForm(instance=event_details)
    return render(request, 'event/update_form.html', {'form': form, 'event': event})


@login_required
def send_event_files(request, pk):
    # Get the event and its related EventDetails
    event = get_object_or_404(Event, pk=pk)
    try:
        event_details = EventDetails.objects.get(event=event)
    except EventDetails.DoesNotExist:
        return JsonResponse({'error': 'EventDetails not found for this event.'}, status=404)

    # Collect all files from EventDetails
    files = {}
    files['event'] = event.name
    if event_details.report_details:
        files['report_details'] = event_details.report_details.file
    if event_details.feedback_text:
        files['feedback_text'] = event_details.feedback_text.file
    if event_details.rating:
        files['rating'] = event_details.rating.file
    if event_details.participant_count:
        files['participant_count'] = event_details.participant_count.file

    # Target server URL
    target_url = "https://webhook.site/62f55e3d-cacb-489a-ab8d-6693ebe17248"  # Replace with the actual API endpoint

    # Send the POST request with the files
    try:
        #response = requests.post(target_url, files=files)
        requests.post(target_url, files=files)
        #response.raise_for_status()  # Raise an error for HTTP errors
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    # Mark the event as closed
    event.status = 'Closed'
    event.save()

    # Return the response from the target server
    return redirect('event_detail', pk=pk)