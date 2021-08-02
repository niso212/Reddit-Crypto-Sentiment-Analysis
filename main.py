###Connect to Reddit

reddit = praw.Reddit(client_id='dOAvNL7RYQ03gw', client_secret='wDP_owo_3t9BiTCq_msuihboDfE8Ag', user_agent = 'ua', username='cosmonaut49', password='Redditns1!')
print(reddit.user.me()) #QA Connection


###Scrape past 30 submissions in Daily Discussion tagged posts
crypto_reddit = reddit.subreddit('CryptoCurrency')

data = []

cols = ['submission_id', 'post_title', 'date', 'comments']
for post in crypto_reddit.search('Daily Discussion', limit=32):     #adjust limit for number of posts
  comments_all = [] 

  title = post.title
  submission_id = post.id  
  date = post.created_utc

  if time.gmtime(date).tm_mday < 10:
    adj_date = '{0}-0{1}-0{2}'.format(time.gmtime(date).tm_year, time.gmtime(date).tm_mon, time.gmtime(date).tm_mday)
  else:
    adj_date = '{0}-0{1}-{2}'.format(time.gmtime(date).tm_year, time.gmtime(date).tm_mon, time.gmtime(date).tm_mday)
    
  post.comments.replace_more(limit=32)
  [comments_all.append(comments.body) for comments in post.comments.list()]
    
  data.append((submission_id, title, adj_date, comments_all)) 
  
post_df = pd.DataFrame(data, columns=cols).set_index('submission_id')

###Clean the Comments
comments_clean = []

for comment in post_df['comments']:
  comment_list = [str(i) for i in comment]
  #unclean_string = ' , '.join(comment_list)
  #comments_no_emoji = emoji.get_emoji_regexp().sub(u'', unclean_string)
  comments_no_link = [re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', i) for i in comment_list]
  comments_no_break = [re.sub('\n', '', i) for i in comments_no_link]
  #comments_no_gif = re.sub('')
  #word_tokens = word_tokenize(comments_no_link)
  phrase_tokens = [sent_tokenize(i) for i in comments_no_break]
  tokenizer = RegexpTokenizer('\w+|\$[\d.]+|http\S+')
  #regex_tokens = tokenizer.tokenize(comments_no_link)

  comments_clean.append(phrase_tokens)
  
  
post_df['phrase_tokens'] = comments_clean
flat_list = [item for sublist in post_df['phrase_tokens'] for item in sublist]


###VADER Model

sid = vader.SentimentIntensityAnalyzer()

scores_list = []


for comment_list in post_df['phrase_tokens']:
  compound_list = []
  flat_list = [item for sublist in comment_list for item in sublist]
  for comment in flat_list:
    ss = sid.polarity_scores(comment)
    if ss['compound'] == 0.0:
      continue
    compound_score = ss['compound']
    compound_list.append(compound_score)
  
  plt.figure()
  plt.hist(compound_list, bins=20)
  plt.title('Compound Score Distribution')
  plt.show()

  compound_average = (sum(compound_list)/len(compound_list))
  scores_list.append(compound_average)

post_df['VADER_compound'] = scores_list

###GET Crypto data
ticks = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'USDT-USD', 'ADA-USD', 'XLM-USD', 'LINK-USD', 'UNI3-USD', 'DOT1-USD', 'USDC-USD']  #adjust tickers as necessary
tickers = yfinance.Tickers(ticks)

close = tickers.history()['Close']
open = tickers.history()['Open']
day_change = close - open
pct_day_change = close.pct_change()
avg_day_change = pct_day_change.mean(axis=1)
avg_day_change.name = 'avg_day_change'
avg_day_change

###Comparison DataFrame
post_subdf = (post_df[['date', 'VADER_compound']]).reset_index().drop('submission_id', axis=1).set_index('date').sort_index()
comp_df = post_subdf.join(avg_day_change)
