import subprocess
import time

n_crawlers = 15

for i in range(n_crawlers):
    fopen = open('./logs/crawler{}.log'.format(i), 'w')
    # subprocess.run(cmd, shell=True, stdout=fopen, stderr=fopen)
    cmd = ['source activate conda_1 \n scrapy crawl ucl.ac.uk -o output.json']
    subprocess.Popen(cmd, shell=True, stdout=fopen, stderr=fopen)
    print('crawler {} kicked off'.format(i))
    # give the url service some time!
    time.sleep(5)

    # , stdout=fopen)

print('all crawlers running')