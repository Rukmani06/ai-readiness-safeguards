import re,csv,sys
L=open(sys.argv[1]).read().split('\n')
n9=r'\s+'.join([r'(\d+(?:\.\d+)?)']*9)
rows=[]
for i,l in enumerate(L):
    m=re.match(r'^\s*(\d{1,3})\s+(.*?)\s*'+n9+r'\s*$',l)
    if not m: continue
    t=m.group(2).strip()
    t=re.sub(r'\s+(Europe|Africa|Central|Middle|Asia &|North|South &|Northern)$','',t).strip()
    if t in ('Europe','Africa','Central','Middle','Asia &','North','South &','Northern'): t=''
    rows.append([int(m.group(1)),t]+[float(m.group(k)) for k in range(3,12)]+[i])
for r in rows:
    i=r[-1]; ctx=[re.sub(r'\s{2,}.*','',L[j].strip()) for j in range(i-2,i+3) if j!=i and L[j].strip()]
    print(r[0],'|',r[1],'|',ctx)
