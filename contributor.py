import json, shutil, os

class TweetCorrection():
    def __init__(self):
        self.config = json.loads(open('config.json').read())
        self.tweets = open(self.config['DATA_FILE_NAME']).read().split('\n')

        self.omitted_tweets = []
        self.sentiments = []
        self.unchanged_tweets = []
        self.corrected_original_tweets = []
        self.corrected_changed_tweets = []

    def display_rules(self):
        print('\nPLEASE READ THE BELOW RULES CAREFULLY AND APPLY AS NEEDED:')
        for rule in self.config['RULES']:
            print('* '+rule)
        print('\nStarting Tweet Correction...\n')


    def prompt_usn_input(self):
        try:
            self.usn = raw_input('Please enter your USN: ')
            self.output_dir = self.usn+'_output'
            assert(self.usn != '')
        except Exception:
            self.prompt_usn_input()

    def prompt_split_input(self):
        try:
            self.split_index = int(raw_input('Please enter split assigned to you: '))
            assert(self.split_index != '')
        except:
            self.prompt_split_input()

    def prompt_tweet(self, tweet, count):
        print('\n\nTweet ' + str(count) + ': \"' + tweet + '\"')
        print

    def prompt_tweet_omission(self):
        omit = raw_input('Should the tweet be removed? (no) : ')
        return False if (omit in ['','no']) else True

    def prompt_sentiment_input(self):
        try:
            sentiment = raw_input('Please assign sentiment to tweet? (0 -negative, 1 -neutral, 2 -positive) : ')
            assert (sentiment in ['0', '1', '2'])
            return sentiment
        except:
            self.prompt_sentiment_input()

    def prompt_if_correction_needed(self):
        correction = raw_input('Does the tweet need correction? (yes) : ')
        return True if (correction in ['','yes']) else False

    def prompt_correction_input(self):
        correction = raw_input('Please enter the complete corrected tweet : ')
        edit_correction = raw_input('Do you want to edit the correction? (no) : ')
        if (edit_correction in ['','no']):
            return correction
        else:
            return self.prompt_correction_input()

    def prompt_before_save(self):
        save = raw_input('\nDo you want to save? (yes) : ')
        return True if (save in ['','yes']) else False

    def process_tweet(self, tweet, count):
        self.prompt_tweet(tweet, count)

        omitted = self.prompt_tweet_omission()

        if not omitted:
            sentiment = self.prompt_sentiment_input()

            if self.prompt_if_correction_needed():
                correction_needed = True
                correction = self.prompt_correction_input()
            else:
                correction_needed = False

            if not self.prompt_before_save():
                self.process_tweet(tweet, count)
            else:
                self.sentiments.append(sentiment)
                if correction_needed:
                    self.corrected_changed_tweets.append((correction, sentiment))
                    self.corrected_original_tweets.append((tweet, sentiment))
                else:
                    self.unchanged_tweets.append((tweet, sentiment))
        else:
            if not self.prompt_before_save():
                self.process_tweet(tweet, count)
            else:
                self.omitted_tweets.append(tweet)

    def save_output(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        with open(self.output_dir+'/omitted_tweets.txt','w') as f:
            for omitted_tweet in self.omitted_tweets:
                f.write(omitted_tweet+'\n')

        with open(self.output_dir+'/unchanged_tweets.txt','w') as f:
            for unchanged_tweet_sentiment_tuple in self.unchanged_tweets:
                f.write(', '.join(unchanged_tweet_sentiment_tuple)+'\n')

        with open(self.output_dir+'/corrected_original.txt','w') as f:
            for corrected_original_tweet_sentiment_tuple in self.corrected_original_tweets:
                f.write(', '.join(corrected_original_tweet_sentiment_tuple)+'\n')

        with open(self.output_dir+'/corrected_changed.txt','w') as f:
            for corrected_changed_tweet_sentiment_tuple in self.corrected_changed_tweets:
                f.write(', '.join(corrected_changed_tweet_sentiment_tuple)+'\n')

        shutil.make_archive(self.output_dir, 'zip', self.output_dir)
        print('\nThank you for your contribution. Your work is saved into '+self.output_dir+'.zip')

    def run(self):
        self.prompt_usn_input()
        self.prompt_split_input()
        self.display_rules()

        self.split_size = len(self.tweets) / int(self.config['NUMBER_OF_PARTICIPANTS'])
        self.split_start_index = (self.split_index-1) * self.split_size
        self.split_end_index = len(self.tweets) if(self.split_size == self.split_index) else (self.split_index) * self.split_size

        count = 1
        for tweet_index in range(self.split_start_index, self.split_end_index):
            tweet = self.tweets[tweet_index]
            self.process_tweet(tweet, count)
            count += 1

        self.save_output()

app = TweetCorrection()
app.run()
