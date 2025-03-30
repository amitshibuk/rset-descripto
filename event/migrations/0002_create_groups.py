# filepath: e:\Development\rsetdescripto\rsetdescripto\event\migrations\000X_create_groups.py
from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create Event Editors group
    event_editors_group, created = Group.objects.get_or_create(name='Event Editors')

    # Assign permission to change event status
    change_event_permission = Permission.objects.get(codename='change_event')
    event_editors_group.permissions.add(change_event_permission)

class Migration(migrations.Migration):

    dependencies = [# Adjust this dependency as needed
        ('event', '0001_initial'),  # Adjust this dependency as needed
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]