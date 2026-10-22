
import tiktoken

# Load the GPT-2 tokenizer
tokenizer = tiktoken.get_encoding("gpt2")

text = "I like to eat the apple, and ram is a very disciplined guy"

# Convert text into token IDs
token_ids = tokenizer.encode(text)

print("Original text:", text)
print("Token IDs:", token_ids)
print("Number of tokens:", len(token_ids))

# Convert token IDs back into text
decoded_text = tokenizer.decode(token_ids)
print("Decoded text:", decoded_text)
