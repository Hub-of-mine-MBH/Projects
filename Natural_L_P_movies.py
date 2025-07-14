import spacy

# Function to calculate similarity between two movie descriptions
def prob_movie(description, watched_movie, max_prob):
    prob = description.similarity(watched_movie)
    if prob > max_prob:
        max_prob = prob  # Update max if this one is higher
        return max_prob
    else:
        return max_prob  # Otherwise, return existing max


# Function to determine which movie from the file is most similar to the user's watched movie
def deter_movie(past_movie):
    toks_ref_movie = nlp(past_movie)  # Processes the watched movie description using spaCy
    
    # Initialize maximum similarity score
    maxi_prob = 0                     
    movie = []                        


    with open("C:\\Users\\mobha\\movies.txt", "r", encoding="utf-8") as file:
        for lines in file:
            line = lines.strip().split(":") 

            toks = nlp(line[1])  # Processing the recommended movie description
            new_prob = prob_movie(toks, toks_ref_movie, maxi_prob)  # Compare with user's movie

            if new_prob > maxi_prob:
                maxi_prob = new_prob  # Update max similarity score
                movie = line          # Store the current best match

    # Print out the best matching movie title and description
    print(f"Recommended movie: {movie[0]}")
    print()
    print(f"Movie description:\n\n{movie[1]}")


# Load the spaCy language model
nlp = spacy.load("en_core_web_md")


ref_movie = (
    "Will he save their world or destroy it? "
    "When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a "
    "planet where the Hulk can live in peace. Unfortunately, Hulk lands on the "
    "planet Sakaar where he is sold into slavery and trained as a gladiator."
)


deter_movie(ref_movie)
