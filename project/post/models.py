from django.db import models

# Create your models here.
class Post(models.Model):
    
    
    parent_post = models.ForeignKey("Post.Post", on_delete=models.CASCADE, blank=True, null = True)
    post_owner = models.ForeignKey(Profile,related_name="created_posts", on_delete=models.CASCADE)
    text = models.TextField()
    
    saved_by = models.ManyToManyField(Profile, related_name="saved_posts", blank = True)
    
    video_linked = models.FileField(upload_to = 'post/videos/', blank = True, null = True,
                                    storage = VideoMediaCloudinaryStorage())
    
    doc_linked  = models.FileField(upload_to = 'post/docs', blank = True, null = True,
                                   storage = RawMediaCloudinaryStorage(),)
    
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    viewed_by = models.ManyToManyField(Profile, related_name="viewed_posts", blank=True)
    reacted_by = models.ManyToManyField(Profile, through='PostReaction', related_name="reacted_posts")
    commented_by = models.ManyToManyField(Profile, through='Comment', related_name="commented_posts")
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.post_owner.full_name}--> Post{self.id}"
    