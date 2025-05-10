from rest_framework import generics, views, response, status
from django.db.models import Count, aggregates, Avg 
from movies.models import Movie
from movies.serializers import MovieModelSerializer, MovieStatsSerializer, MovieListDetailSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import  GlobalDefaultPermission
from reviews.models import Review

class MovieCreateListview(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    #serializer_class = MovieModelSerializer

    #sobescrevendo o metodo
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
    queryset = Movie.objects.all()
   
    #sobescrevendo o metodo
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MovieStatsView(views.APIView): #apis mais simples para customizar os metodos get, post, put, delete.
    permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request): #self é a instandia da classe MovieStats. nela customizo outras funções
        total_movies = self.queryset.count() #reutilizando a consulta
        movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        total_reviews = Review.objects.count()
        average_stars = Review.objects.aggregate(avg_stars=Avg('stars'))['avg_stars']

        data={
                'total_movies': total_movies,
                'movies_by_genre': movies_by_genre,
                'total_reviews': total_reviews,
                'average_stars': average_stars,
        }
        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK,
            )






