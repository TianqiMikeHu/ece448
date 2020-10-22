"""
Part 4: Here should be your best version of viterbi, 
with enhancements such as dealing with suffixes/prefixes separately
"""
import math

def viterbi_3(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    data = {}
    count = {}
    tags = []
    tag_pair = {}
    output = []
    just_words = []
    hapax = []
    hapax_count = 0
    k = 0
    alpha = 0.00001
    suffix = {}
    suffix2 = {}
    for sentence in train:
        for i in range(len(sentence)):
            if data.get(sentence[i][1]) is None:
                data[sentence[i][1]] = {}
                count[sentence[i][1]] = 0
                tags.append(sentence[i][1])
            count[sentence[i][1]] += 1
            if data[sentence[i][1]].get(sentence[i][0]) is None:
                data[sentence[i][1]][sentence[i][0]] = 1
            else:
                data[sentence[i][1]][sentence[i][0]] += 1
            if i > 0:
                if tag_pair.get(sentence[i - 1][1] + sentence[i][1]) is None:
                    tag_pair[sentence[i - 1][1] + sentence[i][1]] = 1
                else:
                    tag_pair[sentence[i - 1][1] + sentence[i][1]] += 1
            if len(sentence[i][0]) > 2:
                substring = sentence[i][0]
                substring = substring[-2:]
                if suffix.get(substring+sentence[i][1]) is None:
                    suffix[substring+sentence[i][1]] = 1
                    suffix2[substring + sentence[i][1]] = 1
                else:
                    suffix[substring + sentence[i][1]] += 1
                    suffix2[substring + sentence[i][1]] += 1
                substring = sentence[i][0]
                substring = substring[-3:]
                if suffix.get(substring + sentence[i][1]) is None:
                    suffix[substring + sentence[i][1]] = 1
                    suffix2[substring + sentence[i][1]] = 1
                else:
                    suffix[substring + sentence[i][1]] += 1
                    suffix2[substring + sentence[i][1]] += 1
    for i in range(len(tags)):
        hapax.append(0.00001)
    for i in range(len(tags)):
        if tags[i] == 'X':
            continue
        for word in data[tags[i]]:
            if data[tags[i]][word] == 1:
                hapax[i] += 1
                hapax_count += 1
    for key in suffix:
        if suffix[key] < 5000:
            del suffix2[key]
    # format: (probability, word, previous tag index)
    trellis = []
    for sentence in test:
        for word in sentence:
            k += 1
            just_words.append(word)
    for i in range(k):
        trellis.append([])
        for j in range(len(tags)):
            trellis[i].append((float('-inf'), '', 0))
    for i in range(len(just_words)):
        # pdb.set_trace()
        if i == 0:
            trellis[0][0] = (math.log(1), 'START', -1)
            for x in range(len(tags)):
                prev = trellis[0][0][0]
                if tag_pair.get('START' + tags[x]) is None:
                    transition = math.log(alpha / count['START'])
                else:
                    transition = math.log((tag_pair.get('START' + tags[x]) + alpha) / count['START'])
                if data[tags[x]].get(just_words[1]) is None:
                    emission = math.log(alpha / count[tags[x]])
                else:
                    emission = math.log((data[tags[x]][just_words[1]] + alpha) / count[tags[x]])
                trellis[1][x] = (prev + transition + emission, just_words[1], 0)
        elif i == len(just_words) - 1:
            break
        else:
            for x in range(len(tags)):
                prob = float('-inf')
                best = 0
                if data[tags[x]].get(just_words[i + 1]) is None:
                    if len(just_words[i+1]) > 2:
                        substring = just_words[i + 1]
                        substring = substring[-3:]
                        if suffix2.get(substring+tags[x]) is not None:
                            emission = math.log(alpha / count[tags[x]])
                        else:
                            substring = just_words[i + 1]
                            substring = substring[-2:]
                            if suffix2.get(substring + tags[x]) is not None:
                                emission = math.log(alpha / count[tags[x]])
                            else:
                                emission = math.log((alpha * hapax[x] / hapax_count) / count[tags[x]])
                    else:
                        emission = math.log((alpha * hapax[x] / hapax_count) / count[tags[x]])
                else:
                    emission = math.log((data[tags[x]][just_words[i + 1]] + alpha) / count[tags[x]])
                for y in range(len(tags)):
                    prev = trellis[i][y][0]
                    if tag_pair.get(tags[y] + tags[x]) is None:
                        transition = math.log(alpha / count[tags[y]])
                    else:
                        transition = math.log((tag_pair.get(tags[y] + tags[x]) + alpha) / count[tags[y]])
                    temp = prev + transition + emission
                    if temp > prob:
                        prob = temp
                        best = y
                trellis[i + 1][x] = (prob, just_words[i + 1], best)
    output.append([])
    prob = float('-inf')
    best = 0
    for i in range(len(tags)):
        if trellis[k - 1][i][0] > prob:
            prob = trellis[k - 1][i][0]
            best = i
    output[0].insert(0, (trellis[k - 1][best][1], tags[best]))
    best = trellis[k - 1][best][2]
    for i in range(1, k):
        # pdb.set_trace()
        if trellis[k - i - 1][best][1] == 'START':
            best = 0
        output[0].insert(0, (trellis[k - i - 1][best][1], tags[best]))
        if best == 0 and i != (k - 1):
            output.insert(0, [])
        best = trellis[k - i - 1][best][2]
    # print(output[0])
    # print(test)
    # print(output)
    return output