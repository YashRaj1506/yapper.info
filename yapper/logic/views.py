from django.shortcuts import render, redirect
from calc.yapper import yapper_score, clean_tweets
from calc.main import extract_tweets

def home(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        result = extract_tweets(f"https://x.com/{username}")
        
        # Extract tweets and profile pic URL from the result
        tweets = result["tweets"]
        profile_pic_url = result["profile_pic_url"]
        
        cleaned_tweets = clean_tweets(tweets)
        score = yapper_score(cleaned_tweets)
        
        # Add the data to the context to display in the template
        context = {
            'username': username,
            'score': score,
            'profile_pic_url': profile_pic_url
        }
        
        print(f"Username: {username}")
        print(f"Score: {score}")
        print(f"Profile picture URL: {profile_pic_url}")

        request.session['context'] = {
            'username': username,
            'score': score,
            'profile_pic_url': profile_pic_url
        }

        return redirect('cardpage')

    return render(request, 'home.html', context)


def card(request):

    context = request.session.get('context', {})

    return render(request, 'card.html', context)
    
