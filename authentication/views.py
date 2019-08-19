# from django.contrib import messages
# from django.contrib.auth import logout, authenticate, login
# from django.shortcuts import redirect, render
# from django.urls import reverse_lazy
# from django.views import generic
# from django.views.generic import TemplateView
# from .forms import RegistrationForm, AccountAuthenticationForm
#
#
# class HomePageView(TemplateView) :
#     template_name = 'home.html'
#
# def SignUp(request) :
#     print('hit function')
#     if request.method == 'POST':
#         print('hit post function')
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             print(email)
#             raw_password = form.cleaned_data.get('password1')
#             print(raw_password)
#             authentication = authenticate(email=email, password=raw_password)
#             print(authentication)
#             login(request, authentication)
#             return redirect('home')
#         else:
#             messages.error(request, "Error")
#             form = RegistrationForm()
#     else :
#         form = RegistrationForm()
#     return render(request, 'registration/signup.html',{'form' : form})
#
#
# def login_view(request) :
#     user = request.user
#     if user.is_authenticated :
#         return redirect("home")
#
#     if request.POST :
#         form = AccountAuthenticationForm(request.POST)
#         if form.is_valid() :
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(email=email, password=password)
#
#             if user :
#                 login(request, user)
#                 return redirect("home")
#         else: # get form
#             form=AccountAuthenticationForm()
#     else :
#         form = AccountAuthenticationForm()
#     # print(form)
#     return render(request, "registration/login.html", {'form' : form})
#
#
# def logout_request(request) :
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("home")
