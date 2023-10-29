import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0007_alter_appointment_meeting_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='meeting_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 13, 47, 15, 829709, tzinfo=datetime.timezone.utc), verbose_name='Meeting Date and Time'),
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 12, 53, 38, 937100, tzinfo=datetime.timezone.utc), verbose_name='Meeting Date and Time'),
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 12, 44, 36, 346413, tzinfo=datetime.timezone.utc), verbose_name='Meeting Date and Time'),
        ),
    ]
