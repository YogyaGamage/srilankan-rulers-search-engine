#https://github.com/rksk/sinhala-news-analysis/blob/master/sinhala-stemmer/stem_dictionary.txt
#https://github.com/nlpcuom/Sinhala-Stopword-list/blob/master/stop%20words.txt
with open('D:/Aca Sem 07/Data Mining/IR project/stem.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

lines = [line.replace('	', ' => ') for line in lines]

with open('D:/Aca Sem 07/Data Mining/IR project/stem1.txt', 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)