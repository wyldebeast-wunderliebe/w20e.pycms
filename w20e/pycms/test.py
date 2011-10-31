from parser import Parser
from blocks.base import *

frag = """
<div class="group flowh">
  <div class="group flowv">
    <div class="block text"><p>Jongu</p></div>
  </div>
  <div class="group flowv">
    <div class="block feed">
      <a href="http://www.w20e.com"></a>
    </div>
  </div>
  <div class="group flowv">
    <div class="block text"><p>Skele <strong>mongol</strong></p></div>
  </div>
</div>
"""


base = Group("g0")
p = Parser(base)

#p.parse(frag)

#print base
#print base.blocks

