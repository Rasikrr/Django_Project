# Generated by Django 4.2.3 on 2023-07-10 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_likecommentpost_delete_likepost_alter_post_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LikeCommentPost',
            new_name='LikePost',
        ),
    ]