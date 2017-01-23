# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-25 10:19
from __future__ import unicode_literals

from django.db import connection, migrations, models

def update_epic_status(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    project_ids = Project.objects.filter(default_epic_status__isnull=True).values_list("id", flat=True)
    if not project_ids:
        return

    values_sql = []
    for project_id in project_ids:
        values_sql.append("('New', 'new', 1, false, '#999999', {project_id})".format(project_id=project_id))
        values_sql.append("('Ready', 'ready', 2, false, '#ff8a84', {project_id})".format(project_id=project_id))
        values_sql.append("('In progress', 'in-progress', 3, false, '#ff9900', {project_id})".format(project_id=project_id))
        values_sql.append("('Ready for test', 'ready-for-test', 4, false, '#fcc000', {project_id})".format(project_id=project_id))
        values_sql.append("('Done', 'done', 5, true, '#669900', {project_id})".format(project_id=project_id))

    sql = """
        INSERT INTO projects_epicstatus (name, slug, "order", is_closed, color, project_id)
        VALUES
        {values};
    """.format(values=','.join(values_sql))
    cursor = connection.cursor()
    cursor.execute(sql)


def update_default_epic_status(apps, schema_editor):
    sql = """
        UPDATE projects_project
        SET default_epic_status_id = projects_epicstatus.id
        FROM projects_epicstatus
        WHERE
        	projects_project.default_epic_status_id IS NULL
        	AND
        	projects_epicstatus.order = 1
        	AND
        	projects_epicstatus.project_id = projects_project.id;
    """
    cursor = connection.cursor()
    cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0051_auto_20160729_0802'),
    ]

    operations = [
        migrations.RunPython(update_epic_status),
        migrations.RunPython(update_default_epic_status)
    ]
