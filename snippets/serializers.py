from rest_framework import serializers
from snippets.models import Snippet
from comments.serializers import CommentSerializer

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style', 
                  'comments']