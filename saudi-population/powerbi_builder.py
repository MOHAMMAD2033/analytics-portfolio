import json,zlib,base64,uuid,zipfile
from pathlib import Path
import pandas as pd
SC='https://developer.microsoft.com/json-schemas/fabric/'
def write(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def build(root,kind):
 root=Path(root);out=root/'outputs';base=root/'powerbi';base.mkdir(exist_ok=True);name={'sales':'Sales','rfm':'RFM','saudi':'SaudiPopulation'}[kind];sm=base/(name+'.SemanticModel');rp=base/(name+'.Report')
 write(base/(name+'.pbip'),{'$schema':SC+'pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}],'settings':{'enableAutoRecovery':True}})
 write(sm/'definition.pbism',{'$schema':SC+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
 write(rp/'definition.pbir',{'$schema':SC+'item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}})
 if kind=='sales':
  f=pd.read_csv(out/'powerbi_Sales.csv');f['DateKey']=f.OrderDate.str.replace('-','').astype(int)
  dates=f[['DateKey','Year','Month','OrderDate']].drop_duplicates().sort_values('DateKey').rename(columns={'OrderDate':'Date'})
  products=f[['ProductId','Category','SubCategory']].drop_duplicates();assert products.ProductId.is_unique
  regions=f[['Region']].drop_duplicates();customers=f[['CustomerId']].drop_duplicates()
  tables={'Sales':f.drop(columns=['Year','Month','Category','SubCategory','OrderDate']),'DimDate':dates,'DimProduct':products,'DimRegion':regions,'DimCustomer':customers}
  rels=[('Sales','DateKey','DimDate','DateKey'),('Sales','ProductId','DimProduct','ProductId'),('Sales','Region','DimRegion','Region'),('Sales','CustomerId','DimCustomer','CustomerId')]
  measures={'Sales':[('Total Sales','SUM(Sales[Sales])','$#,0.00'),('Total Profit','SUM(Sales[Profit])','$#,0.00'),('Profit Margin','DIVIDE([Total Profit], [Total Sales])','0.00%'),('Orders','DISTINCTCOUNT(Sales[OrderId])','#,0'),('Customers','DISTINCTCOUNT(Sales[CustomerId])','#,0'),('Average Order Value','DIVIDE([Total Sales], [Orders])','$#,0.00')]}
  pages=[('Sales overview',[('Total sales','Total Sales'),('Total profit','Total Profit'),('Profit margin','Profit Margin'),('Orders','Orders')],[('Monthly sales','lineChart','DimDate','Month','Total Sales'),('Profit by subcategory','clusteredBarChart','DimProduct','SubCategory','Total Profit')],[('DimDate','Year'),('DimRegion','Region')])]
 elif kind=='rfm':
  f=pd.read_csv(out/'powerbi_Customers.csv');tables={'Customers':f};rels=[]
  measures={'Customers':[('Customers','COUNTROWS(Customers)','#,0'),('Historical Sales','SUM(Customers[Monetary])','$#,0.00'),('Average Recency','AVERAGE(Customers[RecencyDays])','0.0'),('Average Frequency','AVERAGE(Customers[Frequency])','0.0'),('Historical Profit','SUM(Customers[Profit])','$#,0.00')]}
  pages=[('RFM customer segments',[('Customers','Customers'),('Historical revenue','Historical Sales'),('Recency in days','Average Recency'),('Orders per customer','Average Frequency')],[('Customers by segment','clusteredBarChart','Customers','Segment','Customers'),('Revenue by segment','clusteredBarChart','Customers','Segment','Historical Sales')],[('Customers','Segment'),('Customers','RScore')])]
 else:
  f=pd.read_csv(out/'powerbi_Population.csv');tables={'Population':f[['Year','RegionCode','Population']],'DimRegion':f[['RegionCode','Region']].drop_duplicates(),'DimYear':f[['Year']].drop_duplicates()};rels=[('Population','RegionCode','DimRegion','RegionCode'),('Population','Year','DimYear','Year')]
  measures={'Population':[('Population Latest Year','VAR LastYear = MAX(DimYear[Year]) RETURN CALCULATE(SUM(Population[Population]), DimYear[Year] = LastYear)','#,0'),('Regions','DISTINCTCOUNT(Population[RegionCode])','0'),('Latest Year','MAX(DimYear[Year])','0'),('Population 2010','CALCULATE(SUM(Population[Population]), REMOVEFILTERS(DimYear), DimYear[Year] = 2010)','#,0'),('Growth Since 2010','DIVIDE([Population Latest Year] - [Population 2010], [Population 2010])','0.0%'),('Annual Population','SUM(Population[Population])','#,0')]}
  pages=[('Saudi regional population',[('Latest year population','Population Latest Year'),('Regions','Regions'),('Latest year','Latest Year'),('Growth since 2010','Growth Since 2010')],[('Population trend','lineChart','DimYear','Year','Annual Population'),('Population by region latest year','clusteredBarChart','DimRegion','Region','Population Latest Year')],[('DimRegion','Region'),('DimYear','Year')])]
 model={'name':name,'compatibilityLevel':1600,'model':{'culture':'en-US','dataAccessOptions':{'legacyRedirects':True,'returnErrorValuesAsNull':True},'defaultPowerBIDataSourceVersion':'powerBI_V3','tables':[],'relationships':[]}}
 # dataSourceDefaultVersion is the TOM property used by Power BI.
 model['model']['dataSourceDefaultVersion']=model['model'].pop('defaultPowerBIDataSourceVersion')
 dax=[]
 for tn,df in tables.items():
  cols=[];types=[]
  for c in df:
   typ='int64' if pd.api.types.is_integer_dtype(df[c]) else 'double' if pd.api.types.is_numeric_dtype(df[c]) else 'string'
   cols.append({'name':c,'dataType':typ,'sourceColumn':c,'summarizeBy':'none' if typ=='string' or c.lower().endswith(('id','key','code')) or c=='Year' else 'sum'})
   types.append('{"'+c+'", '+{'int64':'Int64.Type','double':'type number','string':'type text'}[typ]+'}')
  raw=json.dumps(df.fillna('').values.tolist(),ensure_ascii=False,separators=(',',':')).encode();co=zlib.compressobj(wbits=-15);encoded=base64.b64encode(co.compress(raw)+co.flush()).decode()
  m='let\n    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("'+encoded+'", BinaryEncoding.Base64), Compression.Deflate)), '+json.dumps(list(df.columns)) .replace('[','{').replace(']','}')+'),\n    Typed = Table.TransformColumnTypes(Source, {'+', '.join(types)+'})\nin\n    Typed'
  table={'name':tn,'columns':cols,'partitions':[{'name':tn,'mode':'import','source':{'type':'m','expression':m.splitlines()}}]}
  if tn in measures:
   table['measures']=[{'name':n,'expression':exp,'formatString':fmt} for n,exp,fmt in measures[tn]]
   dax += [n+' = '+exp for n,exp,fmt in measures[tn]]
  model['model']['tables'].append(table);df.to_csv(out/f'model_{tn}.csv',index=False)
 for ft,fc,tt,tc in rels:model['model']['relationships'].append({'name':str(uuid.uuid5(uuid.NAMESPACE_DNS,name+ft+fc+tt+tc)),'fromTable':ft,'fromColumn':fc,'toTable':tt,'toColumn':tc,'crossFilteringBehavior':'oneDirection','fromCardinality':'many','toCardinality':'one'})
 write(sm/'model.bim',model);(base/'measures.dax').write_text('\n\n'.join(dax))
 definition=rp/'definition';write(definition/'version.json',{'$schema':SC+'item/report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
 # Minimal PBIR report definition; Desktop supplies its default theme.
 write(definition/'report.json',{'$schema':SC+'item/report/definition/report/3.3.0/schema.json','themeCollection':{},'settings':{'useEnhancedTooltips':True,'exportDataMode':'AllowSummarized'}})
 def field(t,c,measure=False):return {('Measure' if measure else 'Column'):{'Expression':{'SourceRef':{'Entity':t}},'Property':c}}
 def projection(t,c,measure=False):return {'field':field(t,c,measure),'queryRef':t+'.'+c,'nativeQueryRef':c}
 mt=list(measures)[0];pnames=[]
 for pi,(title,cards,charts,slicers) in enumerate(pages):
  pn='page'+str(pi+1);pnames.append(pn);pp=definition/'pages'/pn
  write(pp/'page.json',{'$schema':SC+'item/report/definition/page/2.1.0/schema.json','name':pn,'displayName':title,'displayOption':'FitToPage','height':800,'width':1280})
  specs=[]
  for i,(ct,mn) in enumerate(cards):specs.append((ct,'cardVisual',{'Data':{'projections':[projection(mt,mn,True)]}},20+i*315,20,300,140))
  for i,(ct,vt,tn,col,mn) in enumerate(charts):specs.append((ct,vt,{'Category':{'projections':[projection(tn,col)]},'Y':{'projections':[projection(mt,mn,True)]}},20+i*630,250,610,520))
  for i,(tn,col) in enumerate(slicers):specs.append((col,'slicer',{'Values':{'projections':[projection(tn,col)]}},20+i*630,175,610,60))
  for i,(ct,vt,qs,x,y,w,h) in enumerate(specs):
   vn='visual'+str(i+1);visual={'visualType':vt,'query':{'queryState':qs},'visualContainerObjects':{'title':[{'properties':{'show':{'expr':{'Literal':{'Value':'true'}}},'text':{'expr':{'Literal':{'Value':"'"+ct+"'"}}},'fontSize':{'expr':{'Literal':{'Value':'12D'}}}}}]},'drillFilterOtherVisuals':True}
   if vt=='lineChart':
    cat=next(iter(qs['Category']['projections']))['field'];visual['query']['sortDefinition']={'sort':[{'field':cat,'direction':'Ascending'}],'isDefaultSort':False}
   write(pp/'visuals'/vn/'visual.json',{'$schema':SC+'item/report/definition/visualContainer/2.13.0/schema.json','name':vn,'position':{'x':x,'y':y,'z':i,'height':h,'width':w,'tabOrder':i},'visual':visual})
 write(definition/'pages/pages.json',{'$schema':SC+'item/report/definition/pagesMetadata/1.1.0/schema.json','pageOrder':pnames,'activePageName':pnames[0]})
 (base/'OPEN_IN_POWER_BI.md').write_text('''# Open in Power BI Desktop

1. Keep this folder intact and open the `.pbip` file with current Power BI Desktop (Windows).
2. Select Refresh. Tables use embedded, compressed source snapshots: no local file paths or database credentials are required.
3. Inspect the model relationships and measures; compare totals to `../outputs/summary.json`.
4. Save as PBIX if desired and publish to your own workspace after review.

This PBIP was generated programmatically. JSON schema checks and numeric checks were performed, but Power BI Desktop refresh/render has NOT been run in this environment. The PNG and HTML previews are independent Python/web renderings, not screenshots of Power BI. If Desktop reports an issue, the cleaned CSVs, SQL and DAX are supplied separately.

To refresh with changed data, rerun `python analysis.py` from the project root. This rebuilds the embedded snapshot. Do not sum population across years. RFM scores refer to the documented historical snapshot, not current customer activity.
''')
 print('PBIP generated',base)
