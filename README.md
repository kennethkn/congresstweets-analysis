# congresstweets-analysis

Analysing the tweets of U.S. congress members in relation to political affiliation and current issues, by considering the sentiment, frequency, and trends of related statements to understand the priorities and features of the two parties.

Link to Analysis: https://html-preview.github.io/?url=https://github.com/kennethkn/congresstweets-analysis/blob/main/analysis.html

## Project Description

This project aims to foster a boarder understanding of the bipartisan U.S. politics by analyzing the tweets of U.S. congress members, including democratic and republican senators and representatives. The importance of it lies in the potential to reveal patterns and trends in the political discourse of recent years. Understanding these patterns can provide insights into the priorities and strategies of the two parties. Additionally, analyzing the sentiment of tweets can reveal their stance on current issues.

<!-- , as well as their uniformity or diversity in opinion, the portion of radical and moderate members, and the potential for bipartisanship.

The main challenge in answering these questions is the processing and analysis of unstructured text data. NLP techniques will be required to extract meaningful information. Also, accurately determining the sentiment of a tweet can be challenging due to the nuances of human language. The use of machine learning models will contribute to a more in-depth analysis. However, the time and computational resources required, as well as my ability, can be a limitation.

There have been several online sources that have analyzed Twitter data to study political discourse. with a few involving the specific dataset I will be using. However, they either do not answer my questions or are no longer maintained, making my project unique in the use of up-to-date data and the specific investigation target of U.S. congress members. -->

The dataset available for this project is from the GitHub repository [congresstweets](<https://github.com/alexlitel/congresstweets>). It contains a comprehensive collection of tweets from U.S. congress members since 2017, making it a rich resource for a diverse analysis.

<!-- The heavy use of twitter/X by politicians to communicate with the public and express their opinions is seen in no other counties, by which I am fascinated. -->

## Questions to Answer

1. What is the trend of the most common words/hashtags used by democratic and republican congress members in their tweets?
2. What are the sentiments of tweets by democratic and republican congress members on significant issues such as COVID-19, climate change, abortion, gun control, and etc?

## Methodology

Given the enormous size of the dataset (~4M entries), I have chosen a database approach to store and query the data. The database is hosted locally on my computer via PostgresSQL, but you can reproduce the database by executing Python scripts in the `scripts` folder, which holds scripts for database construction as well as text mining.

1. Ready PostgreSQL server (`brew install postgresql && brew services start postgresql` if you are using macOS)
2. Create a database named `congresstweets` (`createdb congresstweets`)
3. Clone the repository
4. Notice the empty `data/tweets/` folder. You need to download the tweets data from the [congresstweets repo](<https://github.com/alexlitel/congresstweets>), as well as [here](https://archive.org/details/tweetsofcongress) for older 2017 data. Place the downloaded json files (eg `2020-03-24.json`) in the `data/tweets/` folder.
5. Setup venv and activate it (`python -m venv venv && source venv/bin/activate`)
6. Install the required packages (`pip install -r requirements.txt`)
7. Open `.env` and replace `YOUR_USERNAME` with your PostgreSQL username. (`DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/congresstweets`)
8. Run `models.py` to create the tables.
9. Run `db_insert_members.py` to populate the `members` table in the database.
10. Run `db_insert_tweets.py` to populate the `tweets` table in the database.
11. Run `text_mining.py` to populate columns pertaining to text mining results in the `tweets` table.
12. Open `analysis.rmd` in RStudio and knit the file to generate the analysis.

## Table of Contents

1. Tweet Count by Party and Year
2. Tweet Count by Chamber and Year
3. Top Tweeters by Year
4. Top Hashtags
5. Top Hashtags by Party
6. Top Hashtags by Party and Year
7. Top Hashtags by Chamber
8. Top Words
9. Top Words by Party
10. Top Words by Party and Year
11. Top Words by Chamber
12. Sentiment Analysis by Party and Year
13. Sentiment Analysis by Chamber and Year
14. Sentiment Analysis by Topic and Party
15. Top Accounts Retweeted
16. Top Accounts Retweeted by Party
17. Top Accounts Quoted
18. Top Accounts Quoted by Party
19. Top Accounts Mentioned
20. Top Accounts Mentioned by Party

## Room for Improvement

1. Use of BERT or GPT to infer topics from tweets.
2. Even more categories, such as top words by chamber and year, sentiment of tweets by topic and chamber, etc.

## Citation

Major credits to Alex Litel for providing the dataset. <https://github.com/alexlitel/congresstweets>
<!-- <https://ucsd.libguides.com/congress_twitter/senators>
<https://ucsd.libguides.com/congress_twitter/reps> -->
