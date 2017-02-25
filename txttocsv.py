import os, csv


with open('train.csv', 'w') as csvfile:
    for i in os.listdir(os.getcwd() + '/training_set'):
        if 'D' in i:
            party = 'D'
        else:
            party = 'R'

        segment = open('training_set/' + i, 'rb')
        segment = ''.join(segment.readlines()).replace('\n', '')

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([segment, party])

print 'all done'

