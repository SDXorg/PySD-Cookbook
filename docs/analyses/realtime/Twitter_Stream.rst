
Feeding models with realtime streaming data
===========================================

In this example, we'll construct a very simple model of the number of
posts relating to a given topic on twitter timelines around the world.
We'll feed the model with live streaming data from the twitter API and
run the model in real time.

Ingredients
-----------

Libraries
^^^^^^^^^

In addition to our standard data analytics stack, we'll take advantage
of the `tweepy <http://tweepy.readthedocs.org/>`__ library for
interacting with the twitter API, the standard python library for
dealing with `JSON <https://docs.python.org/2/library/json.html>`__
objects, and the standard python
`threading <https://docs.python.org/2/library/threading.html>`__
library, to give us access to both the stream and the plots in real
time.

.. code:: python

    %pylab
    import tweepy
    import json
    import pysd
    import threading
    from matplotlib import animation


.. parsed-literal::

    Using matplotlib backend: MacOSX
    Populating the interactive namespace from numpy and matplotlib


Twitter Credentials
^^^^^^^^^^^^^^^^^^^

If you want to execute this recipe, you'll need to `sign up for a
twitter developer account <https://dev.twitter.com/>`__ and create a
file containing your credentials.

Name this file ``_twitter_credentials.py`` and save it in the working
directory. It should contain something similar to:

::

    consumer_key = 'sdjfhkdgjhsk8u09wejne4vdj8j34'
    consumer_secret = 'nvjsdv8wp43nneri'
    access_token = 'vndisoerihosfdbuttonmashingjkfdlasnvei'
    access_token_secret = 'navdjewrjodfjkmorebuttonmashingnjkasdoinv'

We can load these into our environment using the ``import *`` syntax.

.. code:: python

    from _twitter_credentials import *

Model
^^^^^

Our model is a simple delay process. The inflow of the process is the
rate at which twitter users post messages containing our keywords, and
the level decays over time as posts fall out of the top of users
timelines.

We'll explicitly set the timescale in this demo, to show the behavior of
the system in a short timeperiod.

.. code:: python

    model = pysd.read_vensim('../../models/Twitter/Twitter.mdl')
    model.set_components({'displacement_timescale':30})

The Recipe
----------

Listening to twitter
^^^^^^^^^^^^^^^^^^^^

The first thing we'll do is to create a variable that will track the
total number of posts recieved in the last model interation timeperiod.
This counter will be reset after every model timestep.

.. code:: python

    counter = 0

Next, we'll construct a function that will be run whenever a tweet is
recieved from the API. This function will increase the counter value,
and format the tweet to print to the screen.

.. code:: python

    class TweetListener(tweepy.StreamListener):
        def on_data(self, data):
            global counter
            counter += 1
            
            # Twitter returns data in JSON format - we need to decode it first
            decoded = json.loads(data)
    
            # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
            print '@%s: %s\n' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
            return True
    
        def on_error(self, status):
            print status

The tweepy library manages formatting our credentials for the API
request:

.. code:: python

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

Finally we create the object that will parse the twitter stream, and
start it within its own thread.

.. code:: python

    stream = tweepy.Stream(auth, TweetListener())
    
    t = threading.Thread(target=stream.filter, kwargs={'track':['ISDC', 'PySD', 'ISDC15', 'Trump']})
    t.daemon = True
    t.start()

Animation
^^^^^^^^^

First we create a function that will be called at every step in the
integration:

.. code:: python

    #make the animation
    def animate(t):
        global counter
        #run the simulation forward
        time = model.components.t+dt
        model.run({'tweeting':counter}, 
                  return_timestamps=time,
                  return_columns=['tweeting', 'posts_on_timeline'],
                  initial_condition='current',
                  collect=True)
        out = model.get_record()
        ax.plot(out['tweeting'], 'r', label='Tweeting')
        ax.plot(out['posts_on_timeline'], 'b', label='Posts on Timeline')
        counter = 0


.. parsed-literal::

    @alisonjpotter: RT @queenfeminist: Retweet for Bernie Sanders fav for Hillary Clinton
    
    Ignore and Donald Trump wins
    
    @MrTommyCampbell: RT @swhammerhead: #WhenTrumpIsElected the letter H will be removed from the American lexicon as Trump doesn't pronounce it anyways.  It wil
    
    @JBRichard50: RT @BradThor: "It's impossible for Perry to have stayed gov of TX for so long if he really is the person we saw in those debates." http://t
    
    @AdeboyeOriade: RT @politicususa: President Obama Rips Donald Trump, Mike Huckabee, and The Entire Republican Party http://t.co/krMZwVV1u0 via @politicusus
    
    @1baldeagle77: The one thing that makes me take Donald Trump seriously as a candidate  Rush Limbaugh http://t.co/VxDAyO8xw7 via @voxdotcom
    


Lastly we set the parameters for the animation, set up the figure, reset
the counter (which has been accumulating posts since we ran the first
part of the code) and start the animation.

.. code:: python

    #set the animation parameters
    fps=1
    seconds=60*30
    dt=1./fps    
    
    #set up the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0,seconds)
    title = ax.set_title('Expected Twitter Messages on First Page of Feed')
    ax.set_xlabel('Seconds')
    ax.set_ylabel('Posts, Posts/second')
        
    #reset the counter to start fresh.
    counter=0    
        
    # call the animator.
    animation.FuncAnimation(fig, animate, repeat=False,
                            frames=seconds*fps, interval=1000./fps, 
                            blit=False)


.. parsed-literal::

    @shehelby: RT @ProBirdRights: How can they say me a bird can not be run for Presindent when Donal Trump a giant talking corn can??? #birb2016
    
    @LacrosseUpdate: Hope Hicks flies quietly in the eye of the Trump storm http://t.co/SSUZKcyyiG http://t.co/3MlnhhsEwc
    
    @thedancingqueer: RT @queenfeminist: Retweet for Bernie Sanders fav for Hillary Clinton
    
    Ignore and Donald Trump wins
    
    @BuzzFeedAndrew: "Never a Bush fan," Donald Trump campaigned for H.W. in 1988 held a fundraiser for Jeb in 2002. http://t.co/7S2u6eSyrN
    
    @david_alman: Fucking leftist media spends so much time covering Donald Trump's statements from 20 years ago that it neglects like...anything relevant.
    
    @kcasa7131: RT @pdacosta: #WhenTrumpIsElected, he might appoint himself as Chairman of the Federal Reserve, and begin to issue Trump dollars. http://t.
    
    @presidentrumped: President Trump: Mr Trump is a Gemini this means he is TOTALLY unpredictable! http://t.co/tP5lraAyUH
    
    @MicheleUpdate: Nicolle Wallace: Trump Is 'Doing One Thing Really, Really Well' http://t.co/kLfGNkCqyh
    
    @jjyorktown: RT @ConanOBrien: Im on vacation. Please keep Trump popular while Im gone, I need him in the debates.
    
    @MisaelDiazMLM: .@amazonmex @jcgs68 @amazon Amazon: Dejen de vender los libros de Donald Trump! - Firm la Peti... https://t.co/UMSTq5AxY2 va @Change_M
    
    @StrongerForce: RT @BradThor: "It's impossible for Perry to have stayed gov of TX for so long if he really is the person we saw in those debates." http://t
    
    @cheyannebiancab: RT @bigmacher: #WhenTrumpIsElected everyone will get a Trump action figure that will buy all your play houses &amp; then goes bankrupt. http://
    
    @BigEers: RT @Mediaite: Chris Christie Will No Longer Comment Publicly on Donald Trump http://t.co/UrfQEfGklZ (AUDIO) http://t.co/5fEw69cvM7
    
    @_miramira93: RT @SockHimBopHer: Bill Cosby's legacy is dead.. Donald Trump can possibly be the president.. The Klan is traveling like an AAU team.. And 
    
    @paigekathstev: RT @ConanOBrien: Im on vacation. Please keep Trump popular while Im gone, I need him in the debates.
    
    @BMLewis2: RT @GStuedler: I cant see it happening, but in the slim chance it doesa Donald Trump nomination would mean they have completely given up.
    
    @DebndanfarrDeb: Donald Trump Surges to Lead in NH GOP Presidential Poll, Erases Another's Iowa Lead - The Political Insider http://t.co/3exB1TrjPJ via
    




.. parsed-literal::

    <matplotlib.animation.FuncAnimation at 0x114fc0c90>



