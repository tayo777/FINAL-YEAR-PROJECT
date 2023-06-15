from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import models
import spacy
from .models import AmazonProduct
from .models import eBayProduct
from .models import UserPreference
from .scraper import scrape_amazon
from .scraper import scrape_ebay
# Create your views here.
nlp = spacy.load("en_core_web_sm")

def home(request):
    return render(request, 'loginpage/index.html')

def welcome(request):
    
    if request.user.is_authenticated:
        # Get the user's id
        id = request.user.id
    else:
        # Redirect the user to the login page
        return redirect('signin')

    
    recommendations = collaborative_filtering(id)
    return render(request, 'loginpage/index1.html', {'recommendations': recommendations}, {'id': id})

def signup(request): 
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')
        
    return render(request, 'loginpage/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password= password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "loginpage/index1.html", {'fname': fname})
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('welcome')
    return render(request, 'loginpage/signin.html')

def signout(request):
    pass

def signout_user(request):
    return render(request, 'loginpage/index.html')

def namesearch(request):
    if request.method == 'GET':
        query = request.GET.get('query')  
        if query:
            products = scrape_amazon(query)
            products1 = scrape_ebay(query)
            user = request.user
            if user.is_authenticated:
                for product in products:
                    UserPreference.objects.update_or_create(
                        user=user,
                        product=product,
                        defaults={'preference_count': models.F('preference_count') + 1}
                    )
            return render(request, 'loginpage/search_results.html', {'products': products, 'products1': products1})
    return render(request, 'loginpage/namesearch.html')

def descsearch(request):
    if request.method == 'GET':
        query = request.GET.get('query')  
        if query:
            nlp = spacy.load('en_core_web_sm')

            
            doc = nlp(query)

            # Extract named entities
            named_entities = [(ent.text, ent.label_) for ent in doc.ents]

            final_query = generate_final_query(named_entities, query)

            amazon_products = scrape_amazon(final_query)
            ebay_products = scrape_ebay(final_query)
            user = request.user
            if user.is_authenticated:
                for product in amazon_products + ebay_products:
                    UserPreference.objects.update_or_create(
                        user=user,
                        product=product,
                        defaults={'preference_count': models.F('preference_count') + 1}
                    )

            # Pass the scraped data to the template
            return render(request, 'loginpage/search_results.html', {'amazon_products': amazon_products, 'ebay_products': ebay_products, 'final_query': final_query})
        return render(request, 'loginpage/descsearch.html')

def search_results(request):
    if request.method == 'GET':
        # Retrieve the necessary data for rendering the search results page
        products = AmazonProduct.objects.all()
        products1 = eBayProduct.objects.all()
        return render(request, 'loginpage/search_results.html', {'products': products, 'products1': products1})

    return redirect('namesearch')  

def generate_final_query(named_entities, original_query):
    relevant_entities = [ne[0] for ne in named_entities if ne[1] in ['PRODUCT', 'ORG']]  # Filter relevant entities (e.g., product or organization names)
    final_query = ' '.join(relevant_entities) + ' ' + original_query
    return final_query


    

def collaborative_filtering(user):
    # Retrieve top-rated products based on preference_count
    top_products = UserPreference.objects.filter(user=user).order_by('-preference_count')[:10]
    recommendations = [p.product for p in top_products]
    return recommendations
