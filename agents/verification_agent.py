def verify_information(documents):

    verified_docs = []

    for doc in documents:

        if len(doc) > 200:
            verified_docs.append(doc)

    return verified_docs