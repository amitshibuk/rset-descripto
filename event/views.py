from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .models import Event, EventDetails
from .forms import EventForm, EventStatusForm, EventUpdateForm

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
def update_event (request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.in_charge != request.user and not request.user.groups.filter(name='Event Editors').exists():
        return redirect('event_list')

    if request.method == "POST":
        form = EventDetails(request.POST, instance=event)
        if form.is_valid():
            event_update = form.save(commit=False)
            event_update.event = event.event_id
            event_update.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventUpdateForm(instance=event)

    return render(request, 'event/update_form.html', {'form': form, 'event': event})