from rest_framework.views import APIView
# from rest_framework.response import Response

class CodeAuthView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.hook(request)
    
    def hook(self, request):
        print(f"[HOOK] API accessed by: {request.user} at {request.path}")