import unittest
import sys
sys.path.append("/home/wssh/feederPaper/")
sys.path.append("/home/wssh/feederPaper/src")

import random, string
import editor
from feedly import *

x = 'test<iframe allowfullscreen="allowfullscreen" src="https://kinja.com/ajax/inset/iframe?id=youtube-video-5AwFSSX34Wo&start=0" data-chomp-id="5AwFSSX34Wo" data-recommend-id="youtube://5AwFSSX34Wo" width="800" height="450"></iframe>+test2'
articles = ["".join([random.choice(string.ascii_lowercase) for i in range(random.choice([300, 500, 800, 1000]))]) for e in range(5)]
class Test(unittest.TestCase):
  def test_removeYoutube(self):
    _x = removeYoutube(x)
    self.assertEqual(_x, "test<span class=\"youtube\">youtube</span>+test2")
    print(_x)
 
  def test_splitSize(self):
    page = editor.Page()
#     editor.split(articles, page)

  def test_emptyCheck(self):
    page = editor.Page()
    targetSet = editor.checkEmpty(page, 1,2)
    
    page.fill(targetSet)
    
if __name__ == "__main__":
  unittest.main()
