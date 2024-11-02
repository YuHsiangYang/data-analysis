import LLM


#This is the main script for executing the process of searching and retrieving contents of web pages.

#Get the search prompt from the user
searchPrompt = input("Enter the search prompt: ")



#Use LLM to formulate queries based on the search prompt
queries = LLM.formulateQueries(searchPrompt)
print(queries)