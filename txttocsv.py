import os, csv

dcount = 0
rcount = 0

with open('train.csv', 'w') as csvfile:
    for i in os.listdir(os.getcwd() + '/training_set'):
        if (rcount + dcount) < 500:
            if 'D' in i and dcount < 250:
                party = 'pos'
                dcount += 1
            elif rcount < 250:
                party = 'neg'
                rcount += 1

            segment = open('training_set/' + i, 'rb')
            segment = ''.join(segment.readlines()).replace('\n', '')

            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([segment, party])

        else:

            break

print 'all done'

