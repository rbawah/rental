from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from mainpages.models import Building, Unit, Home, HomeType, LocationCity
from api.serializers import HomeSerializer, BuildingSerializer, UnitSerializer, UserSerializer
from api.permissions import IsManagerOrReadOnly

from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list', request=request, format=format),
        'buildings': reverse('building_list', request=request, format=format),
        'homes': reverse('home_list', request=request, format=format),
        'units': reverse('unit_list', request=request, format=format),
    })


class HomeListAPIView(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class UnitListAPIView(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


#class HomeDetailApiView(generics.RetrieveUpdateDestroyAPIView):
class HomeDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

"""
class UnitsInBuildingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    #renderer_classes = [JSONRenderer]

    def get(self, request, slug):
        building = Building.objects.get(slug=slug)
        unit_list = Unit.objects.filter(
            building__name=building
        )
        units_list = [unit for unit in unit_list]
        #ctx = {'units_list': units_list, 'building':building}
        return Response(units_list)
"""


class HomeListAPI(APIView):

    """
    List all homes, or create a new home.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]
    def get(self, request, format=None):
        homes = Home.objects.all()
        serializer = HomeSerializer(homes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeDetailAPI(APIView):

    """
    Retrieve, update or delete a home instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]

    def get_object(self, pk):
        try:
            return Home.objects.get(pk=pk)
        except Home.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        home = self.get_object(pk)
        serializer = HomeSerializer(home)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        home = self.get_object(pk)
        serializer = HomeSerializer(home, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        home = self.get_object(pk)
        home.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnitListAPI(APIView):
    """
    List all units, or create a new unit.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]
                            
    def get(self, request, format=None):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitDetailAPI(APIView):
    """
    Retrieve, update or delete a unit instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]

    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        unit = self.get_object(pk)

        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        unit = self.get_object(pk)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildingListAPI(APIView):
    """
    List all buildings, or create a new building.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]

    def get(self, request, format=None):
        buildings = Building.objects.all()
        serializer_context = {'request': request,}
        #serializer = UnitSerializer(unit, context=serializer_context)
        serializer = BuildingSerializer(buildings, many=True, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class BuildingDetailAPI(APIView):
    """
    Retrieve, update or delete a building instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsManagerOrReadOnly,
                            ]

    def get_object(self, pk):
        try:
            return Building.objects.get(pk=pk)
        except Building.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        building = self.get_object(pk)
        serializer = BuildingSerializer(building)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        building = self.get_object(pk)
        serializer = BuildingSerializer(building, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        building = self.get_object(pk)
        building.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

