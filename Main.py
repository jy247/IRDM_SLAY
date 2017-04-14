from PreProcess import PreProcess
from ReverseDictionary import ReverseDictionary

urls = []
urls.append('www.cat.com/index/')
urls.append('www.hat.com/find/something')
urls.append('www.run.com/find/something')

contents = []
contents.append('some story test about a cat cat')
contents.append('some story about a cat hat')
contents.append('running')



pp_obj = PreProcess()
for i in range(0, len(contents)):
    contents[i] = pp_obj.process_sentence(contents[i])

rd_obj = ReverseDictionary()
rd_obj.build_dictionary(urls, contents)

search_string = 'cat'
search_terms = pp_obj.process_sentence(search_string)

print(rd_obj.get_urls(search_terms))