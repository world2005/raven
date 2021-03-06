# Copyright 2017 Battelle Energy Alliance, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
frameworkDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(frameworkDir,'utils'))
from utils import utils
utils.find_crow(frameworkDir)
distribution1D = utils.find_distribution1D()
stochasticEnv = distribution1D.DistributionContainer.instance()
import math
normal1 = distribution1D.BasicNormalDistribution(0.5, 0.05, 0.0,1.0)

def initialize(self, runInfo, Input):
  self.Vb = 0.3
  self.Fb = 0.7
  self.Fr = 1

def run(self,Input):
  # sample f and d
  rand1  = stochasticEnv.random()
  rand2  = stochasticEnv.random()
  self.d = normal1.inverseCdf(rand1)
  self.f = normal1.inverseCdf(rand2)
  B      = self.B
  R      = self.R
  d      = self.d
  f      = self.f
  self.c = self.Fb * B + self.Vb * ( d - R * f ) + self.Fr * R
