greetings = [ "balance", "amount", "money", "worth", "overview" ]

# Generates a bot response from a user message
def generateReply(message):
	tokens = message.split(" ")

	if len(tokens)>0 and tokens[0].lower() in greetings:
			return "Your bank balance is: Rs. 0.00"
	else:
			return "I don't understand." # Otherwise the bot doesn't understand what the user said