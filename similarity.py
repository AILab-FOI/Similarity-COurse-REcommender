# from gensim import similarities
# from gensim import models
# from gensim import corpora
# from collections import defaultdict
# from nltk.corpus import stopwords
# import numpy as np
# import nltk
# nltk.download('stopwords')


def to_LSA_comparison_document(description: str, goals: str):
    return f'{description} {goals}'


def generate_similarity_str(similarity):
    return f'{similarity * 100}%'

# def preprocessLSA(documents: list):
#     stoplist = set(stopwords.words('english'))

#     texts = [
#             [
#                 word for word in document.lower().split() if word not in stoplist
#             ] for document in documents
#     ]

#     frequency = defaultdict(int)
#     for text in texts:
#         for token in text:
#             frequency[token] += 1

#     texts = [
#             [
#                 token for token in text if frequency[token] > 1
#             ] for text in texts
#     ]

#     dictionary = corpora.Dictionary(texts)
#     corpus = [dictionary.doc2bow(text) for text in texts]

#     return (dictionary, corpus)


# def createLSIModel(dictionary, corpus, numTopics: int = 7):
#     lsi = models.LsiModel(
#         corpus,
#         id2word=dictionary,
#         num_topics=numTopics
#     )

#     index = similarities.MatrixSimilarity(lsi[corpus])

#     return (lsi, index)


# def computeLSA(baseDoc: str, documents: list, n: int = 1, lsi: models.LsiModel = None, index=None):
#     dictionary, corpus = preprocessLSA(documents)

#     if not lsi:
#         lsi, index = createLSIModel(dictionary, corpus)

#     if not index:
#         index = similarities.MatrixSimilarity(lsi[corpus])

#     vecBow = dictionary.doc2bow(baseDoc.lower().split())
#     vecLSI = lsi[vecBow]

#     sims = index[vecLSI]

#     return sims


def mock_compute_lsa(baseDoc: str, documents: list):
    return [x for x in range(len(documents))]


def compute_similarity(input_params, courses_json):
    input_document = to_LSA_comparison_document(
        input_params['description'], input_params['goals'])

    course_documents = list(map(lambda course: to_LSA_comparison_document(
        course['description'], course['goals']), courses_json))

    similarities = mock_compute_lsa(input_document, course_documents)

    for index, course in enumerate(courses_json):
        course_similarity = similarities[index]
        course['similarity'] = generate_similarity_str(course_similarity)

    return courses_json
