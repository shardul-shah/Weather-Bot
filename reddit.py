import praw
import pdb
import re
import os
import importlib.util

# Documentation used = https://praw.readthedocs.io/en/v4.0.0/tutorials/comments.html


def main():
	
	# setting up importing of local module:
	
	spec = importlib.util.spec_from_file_location("weather", "/Users/Shardul/Desktop/python projects/weather app/Weather-app/weather.py")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	
	# setting up bot account
	reddit = praw.Reddit('bot1')
		
	# setting up subreddits to iterate through
	subreddit_list = [reddit.subreddit("5hardul"), reddit.subreddit("weather"), reddit.subreddit("all")]

	# from http://pythonforengineers.com/build-a-reddit-bot-part-3-automate-your-bot/ 
	for subreddit in subreddit_list:
		for submission in subreddit.hot(limit = 50):
		# alternative way to assign submission URL
		#submission = reddit.submission(url="https://www.reddit.com/r/5hardul/comments/82a9lc/bot_test_1/")	
			submission.comments.replace_more(limit=50)
			i = 0
		
			if not os.path.isfile("comments_replied_to.txt"):
					comments_replied_to = []
					f = open("comments_replied_to.txt", "w+")
			
			else:
				f = open("comments_replied_to.txt", "r+")
				comments_replied_to = f.read()
				comments_replied_to = comments_replied_to.split("\n")
				comments_replied_to = list(filter(None, comments_replied_to)) # filter with None
				
			for comment in submission.comments.list():	
				if comment.id not in comments_replied_to:
					re_result = re.search(r"!weather", comment.body)
					if re_result is not None:
						location = re.search(r"!weather(\d)\s(.*)", comment.body).group(1, 2)
						#print(location)
						city = re.search(r"(.*),", location[1]).group(1)
						country = re.search(r",(.*)", location[1]).group(1)
						#print(comment.body)
						loc_list = [city, country]
					
						API_key = "872ef0432dbc6d8ab88c0f92d85d7746"
						API_url_domain = "http://api.openweathermap.org/data/2.5/forecast?q="
						API_appid = "&APPID=" + API_key
  
						api_url = API_url_domain + city + ',' + country + API_appid # you can do string contacenation in Python, like in JavaScript
						
						day_flag = int(location[0])
						weather_dump = foo.weather(api_url, 0, loc_list, day_flag)
					
						output_str_new = "Date | Time (Local Time) | Temperature (C) | Pressure (kPa) | Humidity (%) | Cloud Cover (%) | Wind Speed (km/h) | Weather Condition"
						output_str_new+="\n-------|-------|-------|-------|-------|-------|-------|-------\n"
					
						output_str = ""
						dt_flag = False
					
						for day_info in weather_dump:
							if dt_flag == True:
								dt_tup = re.search(r"At (.*) (.*) local time", day_info).group(1,2) # https://regex101.com/r/DUspBR/1/
								weather_tup = re.search(r"Temperature \(Celsius\): (.*)\nPressure \(kPa\): (.*)\nHumidity \(%\): (.*)\nCloud Cover \(%\): (.*)\nWind Speed \(km/h\): (.*)\nThe weather condition outside: (.*)", day_info).group(1, 2, 3, 4, 5, 6) # https://regex101.com/r/sJ4NhZ/2/
								output_str+=(day_info+'\n')
						
								output_str_new+="{0} | {1} | {2} | {3}| {4} | {5}| {6} | {7}\n".format(dt_tup[0], dt_tup[1], weather_tup[0], weather_tup[1], weather_tup[2], weather_tup[3], weather_tup[4], weather_tup[5])
							dt_flag = True
					
					
						output_str_new+="\n\n\n\n---------------"
						output_str_new+="\n\nClick [here](https://www.reddit.com/r/5hardul/wiki/index) for instructions on how to use this bot!\n\n"
						output_str_new+="[Author](https://www.reddit.com/user/5hardul/) | "
						output_str_new+="[Provide Feedback](https://www.reddit.com/r/5hardul/comments/8ds9je/weatherbot_feedback_here/)"
						comment.reply(output_str_new)
						

						# Table format used for outputting table on Reddit. The pipes and ---- are required
						""""
						Column A | Column B | Column C
						---------|----------|----------
						A1 | B1 | C1
						A2 | B2 | C2
						"""
					
						comments_replied_to.append(comment.id)
						f.write(comment.id+"\n")
						i+=1
					
			f.close() #closing file
		
	
			# else do nothing
		
		#in order to not reply to the same comment repeatedly, I'll need to use the post_replied_to = [] method for the comment IDs too!	
		
	"""		   
	# This prints top level Reddit comments only, instead of printing nested comments as well	
	print("\nTop level comments only: ")
	for top_level_comment in submission.comments:
	    print(top_level_comment.body, "\n--------------")
	"""
	
		
if __name__ == "__main__":
	main()