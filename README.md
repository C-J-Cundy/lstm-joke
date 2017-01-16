# Using an LSTM character-based model to generate jokes from a corpus scraped from reddit.
## Note that due to the source of the jokes (the /r/jokes subreddit), which often has quite offensive jokes, many of the `jokes' that the model generates are quite offensive.

A project inspired by [the openAI requests for research](https://openai.com/requests-for-research/#funnybot), to find a large corpus of jokes and train an LSTM character-based method on it. As far as I could tell, there are no large collections of jokes available on the internet. Using the great databases at pushift.io, I downloaded a dump of all of the top-level posts on Reddit, and used bzgrep to extract the posts which were on [the jokes subreddit](www.reddit.com/r/jokes) , which are almost entirely jokes. I then ran a quick python script to fetch the text of the jokes, and put them into a text file. I did a minimal amount of data cleaning, removing only those posts which had been deleted. Taking the posts which are less than 80 characters long (as we assume that we don't have enough data for a deep learning system to learn how to generate jokes that are many lines long), we have around 100,000 jokes.

I then trained an lstm character-based model on the corpus, adapting the [`city-generation' example](https://github.com/tflearn/tflearn/blob/master/examples/nlp/lstm_generator_cityname.py) in the [TFlearn] (http://tflearn.org/) library. In the future I'm going to pivot to using keras for deep learning applications, but in the meantime I'm using TFlearn. 
I then trained the model on an AWS p2.xlarge instance. I used the [TensorFlow AWS](https://github.com/ritchieng/tensorflow-aws-ami) provided by Ritchie Ng, which was very helpful in spinning up the instance as quickly as possible. I trained the model for around 36 hours, which was the point at which I didn't want to spend any more money on the Amazon servers. To use the trained model yourself:

1. Spin up a p2 from AWS, using the TF AWI
2. Install TFlearn: `sudo pip install git+https://github.com/tflearn/tflearn.git`
3. Clone this repo on the machine
4. Run `lstm_readout.py`.
5. After some time, you should have a sample of the jokes.

A few of the jokes that were created in the output that weren't in the input were (and are relatively non-offensive, compared to the majority of the output):
What do you call a dog with a rubber toe? Roberto
What is a Mexican's favorite number? Juan

These jokes are very closely related to jokes in the input. In particular, there are over 50 repeats of the `What do you call a [noun] with a rubber toe? Roberto' joke. The model has obviously learned that it can replace [noun] with any noun and it will make a valid joke, as it outputs many variations with [noun] taking on various different nouns, such as dog, mexican, man. All the words it substitutes in are valid nouns, and in general the model does use correct grammar at lower temperatures. In fact, it is very impressive that this character-based model is able to learn essentially correct grammar, even if it is nonsensical semantically.

A random sample of the output at varying temperature (which corresponds to how random the output is), with jokes that are in the input (and which the the network has memorised) marked with an *.
NB Some of these may be offensive!

Temperature 1.2:
*I aplaud Mrr joke Space I swallowed love.
*Women that met.  on old one light Now there used to high if you're wo=kers
*Damn girl, are you a window app; Because you can geld lose in about 6 inches.
*What Joke Paydo el Mars Voming Gender Past? Aye faal's quein
*Confucius say I'm really thinking of self-ve mother but Soleo parents.

Temperature 0.8:
*What do you call a gay dinosaur? an African And Ellen Pao falls.
*What do you laugh an Asian? A AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY!
*How many tickles does it take to make an octopus laugh? Ten tickles *
*What's another name for glasses? Cilling Dead tomorrow 
*Where's the best cannibal to eat? The wheelchair..
*was wondering why the guy who could hasly was in the toilet in the sushi.

Temperature 0.4:
*What do you call a cannibal that lost his balls? A polar bear.
*What do you call a black guy with a rubber toe? Fuck
*What do you call a man with a rubber toe? Roberto *
*So a blind man walks into a bar... and a table... and a chair. *
*What do you call a dog with no legs? Ground beef

