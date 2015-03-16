# -*- coding: utf-8 -*-

import csv, json
import scipy.stats, numpy

def mkJson():
  """
  """
  r = readFile1("./data/dataComuniPiem.csv")
  r13 = readFile2("./data/camera2013.csv")
  r08 = readFile2("./data/camera2008.csv")
  r06 = readFile2("./data/camera2006.csv")

  l13 = readFile3("./data/liste13.csv")
  l08 = readFile3("./data/liste08.csv")
  l06 = readFile3("./data/liste06.csv")
 

  res = [];
  for k, v in r.iteritems():
    if k in r13.keys() and k in r08.keys() and k in r06.keys():

      #r13[k].update({"liste":l13[k]})
      #r08[k].update({"liste":l08[k]})
      #r06[k].update({"liste":l06[k]})

      r13[k].update({"liste":selection(l13[k],["pier luigi bersani","mario monti","giuseppe piero grillo","silvio berlusconi"])})
      r08[k].update({"liste":selection(l08[k],["pier ferdinando casini","walter veltroni","silvio berlusconi"])})
      r06[k].update({"liste":selection(l06[k],["prodi romano","berlusconi silvio"])})

      r13[k].update({"entropia":round(entropy(l13[k]),3)})
      r08[k].update({"entropia":round(entropy(l08[k]),3)})
      r06[k].update({"entropia":round(entropy(l06[k]),3)}) 

      v.update({"y13":r13[k], "y08":r08[k], "y06":r06[k]})
      res.append(v)

  #for k, v in r1.iteritems():
  #  v.update(r[k])

  with open('data.json', 'w') as outfile:
    json.dump(res, outfile)

  lr("y13",res)
  lr("y08",res)
  lr("y06",res)

  rangeEntr([i["y13"]["entropia"] for i in res],4)
  rangeEntr([i["y08"]["entropia"] for i in res],4)
  rangeEntr([i["y06"]["entropia"] for i in res],4)


  return None;

def selection(obj, names):
  """
  """
  res = {}
  tr = {"pier luigi bersani":"b", "mario monti":"m", "giuseppe piero grillo":"g", "silvio berlusconi":"sb", "pier ferdinando casini":"c", "walter veltroni":"v", "prodi romano":"p", "berlusconi silvio":"sb"}
  for k, v in obj.iteritems():
    if k in names:
      res[tr[k]] = v
  res["w"] = max(res.iterkeys(), key=(lambda key: res[key])) # return the key with the max value
  return res

def lr(year,res):
  """
  """
  print year 
  x = []
  y = []
  for v in res:
    #x.append(v['dens'])
    #x.append(numpy.log(v['dens']))
    x.append(numpy.log(v['pop']))
    y.append(v[year]['perc'])
  b0, b1 = linear_regression(x, y, .95)
  #print min(x), y[x.index(min(x))], b0 + b1 * min(x)
  #print max(x), y[x.index(max(x))], b0 + b1 * max(x)
  return None

def readFile1(file1):
  """
  """
  res = {}
  with open(file1, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
      res[row[3].lower()] = {"comune":row[3],"sup":float(row[5]), "pop":int(row[7]), "dens":float(row[8])}
  return res

def readFile2(file2):
  """
  """
  res = {}
  with open(file2, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
      res[change(row[0].lower().strip())] = {"elettori":int(row[1]), "votanti":int(row[2]), "bianche":int(row[3]), "nonvalide":int(row[4]), "perc":round(float(row[2])/float(row[1]),4)}
  return res

def readFile3(file3): #liste
  """
  """
  res = {}
  lista = ""
  with open(file3, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
      comune = change(row[0].lower().strip())
      if comune not in res:
        res[comune] = {}
        lista = row[1].lower().strip()
        res[comune][lista] = int(row[3])
      else:
        if row[1] is "":
          res[comune][lista] += int(row[3])
        else:
          lista = row[1].lower().strip()
          res[comune][lista] = int(row[3])
  return res

         
import math, numpy
def entropy(obj):
  """
  """
  tot = float(sum(obj.values()))
  return -sum(v/tot * math.log(v/tot) for v in (i for i in obj.values() if i != 0))

def rangeEntr(l,n):
  """
  """
  #l = sorted(l)
  #k = len(l)/n
  #for i in range(1,n+1):
  #  print l[k * i]
  print numpy.mean(l) - numpy.std(l)
  print numpy.mean(l) + numpy.std(l)





def change(name):
  """
  """
  c = {"leini'":"leini", "campiglione-fenile":"campiglione fenile", "cavaglia'":"cavaglià", "viale d'asti":"viale", "trinita'":"trinità", "vestigne'":"vestignè", "roccaforte mondovi'":"roccaforte mondovì", "santhia'":"santhià", "rora'":"rorà", "viu'":"viù", "carde'":"cardè", "cerreto langhe":"cerretto langhe", "bastia mondovi'":"bastia mondovì", "cerrina":"cerrina monferrato", "sanfre'":"sanfrè", "montaldo di mondovi'":"montaldo di mondovì", "brignano frascata":"brignano-frascata", "cuorgne'":"cuorgnè", "loranze'":"loranzè", "torre mondovi'":"torre mondovì", "lusiglie'":"lusigliè", "vialfre'":"vialfrè", "carru'":"carrù", "rocca ciglie'":"rocca cigliè", "piova' massaia":"piovà massaia", "villanova mondovi'":"villanova mondovì", "aglie'":"agliè", "bianze'":"bianzè", "san michele mondovi'":"san michele mondovì", "mazze'":"mazzè", "cirie'":"ciriè", "monta'":"montà", "mondovi'":"mondovì", "ciglie'":"cigliè", "alluvioni cambio'":"alluvioni cambiò", "cerreto delle langhe":"cerretto langhe", "monte castello":"montecastello"}
  if name in c.keys():
    return c[name]
  else:
    return name

def linear_regression(x, y, prob):
    """
    Return the linear regression parameters and their  confidence intervals.
    >>> linear_regression([.1,.2,.3],[10,11,11.5],0.95)
    """
    x = numpy.array(x)
    y = numpy.array(y)
    n = len(x)
    xy = x * y
    xx = x * x

    # estimates

    b1 = (xy.mean() - x.mean() * y.mean()) / (xx.mean() - x.mean()**2)
    b0 = y.mean() - b1 * x.mean()
    s2 = 1./n * sum([(y[i] - b0 - b1 * x[i])**2 for i in xrange(n)])
    print 'b0 = ',b0
    print 'b1 = ',b1
    print 's2 = ',s2
    
    #confidence intervals
    
    alpha = 1 - prob
    c1 = scipy.stats.chi2.ppf(alpha/2.,n-2)
    c2 = scipy.stats.chi2.ppf(1-alpha/2.,n-2)
    print 'the confidence interval of s2 is: ',[n*s2/c2,n*s2/c1]
    
    c = -1 * scipy.stats.t.ppf(alpha/2.,n-2)
    bb1 = c * (s2 / ((n-2) * (xx.mean() - (x.mean())**2)))**.5
    print 'the confidence interval of b1 is: ',[b1-bb1,b1+bb1]
    
    bb0 = c * ((s2 / (n-2)) * (1 + (x.mean())**2 / (xx.mean() - (x.mean())**2)))**.5
    print 'the confidence interval of b0 is: ',[b0-bb0,b0+bb0]
    print {"y":{"b0":b0, "b1":b1, "s2":s2, "db0":[b0-bb0,b0+bb0], "db1":[b1-bb1,b1+bb1], "ds2":[n*s2/c2,n*s2/c1]}}
    return b0, b1
  


