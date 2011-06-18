#!/usr/bin/python

import sys
import math
import random

import termios,os

def init(file_name):
    """read file and create problem/answer pair
    """
    try:
        fp = open(file_name)
    except IOError:
        print "open file error, file may not exist"
    
    data = fp.readlines()
    print "initialization...",
    problem_set = []
    for line_num, line in enumerate(data):
        line = line.strip()
        if line.find('\t') == -1:
            line = line.partition(' ')
        else:
            line = line.partition('\t')

        question = line[0].lower()
        for answer in line[2].split('/'):
            problem_set.append([question.strip(),answer.strip()])
    print "Done"
    return problem_set

def getkey():
    TERMIOS = termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

def examination(problem_set):
    """Examination
    """
    print "press a,s,d,f,g or 1,2,3,4,5 to choose A,B,C,D,E"
    print "q to quit"
    print "Start"
    print ""
    total_number = len(problem_set)
    
    key = {"a":0,"s":1,"d":2,"f":3,'g':4,
           "1":0,"2":1,"3":2,"4":3,"5":4,'\t':-1}
    number_of_correct = 0
    not_sure_problem = []
    wrong_problem = []

    for problem_num, problem in enumerate(problem_set):
        if random.randint(0,2) == 0:
            problem.reverse()
        question,answer = problem
        print "Question %d/%d:" %(problem_num+1, total_number)
        print question.upper()
        choice = [""] * 5
        correct_choice = random.randint(0,4)
        choice[correct_choice] = answer
        for i in range(0,5):
            if choice[i] == "":
                wrong_choice = problem_num
                while wrong_choice == problem_num:
                    wrong_choice = random.randint(0,total_number-1)
                    choice[i] = problem_set[wrong_choice][random.randint(0,1)]
                    for j in range(0,i):
                        if choice[i] == choice[j]:
                            wrong_choice = problem_num
                            break
            print "%s) %s" %(chr(ord('A')+i), choice[i])
        
        while True:
            ch = getkey()
            if ch == 'q':
                print ""
                return number_of_correct,problem_num,not_sure_problem,wrong_problem
            if ch in key:
                break

        if key[ch] == correct_choice:
            print "Correct"
            number_of_correct += 1
        elif key[ch] == -1:
            not_sure_problem.append(problem)
            print "The answer is",chr(ord('A')+correct_choice)
        else:
            wrong_problem.append(problem)
            print "WRONG"
            print "The answer is",chr(ord('A')+correct_choice)

        print "" 

    return number_of_correct,total_number,not_sure_problem,wrong_problem
        
def print_res(cnum, tnum, not_sure, wrong, fp):
    fp.write("Result: %d/%d %.2f%%.\n\n" %(cnum, tnum, cnum * 100.0 / tnum))
    fp.write("There are %d not sure problems:\n" %(len(not_sure)))
    for problem in not_sure:
        fp.write("%s    %s\n" %(problem[0], problem[1]))
    
    print ""

    fp.write("There are %d wrong problems:\n" %(len(wrong)))
    for problem in wrong:
        fp.write("%s    %s\n" %(problem[0], problem[1]))

def get_output_file_name():
    fname = "result"
    suffix = 0
    while os.path.exists(fname+str(suffix)):
        suffix += 1
    return fname + str(suffix)

if __name__=="__main__":
    if len(sys.argv) == 1:
        file_name = "ana0"
    else:
        file_name = sys.argv[1]
    random.seed()

    problem_set = init(file_name)
    random.shuffle(problem_set)
    
    cnum,tnum,not_sure,wrong = examination(problem_set)
    if tnum > 0:
        print_res(cnum,tnum,not_sure, wrong, sys.stdout)
        print_res(cnum,tnum,not_sure, wrong, open(get_output_file_name(), "w"))

