from customtkinter import *
import heroes
from wonderwords import RandomSentence
import time

app = CTk()
app.geometry('800x300')
set_appearance_mode('dark')
app.iconbitmap('typewriterapp.ico')

app.title('HeroesTypeWriter')

s = RandomSentence()


class TextGenerator:
    def __init__(self):
        self.sentences = []
        self.count = 0
        self.display = ''
        self.r_key = 1
        self.user_text = ''
        self.user_text_words = 0
        self.text_compare = ''
        self.r_key_total = 0
        self.turn_clock = 1
        self.start_time = None
        self.end_time = None
        self.wpm_count = 0

    def generate(self):
        n_sentences = 48
        temp_list = []
        while n_sentences > 0:
            result = s.sentence()
            temp_list.append(result)
            n_sentences -= 1
        self.sentences = [f'{heroes.genarr(48)[i]} ' + temp_list[i].lower()
                          for i in range(0, len(temp_list))]

    def display_text(self):
        if self.count + 4 <= 48:
            result = ' \n\n'.join([sr for sr in self.sentences[self.count:self.count + 4]])
            self.count += 4
        else:
            result = ''
        self.display = result

    def callback(self):
        if self.r_key < 1:
            self.r_key += 1
            create_obj()
        else:
            if entry.get():
                if self.user_text:
                    self.user_text += ' \n\n'
                    self.user_text += entry.get()
                else:
                    self.user_text += entry.get()
            else:
                if self.user_text:
                    self.user_text += '0' * len(self.sentences[self.r_key_total])
                else:
                    self.user_text += '0' * len(self.sentences[self.r_key_total])
            self.t_compare()
            self.user_words()
            entry.delete(0, END)
            if self.r_key == 4:
                self.display_text()
                self.reset_textbox()
                self.r_key = 1
            else:
                self.r_key += 1
            self.wpm_counter()

    def user_words(self):
        if self.user_text:
            self.user_text_words = self.user_text.count(' ')
        else:
            self.user_text_words = 0

    def t_compare(self):
        if self.text_compare:
            self.text_compare += ' \n\n'
            self.text_compare += self.sentences[self.r_key_total]
        else:
            self.text_compare += self.sentences[self.r_key_total]
        self.r_key_total += 1

    def accuracy(self):
        if len(self.user_text) < len(self.text_compare):
            self.user_text = self.user_text.ljust(len(self.text_compare), '0')
        diff_count = sum(1 for a, b in zip(self.text_compare, self.user_text) if a != b)
        pct_accu = '{:.2f}'.format(abs((diff_count / len(self.text_compare)) * 100 - 100))
        return f'{pct_accu}%'

    def reset_textbox(self):
        textbox.configure(state='normal')
        textbox.delete(1.0, END)
        textbox.insert('end', self.display, )
        textbox.configure(state='disabled')

    def wpm_counter(self):
        if self.turn_clock:
            self.start_time = time.time()
            self.turn_clock -= 1
        else:
            self.end_time = time.time()
            minutes = (self.end_time - self.start_time) / 60
            if minutes >= 1:
                self.user_text_words = self.user_text.count(' ') + 1
                self.wpm_count = round(self.user_text_words / minutes)
                self.end_textbox()
                self.r_key = 0

    def end_textbox(self):
        textbox.configure(state='normal')
        textbox.delete(1.0, END)
        textbox.insert('end', 'Your result is:\n\n'
                              f'Words per minute: {self.wpm_count}\n\n'
                              f'Accuracy: {self.accuracy()}\n\n\n'
                              f'Press the <Return> key to try again.', )
        textbox.configure(state='disabled')


def create_obj():
    global tgen
    tgen = TextGenerator()
    tgen.generate()
    tgen.display_text()
    tgen.reset_textbox()


tgen = TextGenerator()
tgen.generate()
tgen.display_text()

textbox = CTkTextbox(master=app, width=750, height=240, font=('Arial', 25), )
textbox.insert('end', tgen.display, )
textbox.configure(state='disabled')

entry = CTkEntry(master=app, placeholder_text='Type here...',width=750,
                 font=('Arial', 25),)

textbox.pack(anchor='n', expand=True,)
entry.pack(anchor='n', expand=True,)


app.bind('<Return>', lambda event: tgen.callback())


app.mainloop()
