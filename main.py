import matplotlib.pyplot as plt
import pandas as pd
import RAKE
import sys
import argparse
from  textwrap import indent

STOP_LIST = 'SmartStopList.py'


def highlight_word(words, keyword):
    temp = words.replace(' ' + keyword + ' ', ' **' + keyword.upper() + '** ')
    temp = temp.replace(' ' + keyword[0].upper() + keyword[1:] + ' ', ' **' + keyword.upper() + '** ')
    return temp


class TranslationData:

    def __init__(self, text):
        self.text = text
        self.data = self.create_data()

    def find_freq_of_word(self, keyword):
        for word in self.data:
            if word[0].lower() == keyword.lower():
                return word[1]
        return 0

    def find_timestamp_index_of_word(self, keyword):
        index_num = 0
        index_num_list = []
        timestamp_words = self.text.split('\n\n')
        for words in timestamp_words:
            for word in words.split():
                if word.lower() == keyword.lower():
                    index_num_list.append(index_num)
                    break
            index_num += 1
        return index_num_list

    def print_keyword_passages(self, keyword):
        index_num_list = self.find_timestamp_index_of_word(keyword)
        timestamp_words = self.text.split('\n\n')
        print('Freq: ' + str(self.find_freq_of_word(keyword)) + '\n')
        for index_num in index_num_list:
            highlight_text = highlight_word(timestamp_words[index_num], keyword)
            print(highlight_text + '\n')
        print('\n')

    def find_timestamp_index_of_words(self, keywords):
        index_num = 0
        index_num_list = []
        timestamp_words = self.text.split('\n\n')
        stopper = 0
        for words in timestamp_words:
            for word in words.split():
                for keyword in keywords:
                    if word.lower() == keyword.lower():
                        index_num_list.append(index_num)
                        stopper = 1
                        break
                if stopper:
                    stopper = 0
                    break
            index_num += 1
        return index_num_list

    def get_keyword_passages(self, keywords):
        index_num_list = self.find_timestamp_index_of_words(keywords)
        print(index_num_list)
        timestamp_words = self.text.split('\n\n')

        text_dump = timestamp_words[0] + ' KEYWORD DUMP\n\n' + timestamp_words[1] + '\n\n' + 'KEYWORDS: ' + '\n'

        for keyword in keywords:
            freq = str(self.find_freq_of_word(keyword))
            text_dump += '\t' + keyword + ': ' + freq + '\n'
        text_dump += '\n' + 'RAKE STATS:' + '\n'
        df = pd.DataFrame(self.data)
        text_dump += str(df[:50]) + '\n\n\n'

        for index_num in index_num_list:
            temp = timestamp_words[index_num]
            keys = 'Keywords: '
            for keyword in keywords:
                temp2 = highlight_word(temp, keyword)
                if temp != temp2:
                    keys += keyword.upper() + ', '
                temp = temp2
            text_dump += keys + '\n' + temp + '\n\n'

        return text_dump

    def create_data(self):
        rake = RAKE.Rake(STOP_LIST)
        return rake.run(self.text, minCharacters=1, minFrequency=1)
        # return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='Keyword Trans-scripter')
    parser.add_argument('--file', dest='text_file', type=str, help='Path of the text file')
    parser.add_argument('--words', dest='keywords_file', type=str, help='Path of keywords file')
    args = parser.parse_args()

    file_path = args.text_file

    keywords_file = 'keywords.txt'
    if args.keywords_file is not None:
        keywords_file = args.keywords_file
    try:
        with open(keywords_file, 'r') as f:
            keywords = f.read()
            keywords = keywords.split()
    except FileNotFoundError:
        print('No Keyword File!')
        sys.exit(0)

    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print('No Text File!')
        sys.exit(0)

    translation_data = TranslationData(text)
    new_text = translation_data.get_keyword_passages(keywords)

    new_file_path = file_path[:-4] + '_keywords.txt'
    with open(new_file_path, 'w') as f:
        f.write(new_text)

    # while True:
    #     keyword = input('Enter Keyword: ')
    #     if keyword == 'q':
    #         break
    #     translation_data.print_keyword_passages(keyword)



if __name__ == '__main__':
    main()

