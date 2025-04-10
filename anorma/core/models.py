from django.db import models
from django.core.exceptions import ValidationError

class BaseProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="Unknown")
    font_color = models.CharField(max_length=7, default='#ffffff')
    background_color = models.CharField(max_length=7, default='#000000')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def content_blocks(self):
        return ContentBlock.objects.filter(
            models.Q(project=self) | models.Q(upcoming_project=self)
        ).order_by('order')

class Project(BaseProject):
    pass

class UpcomingProject(BaseProject):
    image = models.ImageField(upload_to='upcoming_projects/')

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='team_members/', blank=True, null=True)
    
    @property
    def content_blocks(self):
        return ContentBlock.objects.filter(team_member=self).order_by('order')

    def __str__(self):
        return f"{self.name} - {self.role}"

class ContentBlock(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='content_blocks'
    )
    upcoming_project = models.ForeignKey(
        UpcomingProject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='content_blocks'
    )
    team_member = models.ForeignKey(
        TeamMember,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='content_blocks'
    )

    content_type_block = models.CharField(max_length=10, choices=CONTENT_TYPES)
    order = models.IntegerField(default=0)
    
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(upload_to='content_blocks/images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def clean(self):
        # Validate single parent relationship
        parents = [self.project, self.upcoming_project, self.team_member]
        valid_parents = sum(p is not None for p in parents)
        
        if valid_parents != 1:
            raise ValidationError("Content block must belong to exactly one parent (Project, UpcomingProject, or TeamMember)")

        # Validate content type
        if self.content_type_block == 'text' and not self.text_content:
            raise ValidationError("Text content is required for text blocks")
        elif self.content_type_block == 'image' and not self.image_content:
            raise ValidationError("Image content is required for image blocks")
        elif self.content_type_block == 'video' and not self.video_url:
            raise ValidationError("Video URL is required for video blocks")

    def __str__(self):
        parent = self.project or self.upcoming_project or self.team_member
        return f"{self.get_content_type_block_display()} Block for {parent}"

class Event(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # Newest first

    def __str__(self):
        return f"{self.title} - {self.date}"
    
class ServiceContent(models.Model):
    content = models.TextField(help_text="the main text contetn of the service page")
    image = models.ImageField(upload_to='services_images/', blank = True, null = True, help_text='An optional image for the service page')
    def __str__ (self):
        return f"Service Content (ID: {self.id})"
    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True,)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__ (self):
        return f"{self.name} - {self.email}"
    
class SocialMediaLink(models.Model):
    name = models.CharField(max_length=100, help_text="The display text for the link (eg. Facebook)")
    url = models.CharField(max_length=500, help_text=" The URL of the social  media profile (e.g., 'https://facebook.com/example')")
    
    def __str__(self):
        return f"{self.name} - {self.url}"