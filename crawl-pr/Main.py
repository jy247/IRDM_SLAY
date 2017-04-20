#from PreProcess import PreProcess
from ReverseDictionary import ReverseDictionary
import pickle
import os

urls = []
urls.append('www.cat.com/index/')
urls.append('www.hat.com/find/something')
urls.append('www.run.com/find/something')

contents = []
contents.append('some story test about a cat cat')
contents.append('some story about a cat hat')
contents.append('running')

#
#
# pp_obj = PreProcess()
# for i in range(0, len(contents)):
#     contents[i] = pp_obj.process_sentence(contents[i])
#
#

rd_obj = ReverseDictionary()
one_contents = ['research', 'excellence', 'framework', 'ref', 'evaluation', 'ucl', 'universities', 'assessed', 'considerably', 'ahead', 'institutions', 'research', 'work', 'rated', 'worldleading', 'highest', 'possible', 'category', 'research', 'work', 'rated', 'internationally', 'excellent', 'ucl', 'researchers', 'computer', 'science', 'informatics', 'received', 'grade', 'point', 'average', 'submitted', 'staff', 'assessed', 'ref', 'ucl', 'computer', 'science', 'made', 'seminal', 'contributions', 'across', 'full', 'range', 'core', 'strengths', 'associated', 'research', 'groups', 'centres', 'including', 'centre', 'health', 'informatics', 'multiprofessional', 'education', 'chime', 'biomedical', 'physics', 'biochemical', 'engineering', 'centre', 'medical', 'image', 'computing', 'cmic', 'great', 'sorrow', 'report', 'death', 'andrea', 'bittau', 'earned', 'bsc', 'phd', 'degrees', 'ucl', 'computer', 'science', 'much', 'respected', 'student', 'colleague', 'across', 'departmentan', 'obituary', 'can', 'found', 'memories', 'andrea', 'can', 'added', 'sending', 'honor', 'remember', 'andreas', 'life', 'talent', 'passion', 'computer', 'systems', 'research', 'andrea', 'bittau', 'memorial', 'scholarship', 'established', 'will', 'support', 'phd', 'student', 'ucl', 'computer', 'science', 'learn', 'memorial', 'scholarship', 'two', 'fellowships', 'awarded', 'support', 'outstanding', 'graduate', 'students', 'exceptional', 'research', 'computer', 'science', 'ebook', 'examines', 'new', 'directions', 'human', 'computer', 'interaction', 'away', 'lab', 'renewal', 'will', 'signal', 'ten', 'years', 'recognition', 'uks', 'authority', 'cyber', 'security', 'multiple', 'ai', 'agents', 'learned', 'work', 'together', 'play', 'starcraft', 'science', 'fiction', 'combat', 'video', 'game', 'using', 'twoway', 'communication', 'ucl', 'among', 'funding', 'recipients', 'projects', 'explore', 'vast', 'potential', 'distributed', 'ledger', 'technology', 'computer', 'science', 'department', 'university', 'college', 'london', 'gower', 'street', 'london', 'wce', 'bt', 'copyright', 'ucl']
rd_obj.add_one('www.cat.com', one_contents)
# rd_obj.add_all(urls, contents)

results = rd_obj.get_urls(['research'])

print(os.getcwd())
i = 0
full_dic = ReverseDictionary()
full_parent_to_children_urls_dic = {}

while i < 15:
    try:
        with open('./data/Rdic_title_{}.pickle'.format(i), 'rb') as handle:
            titles_dic = pickle.load(handle)

        # with open('./crawl-pr/data/parent_to_children_urls_{}.pickle'.format(i), 'rb') as handle:
        #     parent_to_children_urls_dic = pickle.load(handle)
        #
        # for key in parent_to_children_urls_dic:
        #     full_parent_to_children_urls_dic[key] = parent_to_children_urls_dic[key]

        new_dic = ReverseDictionary()
        new_dic.Decode(titles_dic)
        print('size of one dic: {}'.format(len(new_dic.index_to_url_dic)))
        full_dic.combine(new_dic)
    except:
        print('nothing found for i: {}'.format(i))
    i += 1

print('loaded {} files'.format(i))
print('size of full dic: {}'.format(len(full_dic.index_to_url_dic)))
print('size of parent to child dic: {}'.format(len(full_parent_to_children_urls_dic)))


search_string = 'cat'
search_terms = pp_obj.process_sentence(search_string)
# #
print(rd_obj.get_urls(search_terms))