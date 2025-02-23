from django.shortcuts import render, redirect, get_object_or_404 #type: ignore
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

# def AddBlog(request):
#     if request.method == "POST":
#         description = request.POST.get('description')
#         blogimage = request.FILES.get('image')

#         if blogimage: 
#             image_path = os.path.join(settings.MEDIA_ROOT, "technology", blogimage.name)
#             os.makedirs(os.path.dirname(image_path), exist_ok=True)

#             with open(image_path, 'wb') as f:
#                 for chunk in blogimage.chunks():
#                     f.write(chunk)

#             image_relative_path = "/avadhblog/static/images/blog/" + blogimage.name

#         query = """
#             INSERT INTO blog (image, details)
#             VALUES (%s, %s)
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query, [
#                 image_relative_path,
#                 description
#             ])
#         return render(request, 'avadhblog/addBlog.html', {'message': 'Blog Added Successfully...'})
#     return render(request, 'avadhblog/addBlog.html')

def AddBlog(request):
    if request.method == "POST":
        description = request.POST.get('description')
        blogimage = request.FILES.get('image')
        image_relative_path = ""  # Default empty value if no image is provided

        if blogimage:
            # Build the physical file path in the folder 'blog' under MEDIA_ROOT
            image_path = os.path.join(settings.MEDIA_ROOT, "blog", blogimage.name)
            # Ensure the folder exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Write the file in binary mode
            with open(image_path, 'wb') as f:
                for chunk in blogimage.chunks():
                    f.write(chunk)
            
            # Build the relative URL path to match the stored file location as expected in your templates
            image_relative_path = "/avadhblog/static/images/blog/" + blogimage.name

        # Prepare the raw SQL query to insert the blog record
        query = """
            INSERT INTO blog (image, details)
            VALUES (%s, %s)
        """
        # Execute the query with the provided parameters
        with connection.cursor() as cursor:
            cursor.execute(query, [image_relative_path, description])
        
        return render(request, 'avadhblog/addBlog.html', {'message': 'Blog Added Successfully...'})
    
    return render(request, 'avadhblog/addBlog.html')

def DeleteBlog(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blog WHERE id = %s", [id])       
    return redirect('viewblog')

def UpdateBlog(request, id):
    if request.method == "POST":
        new_details = request.POST["details"]
        blogimage = request.FILES.get("image")
        image_relative_path = None

        if blogimage:
            directory = settings.MEDIA_ROOT + "/blog"
            image_path = directory + "/" + blogimage.name
            
            if not os.path.exists(directory):
                os.mkdir(directory)

            f = open(image_path, "wb")
            for chunk in blogimage.chunks():
                f.write(chunk)
            f.close()

            image_relative_path = "/avadhblog/static/images/blog/" + blogimage.name

        cursor = connection.cursor()
        if image_relative_path:
            sql = "UPDATE blog SET image=%s, details=%s WHERE id=%s"
            params = [image_relative_path, new_details, id]
        else:
            sql = "UPDATE blog SET details=%s WHERE id=%s"
            params = [new_details, id]

        cursor.execute(sql, params)
        cursor.close()

        return redirect("viewblog")

    cursor = connection.cursor()
    sql = "SELECT id, image, details FROM blog WHERE id=%s"
    cursor.execute(sql, [id])
    blog = cursor.fetchone()
    cursor.close()

    if blog:
        blog_data = {
            "id": blog[0],
            "images": blog[1],
            "details": blog[2],
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