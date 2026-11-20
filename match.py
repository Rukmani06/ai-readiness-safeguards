import pandas as pd, pycountry
MANUAL={'Bolivia (Plurinational State of)':'BOL','Democratic Republic of the Congo':'COD','Gambia (Republic of The)':'GMB',
'Guinea Bissau':'GNB','Iran (Islamic Republic of)':'IRN','Micronesia (Federated States of)':'FSM','Republic of Korea':'KOR',
'State of Palestine':'PSE','China Hong Kong Special Administrative Region':'HKG',"Cote d'Ivoire":'CIV','Kosovo':'XKX'}
def iso(n):
    if n in MANUAL: return MANUAL[n]
    try: return pycountry.countries.lookup(n).alpha_3
    except LookupError: pass
    try:
        r=pycountry.countries.search_fuzzy(n); return 'FUZZY:'+r[0].alpha_3+':'+r[0].name
    except LookupError: return None

import sys
vd=pd.read_csv('vdem_subset.csv'); vd=vd[vd.year==2025]; vn=dict(zip(vd.country_text_id,vd.country_name))
out={}
for f,k in [('pdf/oxford2025_pillars.csv','ox'),('pdf/girai2026_scores.csv','gi')]:
    d=pd.read_csv(f); d['iso3']=d.country.map(iso); d['vdem_name']=d.iso3.map(vn)
    assert d.iso3.notna().all() and not d.iso3.str.startswith('FUZZY').any() and not d.iso3.duplicated().any(), d[d.iso3.duplicated(keep=False)]
    d.to_csv(f.replace('.csv','_iso.csv'),index=False)
    diff=d[d.vdem_name.notna()&(d.country.str[:4].str.lower()!=d.vdem_name.str[:4].str.lower())]
    print(k,'n',len(d),'no V-Dem:',d[d.vdem_name.isna()].country.tolist()); print(diff[['country','iso3','vdem_name']].to_string())
