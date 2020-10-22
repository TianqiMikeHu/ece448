"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    data = {}
    count = {}
    tags = []
    output = []
    common_tag = ''
    for sentence in train:
        for word in sentence:
            if data.get(word[1]) is None:
                data[word[1]] = {}
                count[word[1]] = 0
                tags.append(word[1])
            count[word[1]] += 1
            if data[word[1]].get(word[0]) is None:
                data[word[1]][word[0]] = 1
            else:
                data[word[1]][word[0]] += 1
    common_tag = max(count, key=count.get)
    for i in range(len(test)):
        output.append([])
        for word in test[i]:
            best = common_tag
            best_count = -1
            for t in tags:
                if data[t].get(word) is not None:
                    if data[t].get(word) > best_count:
                        best_count = data[t].get(word)
                        best = t
            output[i].append((word, best))
    return output
