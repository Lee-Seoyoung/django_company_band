import re
from django.conf import settings  
from django.db import models
from django.urls import reverse 

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


# user
# -> Post.object.filter(author=user)
# -> user.post_set.all()

class Post(BaseModel): 
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set',
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="board/post/%Y/%m/%d", blank=True, null=True)
    text = models.CharField(max_length=1000)
    tag_set = models.ManyToManyField('Tag', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                            related_name='like_post_set')

    def __str__(self):
        return self.text 
    
    # @property
    # def author_name(self):
    #     return f"{self.author.first_name} {self.author.last_name}"
    
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.text)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
    
    def get_absolute_url(self):
        return reverse("board:post_detail", args={self.pk})

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()
    
    class Meta:
        ordering = ['-id']

class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']
    


# class Comment(BaseModel):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     message = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class LikeUser(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

