# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 17:02
from __future__ import unicode_literals

from django.db import migrations


def set_submission_revisions(apps, schema_editor):
    units = apps.get_model("pootle_store.Unit").objects.all()
    submissions = apps.get_model("pootle_statistics.Submission").objects

    # if unit has 0 revision then so does all of its submissions
    submissions.filter(unit__in=units.filter(revision=0)).update(revision=0)
    
    revisions = units.filter(revision__gt=0).exclude(submission__isnull=True).values_list("revision", flat=True).distinct()
    for revision in revisions.iterator():
        seen_units = set()
        subs = set()
        # find the latest submission for each unit at the given revision
        matched_subs = submissions.filter(
            unit__revision=revision).order_by("-creation_time", "-id").values_list("unit", "id")
        for unit, sub in matched_subs.iterator():
            if unit in seen_units:
                continue
            seen_units.add(unit)
            subs.add(sub)
        submissions.filter(id__in=subs).update(revision=revision)


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_statistics', '0007_submission_revision'),
    ]

    operations = [
        migrations.RunPython(set_submission_revisions),
    ]
