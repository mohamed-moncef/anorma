
from django.shortcuts import get_object_or_404, render, redirect
from .models import Project, SocialMediaLink, TeamMember, UpcomingProject, Event, ServiceContent
from .forms import ContactForm
from django.contrib import messages

def home(request):
    # Order projects by most recent first
    projects = Project.objects.all().order_by('-id')
    upcoming_projects = UpcomingProject.objects.all().order_by('-id')
    
    return render(request, 'core/home.html', {
        'projects': projects,
        'upcoming_projects': upcoming_projects,
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    content_blocks = project.content_blocks.all().order_by('order')
    
    # Navigation between projects
    prev_project = Project.objects.filter(id__lt=project_id).order_by('-id').first()
    next_project = Project.objects.filter(id__gt=project_id).order_by('id').first()

    return render(request, 'core/project_detail.html', {
        'project': project,
        'content_blocks': content_blocks,
        'prev_project': prev_project,
        'next_project': next_project,
    })

def upcoming_project_detail(request, project_id):
    project = get_object_or_404(UpcomingProject, pk=project_id)
    content_blocks = project.content_blocks.all().order_by('order')  # Added content blocks
    
    # Navigation between upcoming projects
    prev_project = UpcomingProject.objects.filter(id__lt=project_id).order_by('-id').first()
    next_project = UpcomingProject.objects.filter(id__gt=project_id).order_by('id').first()

    # Print or log for debugging purposes
    print(f"Previous Project: {prev_project}, Next Project: {next_project}")

    return render(request, 'core/upcoming_project_detail.html', {
        'project': project,
        'content_blocks': content_blocks,  # Added to context
        'prev_upcoming': prev_project,     # Renamed for clarity
        'next_upcoming': next_project,     # Renamed for clarity
    })

def about(request):
    team_members = TeamMember.objects.all().order_by('name')
    return render(request, 'core/about.html', {
        'team_members': team_members
    })

def team_member_detail(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    content_blocks = member.content_blocks.all().order_by('order')
    return render(request, 'core/team_member_detail.html', {
        'member': member,
        'content_blocks': content_blocks
    })

def actualites(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'core/actualites.html', {'events': events})

def services(request):
    try:
        content =  ServiceContent.objects.first()
    except ServiceContent.DoesNotExist:
        content = None
    return render(request, 'core/services.html', {'content':content})


def contact_view(request):
    # Initialize the form variable
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the same page after submission

    social_media_links = SocialMediaLink.objects.all()
    return render(request, 'core/contact.html', {
        'form': form,
        'social_media_links': social_media_links,
    })
