import regex
import os
def dumpfiles(folder):
    x=""
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            i = open(os.path.join(folder, file)).read()
            i = regex.sub(r"(#)[^\n]*","",i)
            x = x+i
    return(x)
culture = "serbian"
cultures = dumpfiles("C:/Users/geonc/OneDrive/Dokumentumok/Paradox Interactive/Crusader Kings II/mod/After-the-End---Old-Worldy/common/cultures")
male = regex.compile(culture+"\s*=\s*{[\S\s]*?male_names\s*=\s*{([^}]*)}")
male = male.search(cultures)
male = male.group(1)
male = regex.sub(r"([^\s_]+)_[^\s_]+",r"\1",male)
male = regex.sub(r'"([^\s]+)\s([^\s]+)"',r"\1_\2",male)
male = regex.sub(r'"([^\s]+)\s([^\s]+)\s([^\s]+)"',r"\1_\2_\3",male)
male = male.split()
male = [i.replace("_"," ") for i in male]
female = regex.compile(culture+"\s*=\s*{[\S\s]*?female_names\s*=\s*{([^}]*)}")
female = female.search(cultures)
female = female.group(1)
female = regex.sub(r"([^\s_]+)_[^\s_]+",r"\1",female)
female = regex.sub(r'"([^\s]+)\s([^\s]+)"',r"\1_\2",female)
female = regex.sub(r'"([^\s]+)\s([^\s]+)\s([^\s]+)"',r"\1_\2_\3",female)
female = female.split()
female = [i.replace("_"," ") for i in female]

file = open("w.txt","w",encoding='utf8')
file.write('", "'.join(female))
file.close()
