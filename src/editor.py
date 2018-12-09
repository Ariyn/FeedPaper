import random
from itertools import product
import numpy as np

fullA4 = (210, 297)
size = {
  507 : [(1,1)],
  1407 : ((2,1), (1,2)),
  3338 : [(2,2)]
}

class Page:
  def __init__(self, size=fullA4):
    self.pageSize, self.matrixSize = size, (2,4)
    self.matrix = [None]*(self.pageSize[0]*self.pageSize[1])
  
  def isFilled(self, x, y):
    return self.matrix[y*self.matrixSize[0]+x]
  
  def fill(self, targetSet):
    for i in targetSet:
      print(i)
    
def fitSize(article):
  length = len(article)
  fitSize = min([i-length for i in size if length <= i], default=0)+length
  if fitSize not in size:
    return False
  
  return random.choice(size[fitSize])

def checkEmpty(page, width, height):
  fillSet = set([(i,e) for i,e in product(range(0, page.matrixSize[0]), range(0, page.matrixSize[1])) if page.isFilled(i,e)])
  for x, y in product(range(0, page.matrixSize[0]), range(0, page.matrixSize[1])):
    reqSet = set([(_x, _y) for _x in range(x, width+x) for _y in range(y, height+y)])
    if not(fillSet & reqSet):
      break 
  
  return reqSet
  
  
def maximumSize(article, page):
  size = fitSize(article)
  print(size)
  for x in range(page.matrixSize[0]):
    for y in range(page.matrixSize[1]):
      print(x,y)
  
def split(articles, page):
  fitArray = []
  articles = sorted(articles, key=lambda x:len(x))
  for article in articles:
    size = fitSize(article)
    if size:
      fitArray.append(maximumSize(article, page))
    else:
      print("no!")