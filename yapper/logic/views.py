from django.shortcuts import render, redirect
from calc.yapper import yapper_score, clean_tweets
from calc.main import extract_tweets
# from .models import SiteHit

def home(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        result = extract_tweets(f"https://x.com/{username}")
        
        # Extract tweets and profile pic URL from the result
        tweets = result["tweets"]
        for i in tweets:
            print(i)

        if tweets == []:
            context = {
                'message': 'You are not eligible for a Yapper Card'
            }

            request.session['context'] = {
                'message': 'You are not eligible for a Yapper Card'
            }


            return redirect('cardpage')
        
        profile_pic_url = result["profile_pic_url"]
        
        cleaned_tweets = clean_tweets(tweets)
        score = yapper_score(cleaned_tweets)
        
        # Add the data to the context to display in the template
        context = {
            'message': 'You are eligible for a Yapper Card',
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
            'profile_pic_url': profile_pic_url,
            'message': 'You are eligible for a Yapper Card'
        }

        return redirect('cardpage')

    return render(request, 'home.html', context)


def card(request):

    context = request.session.get('context', {})

    # # Get the total number of site hits
    # total_hits = SiteHit.objects.count()
    # context['total_hits'] = total_hits

    return render(request, 'card.html', context)
    
