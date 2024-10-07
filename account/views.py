
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import  UserSerializer, LoginSerializer, UpdateUserSerializer, StaffSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import User, Staff, Phone, Address, Counter, Trustedclient, Project, Testimonial

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
import random
import os

from django.core.mail import send_mail

from rest_framework import serializers

from drf_yasg.utils import swagger_auto_schema


class sendmailserializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    message = serializers.CharField()

class sendEmail(generics.GenericAPIView):
    serializer_class = sendmailserializer
    
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        name = request.data['name']
        message = request.data['message']
            
        if(email == "" or name == "" or message == ""):
            return Response(data="all fields are required", status=400)
        
        else:
            
        
            send_mail(
                subject="enquiry message",
                message=f"{message}\nreply_to:\n{request.data['email']}",
                from_email=request.data['email'],
                recipient_list=['dejaneesconceptslimited@gmail.com']
            )
            
            return Response(data="success", status=200)
            
        

class login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    
    def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(email = request.data['identity']).first()
            
        if user is not None:
            if user.check_password(request.data['password']) and user.is_active == True:
                refresh = RefreshToken.for_user(user)
                data = {
                    'id': getattr(user, "id"),
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(data=data, status=200)
            
            elif user.check_password(request.data['password']) and user.is_active == False:
                return Response(data="account not activated", status=400)
            else:
                return Response(data="invalid credentials", status=400)
        
        else:
            return Response(data="invalid credentials", status=400)
        
        

class signup(generics.GenericAPIView):
    
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            
            return Response(data=serializer.data, status=201)
        
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class verifyserializer(serializers.Serializer):
    email = serializers.EmailField()


class verifyemail(generics.GenericAPIView):
    serializer_class = verifyserializer
    
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email = request.data['email']).first()
        
        code = ""
        
        for _ in range(0,6):
            i = random.randrange(0,9)
            code += str(i)
            
        user.activation_code = code
        user.save()
        
        
        html_message = render_to_string("forgetpassword.html", context={"code": code})
        text_content = strip_tags(html_message)
        
        data = EmailMultiAlternatives(
        subject = f"Forget Password",
        body = text_content,
        from_email = settings.EMAIL_HOST_USER,
        to = [getattr(user, "email")]
            
        )
    
        
        data.attach_alternative(html_message, "text/html")
        data.send()
    
        
        return Response(getattr(user, "email"), status=200)
    
   
class verifyotpserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class verifyotp(generics.GenericAPIView):
    
    serializer_class = verifyotpserializer
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(email = request.data['email'], activation_code = request.data['otp'])
       
        return Response("success", status=200)
   
    
  
@api_view(['POST'])
def changepassword(request):
    
    try:
        user = User.objects.get(email = request.data['email'])

        user.set_password(request.data['password'])
        
        user.save()
       
        return Response("success", status=200)
    
    except BaseException as e:
        return Response(str(e), status=400)
  
permisson_classes = [IsAdminUser]  
@api_view(['POST'])
def createstaff(request):
    
    
    try:
        
        user = request.user
        
        request.data._mutable = True
       
       
        if user.is_authenticated == False:
            return Response(data={"authentication":"authentication failed"}, status=400)
        
        
        else:
            
            request.data['uid'] = user.id
               
            serializer = StaffSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                
                return Response(data=serializer.data, status=201)
            
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            
        
    except BaseException as e:
        return Response(data=str(e), status=400)

  
permisson_classes = [IsAuthenticated]  
@api_view(['GET'])
def storeStaff(request):
    
    
    try:
        
        user = request.user
        
        
        if user.is_authenticated == False:
            return Response(data={"authentication":"authentication failed"}, status=400)
        
         
        else:
            
            
            staffs = Staff.objects.all()
                      
                
            serializer = StaffSerializer(staffs, many = True)
                
            return Response(data=serializer.data, status=201)
                    
    except BaseException as e:
        return Response(data=str(e), status=400)
    
    
  

@api_view(['GET'])
def AllStaff(request):
    
    
    try:
        
       
        staffs = Staff.objects.all()
                      
                
        serializer = StaffSerializer(staffs, many = True)
                
        return Response(data=serializer.data, status=201)
                    
    except BaseException as e:
        return Response(data=str(e), status=400)
    
    
  
@api_view(['GET'])
def verify_user(request, id, code):
    try:
        user = User.objects.get(id = id, activation_code = code)
    
        if user is not None:
            user.is_active = True
            user.save()
            return Response(data="success", status=status.HTTP_202_ACCEPTED)
        elif user.is_active == True:
            
            return Response(data={"error": "user active"}, status=status.HTTP_400_BAD_REQUEST)
    except BaseException as e:
        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
  
permisson_classes = [IsAuthenticated]
@api_view(['GET'])
def getuser(request):
    user = request.user
   
    try:
        user = User.objects.get(id = user.id)
        
        
        serializer = UserSerializer(user)
            
        return Response(data=serializer.data, status=200)
        
        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]
@api_view(['GET'])
def getuserbyid(request, id):
    user = request.user
   
    try:
        
        if user.is_authenticated == False and user.is_superuser == False:
            return Response(data="invalid credentials", status=400)
        
        else:
            
            user = Staff.objects.get(id = id)
            
           
            
            serializer = StaffSerializer(user)
                
            return Response(data=serializer.data, status=200)
        
        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
 
permisson_classes = [IsAdminUser]   
@api_view(['PATCH'])
def updateuser(request, pk):
    
    try:
        user = Staff.objects.get(id = pk)
        
        serializer = UpdateUserSerializer(instance=user, data= request.data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
        
            return Response(data=serializer.data, status=200)
        
        else:
            return Response(data=serializer.errors, status=400)
        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['DELETE'])
def deleteuser(request, pk):
    
    try:
        staff = Staff.objects.get(id = pk)
        
        user = User.objects.get(id = staff.user.id)
        
        os.remove(f"media/{user.photo}")
        
        
        staff.delete()
        
        user.delete()
       
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['POST'])
def addphone(request):
    
    try:
        
        
       
        chk = Phone.objects.filter(phone = request.data['phone']).first()
        
        if chk is not None:
            chk.phone = request.data['phone']
            
            chk.save()
            return Response(data="success", status=200)
            
        else:
            Phone.objects.create(phone = request.data['phone'])
        
            return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
  
@api_view(['GET'])
def getphone(request):
    
    try:
        
        
       
        phone = Phone.objects.first()
        
        
        
        return Response(data=str(phone), status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

    
permisson_classes = [IsAdminUser]   
@api_view(['POST'])
def addaddress(request):
    
    try:
        
        
       
        chk = Address.objects.filter(city = request.data['city'], street = request.data['street']).first()
        
        if chk is not None:
            chk.street = request.data['street']
            chk.city = request.data['city']
            
            chk.save()
            return Response(data="success", status=200)
            
        else:
            Address.objects.create(street = request.data['street'], city = request.data['city'])
        
            return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
  
@api_view(['GET'])
def getaddress(request):
    
    try:
        
        
       
        address = Address.objects.first()
        
        
        
        return Response(data={"city": address.city, "street": address.street}, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)


permisson_classes = [IsAdminUser]   
@api_view(['POST'])
def addcounter(request):
    
    try:
        
        
       
       
        chk = Counter.objects.filter(title = request.data['title']).first()
        
        print(chk)
        
        if chk is not None:
            
            return Response(data="title already exists", status=200)
            
        else:
            Counter.objects.create(title = request.data['title'], number = request.data['number'])
        
            return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

class counterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Counter
  
@api_view(['GET'])
def getcounter(request):
    
    try:
        
        
       
        counter = Counter.objects.all()
        
        serializer = counterSerializer(counter, many = True)
        
        
        return Response(data=serializer.data, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)



    
permisson_classes = [IsAdminUser]   
@api_view(['DELETE'])
def deletecounter(request, pk):
    
    try:
        print(pk)
        counter = Counter.objects.get(id = pk)
        
        
        counter.delete()
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    

permisson_classes = [IsAdminUser]   
@api_view(['POST'])
def addclient(request):
    
    try:
        
        
       
        Trustedclient.objects.create(image = request.data['image'])
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['DELETE'])
def deleteclient(request, id):
    
    try:
        
        
       
        client =  Trustedclient.objects.get(id = id)
        
        
        os.remove(f"media/{client.image}")
        
        client.delete()
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

class TrustedClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Trustedclient
  
@api_view(['GET'])
def gettrustedclient(request):
    
    try:
        
        
       
        tc = Trustedclient.objects.all()
        
        serializer = TrustedClientSerializer(tc, many = True)
        
        
        return Response(data=serializer.data, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)


@api_view(['POST'])
def addtestimonial(request):
    
    try:
        
        if request.data['name'] == "" or request.data['position'] == "" or request.data['text'] == "":
           return Response(data="all fields are required", status=400)
        
        else:
                
            Testimonial.objects.create(
                name = request.data['name'],
                position = request.data['position'],
                text = request.data['text'],
            )
            
            return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['PATCH'])
def updatetestimonial(request, id):
    
    try:
        
        print(id)
        print(request.data)
        
        
       
        tt =  Testimonial.objects.get(id = id)
        
        tt.active = request.data['active']
        
        tt.save()
        

        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['DELETE'])
def deletetestimonia(request, id):
    
    try:
        
        
       
        tt =  Testimonial.objects.get(id = id)
        
        tt.delete()

        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Testimonial
  
@api_view(['GET'])
def gettestimonial(request):
    
    try:
        
        
       
        tc = Testimonial.objects.filter(active = True).all()
        
        serializer = TestimonialSerializer(tc, many = True)
        
        
        return Response(data=serializer.data, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['GET'])
def gettestimonialAdmin(request):
    
    try:
        
        if request.user.is_superuser == False:
            return Response(data="authentication failed", status=400)
       
        tc = Testimonial.objects.all()
        
        serializer = TestimonialSerializer(tc, many = True)
        
        
        return Response(data=serializer.data, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

permisson_classes = [IsAdminUser]   
@api_view(['POST'])
def addproject(request):
    
    try:
        
        
       
        Project.objects.create(image = request.data['image'], company = request.data['company'])
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)
    
permisson_classes = [IsAdminUser]   
@api_view(['DELETE'])
def deleteproject(request, id):
    
    try:
        
        
       
        project =  Project.objects.get(id = id)
        
        
        os.remove(f"media/{project.image}")
        
        project.delete()
        
        return Response(data="success", status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project
  
@api_view(['GET'])
def getproject(request):
    
    try:
        
        
       
        pj = Project.objects.all()
        
        serializer = ProjectSerializer(pj, many = True)
        
        
        return Response(data=serializer.data, status=200)

        
    except BaseException as e:
        return Response(data=str(e), status=400)



