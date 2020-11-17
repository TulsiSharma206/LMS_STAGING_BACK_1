https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout


http://localhost:8000/api/register/ 

{
    "username": "admin",
    "email": "admin@bot.com",
    "password": "Password@123"
}


http://localhost:8000/api/login/ 

 (user ka token database mai se remove hone ke baad hi run hogi ya logout karne ke baad Security reason se ek place per login ho gayi toh 2 time login nahi hogi jab tak session delete mahihota)

{
    "username": "admin",
    "password": "Password@123"
}


# Password Change

{
    "old_password": "Old@123",
    "new_password": "New@123"
}


http://localhost:8000/api/password_reset/

#mail send user email

Copy link which is in email, will be similar to /api/password_reset/?token=339e80fe05e5ca9fc74799213f81a093d1f

Now copy that token which comes in email and and post token and password to /api/password_reset/confirm/ api url.
{
    "token":"3339e80fe05e5ca9fc74799213f81a093d1f",
    "password":"Password@123"
}



path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),