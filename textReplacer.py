from nltk.corpus import brown
from nltk.tag import tnt
import nltk
import pickle
from watson_developer_cloud import AlchemyLanguageV1, ToneAnalyzerV3
from nltk import tokenize
from PyDictionary import PyDictionary

def modifyNews(textData):
    # Initialize the dictionary
    dictionary = PyDictionary()

    # This code is for training TNT Tagger
    # Not necessary when using pickle file
    """
    train_data = brown.tagged_sents()[:45872]
    test_data = brown.tagged_sents()[45872:]

    tnt_pos_tagger = tnt.TnT()
    tnt_pos_tagger.train(train_data)

    f = open('tnt_brown_pos_tagger.pickle', 'w')
    pickle.dump(tnt_pos_tagger, f)
    f.close()
    """

    # Use the pickle file if you do not want to retrain the object
    tnt_pos_tagger = pickle.load(open('tnt_brown_pos_tagger.pickle'), 'r')

    query = raw_input('Article: ')
    alchemy_language = AlchemyLanguageV1(api_key='4c390db1d45633cef4dcff9f91f404618194807e')
    entities_alchemy = alchemy_language.combined(
        text=query.decode('ascii', errors="ignore"),
        extract='entities,keywords',
        sentiment=1,
        max_items=1)
    entity_list = []
    for entity in entities_alchemy['entities']:
        entity_list.append(entity['text'])

    tone_analyzer = ToneAnalyzerV3(
        username='25cd5253-a691-466c-a5ee-5a00823ebefd',
        password='1DkgWn4x0QG3',
        version='2016-05-19')

    sentences = tokenize.sent_tokenize(query.decode('ascii', errors="ignore"))

    newParagraph = ""
    range_ext = 0
    for sentence in sentences:
        tagged_sent = tnt_pos_tagger.tag(nltk.word_tokenize(sentence))
        if any(ext in sentence for ext in entity_list) or range_ext > 0:
            range_ext += 2
            for i in xrange(0, len(tagged_sent)):
                if "JJ" in tagged_sent[i][1] or "RB" in tagged_sent[i][1] or "VB" in tagged_sent[i][1]:
                    syn_list = [tagged_sent[i][0]]
                    syn_list += dictionary.synonym((tagged_sent[i][0]))
                    joy_index = 0
                    syn_index = 0
                    for j in xrange(0, len(syn_list)):
                        tone_json = tone_analyzer.tone(text=syn_list[j])
                        if joy_index < tone_json['document_tone']['tone_categories'][0]['tones'][4]['score']:
                            joy_index = tone_json['document_tone']['tone_categories'][0]['tones'][4]['score']
                            syn_index = j
                    tagged_sent[i] = (syn_list[syn_index], tagged_sent[i][1])
        for ind_tag in tagged_sent:
            newParagraph += str(ind_tag[0])
            newParagraph += ' '
        if range_ext > 0:
            range_ext -= 1


    # ptree = ParentedTree.fromstring(tree.)
    # tree = ' '.join([w for w in tree.leaves()])
    # print tree

    return newParagraph

"""
ptree = ParentedTree.convert(tree)

leaf_values = ptree.leaves()

if 'Trump' in leaf_values:
    leaf_index = leaf_values.index('Trump')
    tree_location = tree.leaf_treeposition(leaf_index)
    print tree_location
    print leaf_values.index('Trump').parent()
"""