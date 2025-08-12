from django.db import migrations


def populate_learning_activities(apps, schema_editor):
    LearningActivity = apps.get_model('core', 'LearningActivity')

    activities = [
        {
            'activity_name': 'Circle Time',
            'description': 'Morning circle time for sharing and discussion',
            'category': 'social',
            'age_group': '3-5 years',
            'duration_minutes': 30
        },
        {
            'activity_name': 'Story Reading',
            'description': 'Reading stories to develop literacy skills',
            'category': 'literacy',
            'age_group': '3-5 years',
            'duration_minutes': 20
        },
        {
            'activity_name': 'Number Games',
            'description': 'Fun games to learn basic counting and numbers',
            'category': 'numeracy',
            'age_group': '3-5 years',
            'duration_minutes': 25
        },
        {
            'activity_name': 'Art and Craft',
            'description': 'Creative activities using various materials',
            'category': 'art',
            'age_group': '3-5 years',
            'duration_minutes': 45
        },
        {
            'activity_name': 'Outdoor Play',
            'description': 'Physical activities in the playground',
            'category': 'physical',
            'age_group': '3-5 years',
            'duration_minutes': 30
        },
    ]

    for activity_data in activities:
        LearningActivity.objects.get_or_create(**activity_data)


def reverse_populate_learning_activities(apps, schema_editor):
    LearningActivity = apps.get_model('core', 'LearningActivity')
    LearningActivity.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_create_system_models'),
    ]

    operations = [
        migrations.RunPython(
            populate_learning_activities,
            reverse_populate_learning_activities
        ),
    ]