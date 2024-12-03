import wikipedia
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag


def generate_questions(paragraph):
    questions = []

    sentences = sent_tokenize(paragraph)

    for sentence in sentences:
        words = word_tokenize(sentence)

        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]

        tagged_words = pos_tag(filtered_words)

        named_entities = [word for word, pos in tagged_words if pos == 'NNP']

        for entity in named_entities:
            questions.append(f"What is {entity} known for?")

    return questions


def get_answer(question):
    try:
        if question.startswith("What is"):
            summary = wikipedia.summary(question, sentences=2)
            return summary
        else:
            return "This question might not be suitable for a Wikipedia search. Try a more factual question."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple Wikipedia pages for '{question}'. Please refine your search."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find an answer on Wikipedia."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while retrieving information."
