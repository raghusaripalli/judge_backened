from .views import *

######################### USERS LISTS #########################################
class NestedUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = NestedUserSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]

class NestedUserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = NestedUserSerializer

    permission_classes = [IsAuthenticated,OwnObjectPermission]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]

class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated,IsOwnerOrReadOnly]

############################ PROFILE #################
class ProfileDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated,OwnObjectPermission]
    def get_object(self,username):
        try:
            return Profile.objects.get(user=username)
        except Exception as ex:
            profile = Profile.objects.create(user=username)
            profile.save()
            return profile

    def get(self, request,format=None):
        profile = self.get_object(request.user)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request,format=None):
        profile = self.get_object(request.user)
        serializer = ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        profile = self.get_object(request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)