from rest_framework.views import APIView
from rest_framework.response import Response
from nltk.corpus import wordnet
import nltk
from .serializers import SynonymSerializer, AntonymSerializer

class SynonymView(APIView):
    serializer_class = SynonymSerializer

    def post(self, request, format=None):
        word = request.data.get('word', '')
        synonyms = []
        for syn in wordnet.synsets(word):
            for w in syn.lemmas():
                synonyms.append(w.name())
                if len(synonyms) >=6:
                    break
            if len(synonyms) >= 6:
                break
        serializer = SynonymSerializer(data={'word': word, 'synonyms': synonyms[:6]})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class AntonymView(APIView):
    serializer_class = AntonymSerializer

    def post(self, request, format=None):
        word = request.data.get('word', '')
        antonyms = []
        for ant in wordnet.synsets(word):
            for w in ant.lemmas():
                if w.antonyms():
                    antonyms.append(w.antonyms()[0].name())
                    if len(antonyms) >= 6:
                        break
            if len(antonyms) >= 6:
                   break
        serializer = AntonymSerializer(data={'word': word, 'antonyms': antonyms[:6]})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)