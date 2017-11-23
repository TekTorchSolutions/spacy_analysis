def mysplit(s):
    head = s.rstrip('abcdefghijklmnopqrstuvwxyz')
    tail = s[len(head):]
    return head, tail
text="del – bom – Indigo – 7:35am arrv 8:50 , Delhi to Lucknow 16th december Evening between 16:00 to 18:00"
splitted_text=[]
for s in text.split():
    if any(i.isdigit() for i in s):
        head,tail=mysplit(s)
        splitted_text.append(head)
        splitted_text.append(tail)
    else:
        splitted_text.append(s)

print(splitted_text)