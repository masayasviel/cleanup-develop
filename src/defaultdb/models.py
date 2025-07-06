from django.db import models

# Create your models here.

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='group_name_uniq'),
        ]
        db_table = "group"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256, unique=True)

    class Meta:
        db_table = "user"


class GroupUserRelation(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "group_user_relation"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    is_official = models.BooleanField(default=False)

    class Meta:
        db_table = "tag"


class UserTagRelation(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tag'], name='user_and_tag_uniq'),
        ]
        db_table = "user_tag_relation"


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    article_path = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='article_title_and_user_uniq'),
        ]
        db_table = "article"


class ArticleTagRelation(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'tag'], name='article_and_tag_uniq'),
        ]
        db_table = "article_tag_relation"


class CycleRelationA(models.Model):
    id = models.AutoField(primary_key=True)
    cycle_relation_b = models.ForeignKey("CycleRelationB", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "cycle_relation_a"


class CycleRelationB(models.Model):
    id = models.AutoField(primary_key=True)
    cycle_relation_a = models.ForeignKey("CycleRelationA", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "cycle_relation_b"
