from __future__ import print_function
from operator import attrgetter
from student import *
from subject import *

num_que_per_stu = 4;

subjects = []
#add_subject(subjects, "prem", "some", "text", "prag", "speech", "convers", "meta", "pragact", "pac", "socprag", "carter")

# add questions to subjects
#subjects[0].add_question(False, 'In Ch.1, Mey focuses on the reasons for pragmatics to expand fast and become a popular trend. Discuss them. Also, focus on its definition and aims.');
#subjects[0].add_question(False, 'According to author (Ch 1), one of the tasks of pragmatics is to explain how the same content is expressed differently in different contexts. Support this view by providing examples.');
#subjects[0].add_question(False, 'In Ch 1 the author deals with such issues as the importance of the user, definition of pragmatics, its limitation, components, perspectives, etc. Focus on each of these issues.');
#subjects[1].add_question(False, 'In Ch. 2, Mey speaks about pragmatics as the ``waste-basket of linguistics". Also, the author compares the development of modern pragmatics to the process of colonization. Moreover, the author mentions that ``[I]f the logic is the ``handmaid of philosophy", then language certainly is the handmaid of logic\'\" (p. 23). Explain what the author may imply.');
#subjects[1].add_question(False, 'In Ch.2, the author notes that ``since presuppositions \\ldots rest entirely on the user context, they are pragmatic, rather than semantic\\ldots " (p. 29). The author also expresses his belief that the renewed interest in the users of language \\ldots is among the main factors that have made pragmatic possible" (p. 29). Discuss these issues.');
#subjects[2].add_question(False, 'The term ``context" is one of the issues discussed in Ch. 3. Explain the role of context in pragmatics. Also, explain the idea put forward in the following sentence: ``There is a built-in contradiction between the conventionalized and more or less rigid forms that the language puts at our disposal, and the spontaneous, individual expression of our thoughts that we all strive to realize" (p. 42).');
#subjects[2].add_question(False, 'In Ch.3, the author focuses on implicature placing emphasis on its definition and conventional implicature. The author also touches upon such terms as ``reference" and ``anaphora". Consider them.');
#subjects[3].add_question(False, 'In Ch.4, the author focuses on two principles: The Communicative Principle and The Cooperative Principle. Discuss them.');
#subjects[3].add_question(False, 'In Ch 4, Mey criticizes ``Grice" referring some principles proposed by other researchers. Discuss them.');
#subjects[4].add_question(False, 'In Ch.5, Mey provides rationale for speech acts and focuses on language use and its functions. The author also focuses on the speech act of promising in the light of its physiognomy and rules. Moreover, the author considers speech verbs (SAVs) and speech acts without SAVs. Discuss them.');
#subjects[4].add_question(False, 'In Ch.5, Mey focuses on Indirect speech acts and places emphasis on their recognition, the steps proposed by Searle and the pragmatic view. The author also considers classifications proposed by various researchers. Discuss these issues.');
#subjects[5].add_question(False, 'Ch. 6 deals with conversation analysis placing emphasis on context, conversation organization and the techniques that are used to convey meaning. Discuss them.');
#subjects[5].add_question(False, 'In Ch.6, Mey examines the content-oriented mechanisms of conversation by providing insights into the pragmatics involved. Discuss them.');
#subjects[6].add_question(False, 'Ch. 7 focuses on Metapragmatics placing emphasis on the definition of metapragmatics, on the relationship between pragmatics and metapragmatics, and finally, on three views of pragmatics. Discuss them.');
#subjects[7].add_question(False, 'Ch. 8 focuses on pragmatic acts considering their essence, certain cases and definition of pragmatic acts. Discuss them.');
#subjects[7].add_question(False, 'In Ch.8, Mey explores ``the background of the social behavior that conversation, seen as pragmatic interacting, represents" (p. 217). What does the author imply?');
#subjects[8].add_question(False, 'In Ch.10, Mey notes that ``the basic character of a particular speech act \\ldots is seen as culture-dependent" (p. 263). How does the author support it?');
#subjects[8].add_question(False, 'In Ch.10, when dealing with pragmatics across cultures, the author focuses on such issues as politeness in conversations, cooperation, addressivity and silence. Discuss them.');
#subjects[9].add_question(False, 'In Ch.11, the author deals with the relationship between pragmatics as a ``pure science" and pragmatics as ``the practice of linguistics" (the relationship between theory and practice). Mey also claims that ``the people who are able to decide what kind of language can be deemed acceptable in the schools... are the same people who \\ldots oppress large segments of the population" (p. 292). Discuss these issues.');
#subjects[9].add_question(False, 'In Ch.11, the writer focuses on the language used in the media and medical interviews. The author also mentions that ``metaphors are necessary for our survival". Then the author adds that ``they make it difficult for us to understand, and be understood by others". What does the author imply here? How does the author support his view?');
#subjects[9].add_question(False, 'In Ch. 11, the author speaks of how language can be used as an instrument of manipulation and how language can be used to prevent the linguistic mis-representation of reality. The author also deals with critical pragmatics, power and naturalization issues. Explain the author\'s stance in these issues.');
#subjects[10].add_question(False, 'McCarthy and Carter (1994) favors for the discourse-based view of language contrasting it with the approach that characterized NL and EFL/ESL teaching. Explain their rationale.');
#subjects[10].add_question(False, 'McCarthy and Carter (1994) deal with the frameworks for classifying spoken and written modes and their applications. Discuss them.');

students = []
#students.append(Student(name='Ahmed Cebi', exc='prem'))
#students.append(Student(name='Madih Ahmed', exc='prem'))
#students.append(Student(name='Farida Aboud', exc='some'))
#students.append(Student(name='Zina Al Hamed', exc='some'))
#students.append(Student(name='Baya Maraf', exc='text'))
#students.append(Student(name='Samet Tok', exc='text'))
#students.append(Student(name='Pervin Arman', exc='prag'))
#students.append(Student(name='Mohammed Almallah', exc='prag'))
#students.append(Student(name='Mehmet V. Babayigit', exc='speech'))
#students.append(Student(name='Rabar A. M. Mahmood', exc='speech'))
#students.append(Student(name='Taye. E. Akinulegun', exc='convers'))
#students.append(Student(name='Airin Sh. Ibrahim', exc='convers'))
#students.append(Student(name='Lamya Hajihasankhan', exc='meta'))
#students.append(Student(name='Tala N. W. Shunnarah', exc='pragact'))
#students.append(Student(name='Darya A. Ismael', exc='pac'))
#students.append(Student(name='Mazin A. A. Abdulla', exc='pac'))
#students.append(Student(name='Lana Tahnan', exc='socprag'))
#students.append(Student(name='Mehrnaz Darban', exc='socprag'))
#students.append(Student(name='Mawada A. M. Enfiss', exc='carter'))
#students.append(Student(name='Sevar S. Salh', exc='carter'))

def distribute():
    for stu in students:
        while len(stu.q) != num_que_per_stu:
            if all(top != sub.name for sub in subjects for top in stu.t) is False:
                break
            sb = min([sub for sub in subjects if stu.exc != sub.name and all(top != sub.name for top in stu.t)],key=attrgetter('f'))
            #nMulChoice = stu.q.mulChoice.count(True)
            nMulChoice = sum(que.mulChoice is True for que in stu.q)
            if nMulChoice is 0:
                qu = min(sb.q, key=attrgetter('f'))
            else:
                qu = min([que for que in sb.q if que.mulChoice is False], key=attrgetter('f'))
            qu.f += 1
            sb.f += 1
            stu.q.append(qu)
            stu.t.append(sb.name)


def generate_latex():
    f = open('jav.tex', 'w')
    f.write('\\documentclass{article}\n')
    f.write('\\usepackage{xparse}\n')
    f.write('\\usepackage{booktabs}\n')
    f.write('\\usepackage{longtable}\n')
    f.write('\\usepackage{array}\n')
    f.write('\\usepackage{enumitem}\n')
    f.write('\\usepackage{geometry}\n')
    f.write('\\geometry{a4paper, total={170mm, 257mm}, left=20mm, top=20mm}\n')
    f.write('\\begin{document}\n')
    for i, stu in enumerate(students):
        f.write('\\newcommand{\\std' + chr(i+ord('a')) + '}{' + stu.name + '}\n')
    for i, sub in enumerate(subjects):
        for j, q in enumerate(sub.q):
            f.write('\\newcommand{\\i' + sub.name + chr(j+ord('a')) + '}{' + sub.name + '(' + chr(j+ord('a')) + ')}\n')
    for i, sub in enumerate(subjects):
        for j, q in enumerate(sub.q):
            f.write('\\newcommand' + '{' + q.s + '}' + '{' + q.q.rstrip() + '}\n')
    f.write('\\DeclareDocumentCommand{\\myenum}{m o o o}\n{\n')
    f.write('\\begin{minipage}[t]{\\linewidth}\n')
    f.write('\\begin{enumerate}[topsep=0pt]\n')
    for i in range(0, num_que_per_stu):
        f.write('\\IfValueT{#' + str(i+1) + '}{\\item #' + str(i+1) + '}\n')
    f.write('\\end{enumerate}\n')
    f.write('\\end{minipage}\n}\n')
    f.write('\\begin{longtable}{l | p{10cm}}\n')
    for i, stu in enumerate(students):
        f.write('\\std' + chr(i+ord('a')) + ' & \myenum')
        for j, q in enumerate(stu.q):
            if j == 0:
                f.write('{' + q.s + '}')
            else:
                f.write('[' + q.s + ']')
        f.write(' \\\\\n')
        if i != len(students)-1:
            f.write('\\midrule\n')
    f.write('\\end{longtable}\n\\end{document}')
