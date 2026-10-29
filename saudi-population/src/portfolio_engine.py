from pathlib import Path
import pandas as pd, numpy as np, sqlite3, json, math, hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

SOURCE_URL='https://tableau.stats.gov.sa/views/Population-EN_17298840150060/PopulationEstimatesbyGenderNationalityandRegion2010-2022.csv?:showVizHome=no'

def run(root,kind):
 root=Path(root); out=root/'outputs';out.mkdir(exist_ok=True);(root/'sql').mkdir(exist_ok=True)
 source=root/'data/source.csv';d=pd.read_csv(source);q={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_rows':len(d),'kind':kind}
 db=sqlite3.connect(out/'analysis.sqlite')
 if kind!='saudi':
  d.columns=[c.lower().replace(' ','_').replace('-','_') for c in d.columns]
  d['order_date']=pd.to_datetime(d.order_date,format='%d/%m/%Y',errors='raise');d['ship_date']=pd.to_datetime(d.ship_date,format='%d/%m/%Y',errors='raise')
  assert d.row_id.is_unique
  for c in d.select_dtypes('object'):d[c]=d[c].str.strip()
  for c in ['sales','profit','quantity','discount']:d[c]=pd.to_numeric(d[c],errors='raise')
  assert (d.sales>=0).all() and (d.quantity>0).all() and d.discount.between(0,1).all()
  assert (d.ship_date>=d.order_date).all()
  assert not d[['customer_id','order_id','product_id','order_date','sales','profit']].isna().any().any()
  q['repeated_business_rows_with_distinct_row_ids']=int(d.drop(columns='row_id').duplicated().sum());q['decision']='Preserve distinct source Row IDs. Repeated business rows are flagged, not proven errors.'
  q['missing_postal_codes']=int(d.postal_code.isna().sum());d['postal_code']=d.postal_code.map(lambda v:'' if pd.isna(v) else str(int(v)).zfill(5))
  d['shipping_days']=(d.ship_date-d.order_date).dt.days;d['year']=d.order_date.dt.year;d['month']=d.order_date.dt.strftime('%Y-%m');d['order_date']=d.order_date.dt.strftime('%Y-%m-%d');d['ship_date']=d.ship_date.dt.strftime('%Y-%m-%d')
  d['is_loss']=(d.profit<0).astype(int)
  d.to_csv(out/'clean_data.csv',index=False);d.to_sql('sales',db,if_exists='replace',index=False)
  if kind=='sales':
   queries={
   'overview':'''SELECT COUNT(*) AS line_items, COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_id) AS customers, SUM(sales) AS sales, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS profit_margin, SUM(sales)/COUNT(DISTINCT order_id) AS average_order_value, SUM(is_loss) AS loss_making_lines FROM sales''',
   'monthly':'''SELECT month, SUM(sales) AS sales, SUM(profit) AS profit, COUNT(DISTINCT order_id) AS orders FROM sales GROUP BY month ORDER BY month''',
   'subcategories':'''SELECT sub_category, SUM(sales) AS sales, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS profit_margin FROM sales GROUP BY sub_category ORDER BY profit''',
   'regions':'''SELECT region, SUM(sales) AS sales, SUM(profit) AS profit, COUNT(DISTINCT order_id) AS orders FROM sales GROUP BY region ORDER BY sales DESC''',
   'discounts':'''SELECT CASE WHEN discount=0 THEN 'No discount' WHEN discount<=0.2 THEN 'Up to 20%' ELSE 'Above 20%' END AS discount_band, COUNT(*) AS lines, SUM(sales) AS sales, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS profit_margin FROM sales GROUP BY discount_band''',
   'growth':'''WITH annual AS (SELECT year,SUM(sales) AS sales FROM sales GROUP BY year), prev AS (SELECT year,sales,LAG(sales) OVER(ORDER BY year) AS prior_sales FROM annual) SELECT *, (sales-prior_sales)/NULLIF(prior_sales,0) AS yoy_growth FROM prev ORDER BY year'''
   }
   frames={k:pd.read_sql_query(v,db) for k,v in queries.items()};summary=frames['overview'].iloc[0].to_dict();bad=frames['subcategories'].iloc[0];summary['lowest_profit_subcategory']=bad.sub_category;summary['lowest_subcategory_profit']=float(bad.profit)
   assert abs(summary['sales']-d.sales.sum())<1e-6 and abs(summary['profit']-d.profit.sum())<1e-6
   summary['date_start']=d.order_date.min();summary['date_end']=d.order_date.max()
   title='Retail sales and profitability';subtitle='Educational Superstore dataset • 2014–2017 • USD'
   charts=[('Monthly sales',frames['monthly'],'month','sales'),('Profit by subcategory',frames['subcategories'],'sub_category','profit')]
   insights=[f"{summary['orders']:,.0f} distinct orders from {summary['customers']:,.0f} customers across {summary['line_items']:,.0f} order lines.",f"Overall profit margin is {summary['profit_margin']:.2%}, calculated as total profit / total sales.",f"{bad.sub_category} has the lowest aggregate profit (${bad.profit:,.2f}); review product mix and discount policy before making changes."]
   modeltables={'Sales':d[['row_id','order_id','customer_id','product_id','order_date','region','category','sub_category','sales','profit','quantity','discount','shipping_days','year','month']].rename(columns=lambda c:''.join(w.title() for w in c.split('_')))}
  else:
   snapshot=(pd.to_datetime(d.order_date).max()+pd.Timedelta(days=1)).strftime('%Y-%m-%d')
   queries={'rfm':f'''SELECT customer_id, CAST(julianday('{snapshot}')-julianday(MAX(order_date)) AS INTEGER) AS recency_days, COUNT(DISTINCT order_id) AS frequency, SUM(sales) AS monetary, SUM(profit) AS profit FROM sales GROUP BY customer_id'''}
   r=pd.read_sql_query(queries['rfm'],db)
   for col,outcol in [('recency_days','r_score'),('frequency','f_score'),('monetary','m_score')]:
    score=np.ceil(r[col].rank(method='average',pct=True)*4).clip(1,4).astype(int);r[outcol]=5-score if col=='recency_days' else score
   def seg(x):
    if x.r_score>=3 and x.f_score>=3 and x.m_score>=3:return 'Champions'
    if x.r_score<=2 and x.f_score>=3:return 'At risk'
    if x.r_score>=3 and x.f_score>=3:return 'Loyal'
    if x.r_score>=3:return 'Promising'
    return 'Needs attention'
   r['segment']=r.apply(seg,axis=1);r['snapshot_date']=snapshot;r.to_sql('rfm',db,index=False,if_exists='replace');r.to_csv(out/'rfm_customers.csv',index=False)
   queries['segments']='''SELECT segment,COUNT(*) AS customers,SUM(monetary) AS sales,SUM(profit) AS profit,AVG(recency_days) AS avg_recency,AVG(frequency) AS avg_frequency FROM rfm GROUP BY segment ORDER BY sales DESC'''
   frames={'segments':pd.read_sql_query(queries['segments'],db)};summary={'customers':len(r),'sales':float(r.monetary.sum()),'segments':r.segment.nunique(),'snapshot_date':snapshot,'at_risk_customers':int((r.segment=='At risk').sum()),'champion_customers':int((r.segment=='Champions').sum()),'champion_sales_share':float(r.loc[r.segment=='Champions','monetary'].sum()/r.monetary.sum())}
   assert len(r)==d.customer_id.nunique() and abs(r.monetary.sum()-d.sales.sum())<1e-6
   q['scoring']='Quartiles based on average percentile ranks; equal values receive equal scores. R is reversed. Segment rules are heuristic, not a predictive model.'
   title='Customer RFM segmentation';subtitle=f'Historical segmentation • Snapshot {snapshot} • Customer IDs only'
   charts=[('Customers by segment',frames['segments'],'segment','customers'),('Revenue by segment',frames['segments'],'segment','sales')]
   insights=[f"{len(r):,} customers assigned to {r.segment.nunique()} mutually exclusive segments.",f"Champions account for {summary['champion_sales_share']:.1%} of historical revenue.",f"{summary['at_risk_customers']} customers meet the heuristic at-risk rule; a retention test is proposed, not an observed uplift."]
   modeltables={'Customers':r.rename(columns=lambda c:''.join(w.title() for w in c.split('_')))}
 else:
  d=d.rename(columns={'D Year':'year','Region':'region','Max. Admin Leaf Cd Code':'region_code','Obs Value':'population'})
  d['population']=pd.to_numeric(d.population.astype(str).str.replace(',',''));totals=d[d.region=='All'].copy();d=d[d.region!='All'].copy()
  assert not d.duplicated(['year','region']).any();assert len(d)==169 and d.region.nunique()==13
  checks=d.groupby('year').population.sum().sub(totals.set_index('year').population)
  q['national_total_difference_by_year']={str(k):int(v) for k,v in checks.items()};assert checks.abs().max()<=5
  d.to_csv(out/'clean_data.csv',index=False);totals.to_csv(out/'official_national_totals.csv',index=False)
  d.to_sql('population',db,index=False,if_exists='replace')
  queries={
  'national_trend':'SELECT year,SUM(population) AS population FROM population GROUP BY year ORDER BY year',
  'regions_2022':'''SELECT region,population,1.0*population/SUM(population) OVER() AS national_share FROM population WHERE year=2022 ORDER BY population DESC''',
  'growth':'''WITH endpoints AS (SELECT region,MAX(CASE WHEN year=2010 THEN population END) AS pop_2010,MAX(CASE WHEN year=2022 THEN population END) AS pop_2022 FROM population GROUP BY region) SELECT *,1.0*(pop_2022-pop_2010)/pop_2010 AS growth_2010_2022 FROM endpoints ORDER BY growth_2010_2022 DESC''',
  'yearly_growth':'''WITH previous AS (SELECT region,year,population,LAG(population) OVER(PARTITION BY region ORDER BY year) AS previous_population FROM population) SELECT *,1.0*(population-previous_population)/NULLIF(previous_population,0) AS yoy_growth FROM previous ORDER BY region,year'''
  }
  frames={k:pd.read_sql_query(v,db) for k,v in queries.items()};last=frames['regions_2022'];p0=int(d.loc[d.year==2010,'population'].sum());pn=int(last.population.sum());summary={'regions':13,'years':13,'region_year_records':len(d),'population_2022':pn,'population_2010':p0,'growth_2010_2022':pn/p0-1,'top_three_share':float(last.head(3).national_share.sum()),'largest_region':last.iloc[0].region}
  title='Saudi regional population';subtitle='GASTAT official historical series • 2010–2022 • All nationalities and genders'
  charts=[('Population by region in 2022',last,'region','population'),('National population trend',frames['national_trend'],'year','population')]
  insights=[f"{pn:,} residents in the 2022 regional total across 13 regions.",f"The three largest regions account for {summary['top_three_share']:.1%} of the 2022 total.",f"Population increased {summary['growth_2010_2022']:.1%} between 2010 and 2022; this historical series is not a 2026 population estimate."]
  modeltables={'Population':d.rename(columns=lambda c:''.join(w.title() for w in c.split('_')))}
 for k,sql in queries.items():(root/'sql'/f'{k}.sql').write_text(sql+';\n')
 for k,df in frames.items():df.to_csv(out/f'{k}.csv',index=False)
 db.close();q['checks_passed']=True;q['clean_rows']=len(d);q['rows_removed']=q['source_rows']-len(d);q['removal_reason']='13 national aggregates excluded to prevent double counting' if kind=='saudi' else 'None'
 (out/'quality_report.json').write_text(json.dumps(q,indent=2));(out/'summary.json').write_text(json.dumps(summary,indent=2));(out/'insights.json').write_text(json.dumps(insights,indent=2))
 for name,table in modeltables.items():table.to_csv(out/f'powerbi_{name}.csv',index=False)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 fig,axes=plt.subplots(1,2,figsize=(15,6.7),gridspec_kw={'width_ratios':[1.1,1]});fig.patch.set_facecolor('#f4f7fb');fig.suptitle(title,fontsize=22,fontweight='bold',x=.055,ha='left',y=.96);fig.text(.055,.895,subtitle,color='#50627a',fontsize=10)
 for ax,(ct,df,x,y) in zip(axes,charts):
  if x in ['month','year']:
   ax.plot(df[x].astype(str),df[y],color='#007f86',linewidth=2.5);ticks=list(range(0,len(df),max(1,len(df)//6)));ax.set_xticks(ticks,[str(df[x].iloc[i]) for i in ticks],rotation=30)
  else:
   c=['#c45757' if v<0 else '#007f86' for v in df[y]];ax.barh(df[x].astype(str),df[y],color=c);ax.invert_yaxis()
  ax.set_title(ct,loc='left',pad=15,fontweight='bold');ax.grid(axis='x' if x not in ['month','year'] else 'y',alpha=.13);ax.ticklabel_format(style='plain',axis='y' if x in ['month','year'] else 'x');ax.set_facecolor('#fff')
  formatter=FuncFormatter(lambda v,pos: f'{v/1e6:g}m' if abs(v)>=1e6 else f'{v/1e3:g}k' if abs(v)>=1e3 else f'{v:g}')
  (ax.yaxis if x in ['month','year'] else ax.xaxis).set_major_formatter(formatter)
 fig.subplots_adjust(left=.14,right=.97,top=.8,bottom=.18,wspace=.65);fig.text(.055,.035,'Portfolio simulation | Computed results; no claimed business uplift | AI-assisted implementation',fontsize=9,color='#50627a');fig.savefig(root/'dashboard_preview.png',dpi=150);plt.close(fig)
 payload={'kind':kind,'title':title,'subtitle':subtitle,'summary':summary,'insights':insights,'data':(r if kind=='rfm' else d).fillna('').to_dict('records')}
 (out/'dashboard_data.json').write_text(json.dumps(payload,default=str))
 print(kind,json.dumps(summary))
 return payload,modeltables
