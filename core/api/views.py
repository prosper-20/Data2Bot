from rest_framework import status
from rest_framework.response  import Response
from .serializers import ItemSerializer, RegistrationSerializer, UserPropertiesSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from core.models import Item, Order
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@api_view(["GET"])
def api_item_list_view(request):
    try:
        items = Item.objects.all()
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["Response"] = "Successfully registered a new user"
            data["email"] = user.email
            data["username"] = user.username
            token = Token.objects.get(user=user).key
            data["token"] = token
        else:
            data = serializer.errors
        return Response(data)



class ItemListView(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

class ItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "slug"


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserPropertiesSerializer(user)
        return Response(serializer.data)



@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def update_user_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = UserPropertiesSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            updated_user = serializer.save()
            data["response"] = "Account update success"
            data["username"] = updated_user.username
            data["email"] = updated_user.email
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def api_order_list_view(request):
    try:
        orders = Order.objects.filter(user=request.user)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

        


