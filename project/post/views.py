from django.shortcuts import render

# Create your views here.
class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PostView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    
    def post(self, request, *args, **kwargs):
        
        print(request.data)
        try:
            request.data._mutable = True
        except AttributeError:
            pass
        request.data.update({"post_owner" : Profile.objects.get(user = request.user).id,
                             "parent_post": None})
        return super().post(request, *args, **kwargs)

   
class SinglePostView(RetrieveDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    queryset = Post.objects.all()
    
    
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post,id = kwargs['pk'])
        if not post.post_owner.user == self.request.user:
            return Response({"detail": "You are not allowed to perform this action"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request, *args, **kwargs)


class PostReactionView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostReactionSerializer
    
    
    def get_queryset(self):
        
        post = self.request.GET.get('post')
        return PostReaction.objects.filter(post = post)
    
    def post(self, request, *args, **kwargs):
        request.data.update({"reacted_by" : Profile.objects.get(user = request.user).id})
        return super().post(request, *args, **kwargs)
    

class SinglePostReactionView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = SinglePostReactionSerializer
    
    queryset = PostReaction.objects.all()
    
    def patch(self, request, *args, **kwargs):
        
        post_reaction = get_object_or_404(PostReaction,id = kwargs['pk'])
        if not post_reaction.reacted_by.user == self.request.user:
            return Response({"detail": "You are not allowed to perform this action"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
            
        return super().patch(request, *args, **kwargs)
    
    
    def delete(self, request, *args, **kwargs):
        post_reaction = get_object_or_404(PostReaction,id = kwargs['pk'])
        if not post_reaction.reacted_by.user == self.request.user:
            return Response({"detail": "You are not allowed to perform this action"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request, *args, **kwargs)
    