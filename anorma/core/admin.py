from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Contact, Project, SocialMediaLink, TeamMember, UpcomingProject, ContentBlock, Event, ServiceContent

class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safely check for field existence before modification
        if self.instance.project_id:
            if 'upcoming_project' in self.fields:
                self.fields['upcoming_project'].widget = forms.HiddenInput()
        if self.instance.upcoming_project_id:
            if 'project' in self.fields:
                self.fields['project'].widget = forms.HiddenInput()

class ProjectContentInline(admin.TabularInline):
    model = ContentBlock
    form = ContentBlockForm
    fk_name = 'project'
    exclude = ('upcoming_project',)
    extra = 1
    ordering = ('order',)
    readonly_fields = ('content_type_block',)
    
    def get_readonly_fields(self, request, obj=None):
        # Allow changing content type when creating new
        if obj:
            return self.readonly_fields
        return ()

class UpcomingProjectContentInline(admin.TabularInline):
    model = ContentBlock
    form = ContentBlockForm
    fk_name = 'upcoming_project'
    exclude = ('project',)
    extra = 1
    ordering = ('order',)
    readonly_fields = ('content_type_block',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()

class ContentBlockInline(admin.StackedInline):  # Use stacked layout
    model = ContentBlock
    extra = 1  # Number of empty forms to show
    fields = ('content_type_block', 'order', 'text_content', 'image_content', 'video_url')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectContentInline]
    list_display = ('title', 'project_type', 'author')
    search_fields = ('title', 'description')

@admin.register(UpcomingProject)
class UpcomingProjectAdmin(admin.ModelAdmin):
    inlines = [UpcomingProjectContentInline]
    list_display = ('title', 'project_type', 'author', 'image')
    search_fields = ('title', 'description')

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('content_type_block', 'parent_display', 'order')  # Keep this line
    list_filter = ('content_type_block',)
    search_fields = ('text_content', 'video_url')
    
    # Rename the method to match list_display
    def parent_display(self, obj):
        return obj.project or obj.upcoming_project or obj.team_member
    parent_display.short_description = 'Parent'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    inlines = [ContentBlockInline]
    list_display = ('name', 'role')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('date', 'title', 'image', 'description')
        }),
    )

@admin.register(ServiceContent)
class ServiceContentAdmin(admin.ModelAdmin):
    list_display= ('preview_image', 'content_preview')

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}"/>', obj.image.url)
        return "No Image"
    preview_image.short_description = "Image Preview"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if obj.content else "No Content"
    content_preview.short_description = "Content Preview"



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')