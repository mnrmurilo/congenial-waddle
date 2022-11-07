import pandas as pd
import re
from tkinter.filedialog import askopenfilename

MAIL_FILETYPES = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

WORD_FILETYPES = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

MAIL = askopenfilename(title='Select Mail .txt file',
        filetypes=MAIL_FILETYPES)
WORDS = askopenfilename(title='Select a List of Words .csv file',
        filetypes=WORD_FILETYPES)

OUTPUT_MAIL = 'output_files/mail.txt'
OUTPUT_CHECK = 'output_files/check_flag.csv'


def list_classified(file):
    df = pd.read_csv(file, header=None)
    return df.values.tolist()


def mail_text_file(file):
    with open(file, "r+") as original_mail:
        mail_str = original_mail.read() # read everything in the file
        return mail_str
        

def words_founded():
    df_given_words = pd.DataFrame(list_classified(WORDS))
    df_given_words.rename(columns={0: 'words'}, inplace=True)
    df_given_words['words'] = df_given_words['words'].str.strip()
    df_given_words['words'] = df_given_words['words'].str.lower()
    mail_str_source = mail_text_file(MAIL) \
        .replace('á', 'a')         \
        .replace('à', 'a')         \
        .replace('ó', 'o')         \
        .replace('ê', 'e')         \
        .replace('ú', 'u')         \
        .replace('í', 'i')         \
        .replace('ã', 'a')         \
        .replace('\n', ' ')         \
        .replace('/', ' ')         \
        .replace('ç', 'o')         \
        .replace(':', ' ')         \
        .replace('.', ' ')         \
        .replace(',', ' ')         \
        .replace('@', ' ')
    mail_str = re.sub('[^A-Za-z0-9 ]+', '', mail_str_source).lower()
    list_words_mail = mail_str.split(' ')
    df_given_mail = pd.DataFrame(list_words_mail)
    df_given_mail = df_given_mail.loc[df_given_mail[0] != 'n']
    df_given_mail.rename(columns={0: 'words'}, inplace=True)
    df_given_mail['words'] = df_given_mail['words'].str.strip()

    df_found_words = pd.merge(
        df_given_words,
        df_given_mail,
        on='words',
        how='inner')
    df_found_words = df_found_words.drop_duplicates(subset=['words'])
    df_found_words['check'] = 'True'

    check_words = pd.merge(
        df_given_words,
        df_found_words,
        on='words',
        how='outer')
    check_words = check_words.drop_duplicates(subset=['words'])
    check_words['check'].fillna('False',inplace=True)

    check_words.to_csv(OUTPUT_CHECK)


def main():
    mail = mail_text_file(MAIL).lower()
    classified_words = list_classified(WORDS)
    for all in classified_words:
        all = all[0].lower()
        mail = mail.replace(all, '****')
    with open(OUTPUT_MAIL, 'w') as censored_mail:
        censored_mail.write(mail)
    words_founded()

main()