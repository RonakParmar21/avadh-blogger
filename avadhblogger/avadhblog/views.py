from django.shortcuts import render, redirect #type: ignore
from django.db import connection #type: ignore
from django.conf import settings #type: ignore
import os

# Create your views here.
def Index(request):
    
    return render(request, 'client/index.html')

def About(request):
    return render(request, 'client/about.html')

def Article(request):
    return render(request, 'client/article.html')

def Category(request):
    return render(request, 'client/category.html')

def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", [email, password])
            user = cursor.fetchone()
            if user:
                request.session['user_email'] = email 
                return render(request, 'client/login.html', {'message':'user found'})
            else:
                return render(request, 'client/login.html', {'message':'user not found'})
    return render(request, 'client/login.html')

def Registration(request):
    if 'user_email' in request.session:
        return redirect('home')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO user(name, email, mobile, password) VALUES('"+name+"', '"+email+"', '"+mobile+"', '"+password+"')")
                
            return render(request, 'client/registration.html', {'message': 'Registration Success'})
        else:
            return render(request, 'client/registration.html', {'message': 'Both password are not match'})

    return render(request, 'client/registration.html')

def AdminDashborad(request):
    if 'admin_email' not in request.session:
        return redirect('adminlogin')
    return render(request, 'avadhblog/dashboard.html')

def AdminLogin(request):
    if request.method == "POST":
        email = request.POST.get('adminemail')
        password = request.POST.get('adminpassword')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM avadhadmin WHERE email = %s AND password = %s", [email, password])
            user = cursor.fetchone()
        if user:
            request.session['admin_email'] = email 
            return render(request, 'avadhblog/dashboard.html')
        else:
            return render(request, 'avadhblog/login.html', {'message':'user not found'})
    return render(request, 'avadhblog/login.html')

def AddBlog(request):
    if request.method == "POST":
        description = request.POST.get('description')
        blogimage = request.FILES.get('image')

        if blogimage:
            image_path = os.path.join(settings.MEDIA_ROOT, "blog", blogimage.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            with open(image_path, 'wb') as f:
                for chunk in blogimage.chunks():
                    f.write(chunk)

            image_relative_path = f'/avadhblog/static/images/blog/{blogimage.name}'

        query = """
            INSERT INTO blog (image, details)
            VALUES (%s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [
                image_relative_path,
                description
            ])
        return render(request, 'avadhblog/addBlog.html', {'success': True})
    return render(request, 'avadhblog/addBlog.html')

def DeleteBlog(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blog WHERE id = %s", [id])       
    return redirect('viewblog')
   
def UpdateBlog(request, id):
    if request.method == "POST":
        new_details = request.POST["details"]
        blogimage = request.POST["image"]  # Assuming image URL or file path is stored

        if blogimage:
            image_path = os.path.join(settings.MEDIA_ROOT, "blog", blogimage.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            with open(image_path, 'wb') as f:
                for chunk in blogimage.chunks():
                    f.write(chunk)

            image_relative_path = f'/avadhblog/static/images/blog/{blogimage.name}'


        with connection.cursor() as cursor:
            cursor.execute("UPDATE blog SET image=%s, details=%s WHERE id=%s", [image_relative_path, new_details, id])

        return redirect("viewblog")  # Redirect to home after update

    # Fetch current data
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM blog WHERE id=%s", [id])
        blog = cursor.fetchone()  # Get a single record

    if blog:
        blog_data = {
            "id": blog[0],
            "details": blog[2],
            "images": blog[1],
        }
        return render(request, "avadhblog/updateblog.html", {"blog": blog_data})
    else:
        return render(request, "avadhblog/updateblog.html", {"error": "Blog not found"})
    
def ViewBlog(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from blog')
        blog = cursor.fetchall()

        blog_list = [
            {
                'id': row[0],
                'details': row[2],
                'images': row[1],
            } for row in blog
        ]
    return render(request, 'avadhblog/viewblogs.html', {'blogs':blog_list})

# def AdminLogin(request):
#     if request.method == "POST":
#         email = request.POST.get('adminemail')
#         password = request.POST.get('adminpassword')

#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", [email, password])
#             user = cursor.fetchone()
#             if user:
#                 request.session['adminEmail'] = email 
#                 return render(request, 'avadhblog/dashboard.html')
#             else:
#                 return render(request, 'avadhblog/login.html', {'message':'user not found'})
#     return render(request, 'avadhblog/login.html')