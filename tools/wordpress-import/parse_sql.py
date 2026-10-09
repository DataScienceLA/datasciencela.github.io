import re, sys, json
from collections import Counter

def split_values(body):
    """Parse a MySQL VALUES (...),(...) string into list of tuples (strings/None/numbers)."""
    rows=[]; i=0; n=len(body)
    while i<n:
        if body[i]=='(':
            i+=1; row=[]; 
            while True:
                c=body[i]
                if c=="'":
                    i+=1; buf=[]
                    while True:
                        c=body[i]
                        if c=='\\':
                            nx=body[i+1]
                            buf.append({'n':'\n','r':'\r','t':'\t','0':'\0'}.get(nx,nx)); i+=2
                        elif c=="'":
                            if i+1<n and body[i+1]=="'": buf.append("'"); i+=2
                            else: i+=1; break
                        else: buf.append(c); i+=1
                    row.append(''.join(buf))
                else:
                    j=i
                    while body[i] not in ',)': i+=1
                    tok=body[j:i].strip()
                    row.append(None if tok=='NULL' else tok)
                if body[i]==',': i+=1; continue
                if body[i]==')': i+=1; break
            rows.append(row)
        else: i+=1
    return rows

def load(path):
    s=open(path,encoding='utf-8',errors='replace').read()
    tables={}
    for m in re.finditer(r"INSERT INTO `(\w+)` VALUES (.*?);\n",s,re.S):
        tables.setdefault(m.group(1),[]).extend(split_values(m.group(2)))
    cols={}
    for m in re.finditer(r"CREATE TABLE `(\w+)` \((.*?)\n\)",s,re.S):
        cols[m.group(1)]=re.findall(r"^\s*`(\w+)`",m.group(2),re.M)
    return tables,cols
