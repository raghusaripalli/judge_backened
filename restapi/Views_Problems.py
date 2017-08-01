from .views import *

class ContestProblemsList(CSRFExemptMixin,APIView):

    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]

    def get(self,request,contestid,format=None):
        snippets = Problem.objects.filter(contest_id=contestid)
        serializer = ProblemSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request,contestid, format=None):
        request.data["contest"] = contestid
        print(request.data)
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContestProblemsDetail(CSRFExemptMixin, APIView):

    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]

    def get_object(self, problemid):
        try:
            return Problem.objects.get(pk=problemid)
        except Problem.DoesNotExist:
            raise Http404

    def get(self, request,problemid,contestid, format=None):
        snippet = self.get_object(problemid)
        serializer = ProblemSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, problemid,contestid, format=None):
        snippet = self.get_object(problemid)
        request.data["contest"] = contestid
        serializer = ProblemSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, problemid, format=None):
        snippet = self.get_object(problemid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
