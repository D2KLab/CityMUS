import subprocess

w = "http://dbpedia.org/resource/Rome"
p = "http://dbpedia.org/resource/Lazio"
endpoint = "https://dbpedia.org/sparql"

import re


def createLine(text):
    lines = text.split('\n')
    return "".join([l.strip() for l in lines])


out = subprocess.check_output(["php","-f","test.php",w,p,endpoint])


results = re.findall(r'<result>.*?</result>', out, re.S)


xml = "\n".join([createLine(r) for r in results])


#print xml