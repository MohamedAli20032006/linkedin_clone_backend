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
    
    
    
class PostImages(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/images/')
    
    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Post Images'
 

class ReactionType(models.Model):
    type = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Reaction Type'
        verbose_name_plural = 'Reaction Types'
        
    def __str__(self):
        return f"{self.type}"
    

class PostReaction(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reacted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post_reactions")
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Post Reaction'
        verbose_name_plural = 'Post Reactions'
        unique_together = (('post', 'reacted_by'))
        
    def __str__(self):
        return f"{self.reacted_by.full_name} --> {self.reaction_type} --> ({self.post})"

