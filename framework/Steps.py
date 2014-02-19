'''
Module containing the different type of step allowed
Step is called by simulation
'''
#for future compatibility with Python 3--------------------------------------------------------------
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)
if not 'xrange' in dir(__builtins__):
  xrange = range
#End compatibility block for Python 3----------------------------------------------------------------

#External Modules------------------------------------------------------------------------------------
import time
import abc
import sys
#External Modules End--------------------------------------------------------------------------------

#Internal Modules------------------------------------------------------------------------------------
from BaseType import BaseType
from utils import metaclass_insert
import Distributions
import Models
#Internal Modules End--------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------
class Step(metaclass_insert(abc.ABCMeta,BaseType)):
  '''this class implement one step of the simulation pattern.
  Initialization happens when the method self is called
  A step could be used more times during the same simulation, if it make sense.

  --Instance--
  myInstance = Simulation(inputFile, frameworkDir,debug=False)
  myInstance.readXML(xml.etree.ElementTree.Element)

  --Usage--
  myInstance.takeAstep(self,inDictionary) nothing more, this initialize the step and run it. Call is coming from Simulation

  --Other external methods--
  myInstance.whoAreYou()                 -see BaseType class-
  myInstance.myInitializzationParams()   -see BaseType class-
  myInstance.myCurrentSetting()          -see BaseType class-

  --Adding a new step subclass--  
  <MyClass> should inherit at least from Step or from another step already presents

  DO NOT OVERRIDE any of the class method that are not starting with self.local*
  
  ADD your class to the dictionary __InterfaceDict at the end of the module

  The following method overriding is MANDATORY:
  self.localInputAndChecks(xmlNode)     : used to specialize the xml reading
  self.localAddInitParams(tempDict)     : used to add the local parameters and values to be printed
  self.localInitializeStep(inDictionary): called after this call the step should be able the accept the call self.takeAstep(inDictionary):
  self.localTakeAstepRun(inDictionary)  : this is where the step happens, after this call the output is ready
  '''

  def __init__(self):
    BaseType.__init__(self)
    self.parList    = []   # List of list [[role played in the step, class type, specialization, global name (user assigned by the input)]]
    self.__typeDict = {}   # For each role of the step the corresponding  used type
    self.sleepTime  = 0.1  # Waiting time before checking if a run is finished
    self.initSeed   = None #If a step possess re-seeding instruction it is going to ask to the sampler to re-seed according
                           #The option are:
                           #-a number to be used as a new seed
                           #-the string continue the use the already present random environment
                           #-None is equivalent to let the sampler to reinitialize

  def readMoreXML(self,xmlNode):
    '''add the readings for who plays the step roles
    after this call everything will not change further in the life of the step object should have been set
    @in xmlNode: xml.etree.ElementTree.Element containing the input to construct the step
    '''
    if 're-seeding' in xmlNode.attrib.keys():
      self.initSeed=xmlNode.attrib['re-seeding']
      if self.initSeed.lower()   == "continue": self.initSeed = "continue"
      else                                    : self.initSeed = int(self.initSeed)
    if 'sleepTime' in xmlNode.attrib.keys(): self.sleepTime = float(xmlNode.attrib['sleepTime'])
    for child in xmlNode:
      self.parList.append([child.tag,child.attrib['class'],child.attrib['type'],child.text])
    self.localInputAndChecks(xmlNode)
    if None in self.parList: raise Exception ('A problem was found in  the definition of the step '+str(self.name))

  @abc.abstractmethod
  def localInputAndChecks(self,xmlNode):
    '''place here specialized reading, input consistency check and 
    initialization of what will not change during the whole life of the object
    @in xmlNode: xml.etree.ElementTree.Element containing the input to construct the step
    '''
    pass
  
  def addInitParams(self,tempDict):
    '''Export to tempDict the information that will stay constant during the existence of the instance of this class'''
    tempDict['Sleep time'  ] = str(self.sleepTime)
    tempDict['Initial seed'] = str(self.initSeed)
    for List in self.parList:
      tempDict[List[0]] = ' Class: '+str(List[1])+' Type: '+str(List[2])+'  Global name: '+str(List[3])
    self.localAddInitParams(tempDict)

  @abc.abstractmethod
  def localAddInitParams(self,tempDict):
    '''place here a specialization of the exporting of what in the step is added to the initial parameters
    the printing format of tempDict is key: tempDict[key]'''
    pass

  def __initializeStep(self,inDictionary):
    '''the job handler is restarted and re-seeding action are performed'''
    inDictionary['jobHandler'].startingNewStep()
    self.localInitializeStep(inDictionary)
  
  @abc.abstractmethod
  def localInitializeStep(self,inDictionary):
    '''this is the API for the local initialization of the children classes'''
    pass

  @abc.abstractmethod
  def localTakeAstepRun(self,inDictionary):
    '''this is the API for the local run of a step for the children classes'''
    pass

  def takeAstep(self,inDictionary):
    '''this should work for everybody just split the step in an initialization and the run itself
    inDictionary[role]=instance or list of instance'''
    if self.debug: print('Initializing....')
    self.__initializeStep(inDictionary)
    if self.debug: print('Initialization done starting the run....')
    self.localTakeAstepRun(inDictionary)
#
#
#
class SingleRun(Step):
  '''This is the step that will perform just one evaluation'''
  def localInputAndChecks(self,xmlNode):
    found = 0
    for index, parameter in enumerate(self.parList):
      if parameter[0]=='Model':
        found +=1
        modelIndex = index
    if found !=1: raise IOError ('One model is needed for Single run!!!')
    toBeTested  = [{'role':myInput[0] ,'class':myInput[1],'type':myInput[2]} for myInput in self.parList if myInput[0]!='Model' ]
    print('the validation of the model in SingleRun needs to be done')
#    if not Models.validate(self.parList[modelIndex][1],toBeTested,'Run'):
#      raise IOError('The usage of the model '+self.parList[modelIndex][2]+' of type '+self.parList[modelIndex][1]+' is not correct')
    
  def localInitializeStep(self,inDictionary):
    '''this is the initialization for a generic step performing runs '''
    #checks
    print('remove the checks from the localInitializeStep by using the validation in localInputAndChecks')
    if 'Model'  not in inDictionary.keys(): raise IOError ('It is not possible a run without a model!!!')
    if 'Input'  not in inDictionary.keys(): raise IOError ('It is not possible a run without an Input!!!')
    if 'Output' not in inDictionary.keys(): raise IOError ('It is not possible a run without an Output!!!')
    #Model initialization
    inDictionary['Model'].initialize(inDictionary['jobHandler'].runInfoDict,inDictionary['Input'])
    if self.debug: print('The model '+inDictionary['Model'].name+' has been initialized')
    #HDF5 initialization
    for i in range(len(inDictionary['Output'])):
      try: #try is used since files for the moment have no type attribute
        if 'HDF5' in inDictionary['Output'][i].type: inDictionary['Output'][i].initialize(self.name)
        elif inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPrint']: inDictionary['Output'][i].initialize(inDictionary)
      except AttributeError as ae: print("Error1: "+repr(ae))
    
  def localTakeAstepRun(self,inDictionary):
    '''main driver for a step'''
    jobHandler = inDictionary['jobHandler']
    inDictionary["Model"].run(inDictionary['Input'],inDictionary['jobHandler'])
    if inDictionary["Model"].type == 'Code': 
      while True:
        finishedJobs = jobHandler.getFinished()
        for finishedJob in finishedJobs:
          if not finishedJob.getReturnCode() == 1:
            # if the return code is == 1 => means the system code crashed... we do not want to make the statistics poor => we discard this run
            newOutputLoop = False
            for output in inDictionary['Output']:                                                      #for all expected outputs
              if output.type not in ['OutStreamPlot','OutStreamPrint']:inDictionary['Model'].collectOutput(finishedJob,output,newOutputLoop=newOutputLoop) #the model is tasked to provide the needed info to harvest the output
              newOutputLoop = True
            for output in inDictionary['Output']:                                                      #for all expected outputs
              if output.type in ['OutStreamPlot','OutStreamPrint']:output.addOutput()                  #the model is tasked to provide the needed info to harvest the output
        if jobHandler.isFinished() and len(jobHandler.getFinishedNoPop()) == 0:
          break
        time.sleep(self.sleepTime)
    else:
      newOutputLoop = True
      for output in inDictionary['Output']:
        inDictionary['Model'].collectOutput(None,output,newOutputLoop=newOutputLoop)
        newOutputLoop = False

  def localAddInitParams(self,tempDict):
    print('localAddInitParams needs to be implemented in SingleRun')
#
#
#
class MultiRun(SingleRun):
  '''this class implement one step of the simulation pattern' where several runs are needed without being adaptive'''
  def __init__(self):
    SingleRun.__init__(self)
    self.maxNumberIteration = 0

  def localInputAndChecks(self,xmlNode):
    #checks
    SingleRun.localInputAndChecks(self,xmlNode)
    found = 0
    for parameter in self.parList:
      if parameter[0]=='Sampler': found +=1
    if found !=1: raise IOError ('One model is needed for Single run!!!')
 
  def addCurrentSetting(self,originalDict):
    originalDict['max number of iteration'] = self.maxNumberIteration

  def localInitializeStep(self,inDictionary):
    SingleRun.localInitializeStep(self,inDictionary)
    #checks
    if 'Sampler'  not in inDictionary.keys(): raise IOError ('It is not possible a multi-run without a Sampler!!!')
    #get the max number of iteration in the step
    if self.debug: print('The max the number of simulation is: '+str(self.maxNumberIteration))
    inDictionary['Sampler'].initialize(externalSeeding=self.initSeed)
    newInputs = inDictionary['Sampler'].generateInputBatch(inDictionary['Input'],inDictionary["Model"],inDictionary['jobHandler'].runInfoDict['batchSize'])
    for newInput in newInputs:
      inDictionary["Model"].run(newInput,inDictionary['jobHandler'])
      if inDictionary["Model"].type != 'Code':
        time.sleep(self.sleepTime) #it is here since models that are not codes do not have the quequing system
        # if the return code is == 1 => means the system code crashed... we do not want to make the statistics poor => we discard this run
        newOutputLoop = True
        for output in inDictionary['Output']:                                                      #for all expected outputs
          if output.type not in ['OutStreamPlot','OutStreamPrint']:inDictionary['Model'].collectOutput(None,output,newOutputLoop=newOutputLoop) #the model is tasked to provide the needed info to harvest the output
          newOutputLoop = False
        for output in inDictionary['Output']:                                                      #for all expected outputs
          if output.type in ['OutStreamPlot','OutStreamPrint']:output.addOutput()                  #the model is tasked to provide the needed info to harvest the output

  def localTakeAstepRun(self,inDictionary):
    jobHandler = inDictionary['jobHandler']
    while True:
      if inDictionary["Model"].type == 'Code': 
        finishedJobs = jobHandler.getFinished()
        #loop on the finished jobs
        for finishedJob in finishedJobs:
          if 'Sampler' in inDictionary.keys(): inDictionary['Sampler'].finalizeActualSampling(finishedJob,inDictionary['Model'],inDictionary['Input'])
          newOutputLoop = True
          for output in inDictionary['Output']:                                                      #for all expected outputs
              if output.type not in ['OutStreamPlot','OutStreamPrint']: inDictionary['Model'].collectOutput(finishedJob,output,newOutputLoop=newOutputLoop)                                #the model is tasked to provide the needed info to harvest the output
              newOutputLoop = False
          for output in inDictionary['Output']:                                                      #for all expected outputs
            if output.type in ['OutStreamPlot','OutStreamPrint']:output.addOutput()                               #the model is tasked to provide the needed info to harvest the output

          if 'ROM' in inDictionary.keys(): inDictionary['ROM'].trainROM(inDictionary['Output'])      #train the ROM for a new run
          for freeSpot in xrange(jobHandler.howManyFreeSpots()):                                     #the harvesting process is done moving forward with the convergence checks
            if inDictionary['Sampler'].amIreadyToProvideAnInput():
              newInput = inDictionary['Sampler'].generateInput(inDictionary['Model'],inDictionary['Input'])
              inDictionary['Model'].run(newInput,inDictionary['jobHandler'])
        if jobHandler.isFinished() and len(jobHandler.getFinishedNoPop()) == 0:
          break
        time.sleep(self.sleepTime)
      else:
        finishedJob = 'empty'
        if inDictionary['Sampler'].amIreadyToProvideAnInput():
          newInput = inDictionary['Sampler'].generateInput(inDictionary['Model'],inDictionary['Input'])
          inDictionary['Model'].run(newInput,inDictionary['jobHandler'])
          newOutputLoop = True
          for output in inDictionary['Output']:
            if output.type not in ['OutStreamPlot','OutStreamPrint']: inDictionary['Model'].collectOutput(finishedJob,output,newOutputLoop=newOutputLoop)
            newOutputLoop = False
          for output in inDictionary['Output']:
            if output.type in ['OutStreamPlot','OutStreamPrint']: output.addOutput()
        else:
          break
        time.sleep(self.sleepTime)
    #remember to close the rom to decouple the data stroed in the rom from the framework
    if 'ROM' in inDictionary.keys(): inDictionary['ROM'].close()
#
#
#
class Adaptive(MultiRun):
  '''this class implement one step of the simulation pattern' where several runs are needed in an adaptive scheme'''
  def localInputAndChecks(self,xmlNode):
    '''we check coherence of Sampler, Functions and Solution Output'''
    #test sampler information:
    foundSampler    = False
    samplCounter    = 0
    foundTargEval   = False
    targEvalCounter = 0
    solExpCounter   = 0
    functionCounter = 0
    foundFunction   = False
    for role in self.parList:
      if   role[0] == 'Sampler'         :
        foundSampler    =True
        samplCounter   +=1
        if not(role[1]=='Samplers' and role[2]=='Adaptive'): raise Exception('The type of sampler used for the step '+str(self.name)+' is not coherent with and adaptive strategy')
      elif role[0] == 'TargetEvaluation':
        foundTargEval   = True
        targEvalCounter+=1
        if role[1]!='Datas'                               : raise Exception('The data chosen for the evaluation of the adaptive strategy is not compatible,  in the step '+self.name)
        if not(['Output']+role[1:] in self.parList[:])    : raise Exception('The data chosen for the evaluation of the adaptive strategy is not in the output list for step'+self.name)
      elif role[0] == 'SolutionExport'  :
        solExpCounter  +=1
        if role[1]!='Datas'                               : raise Exception('The data chosen for exporting the goal function solution is not compatible, in the step '+self.name)
      elif role[0] == 'Function'       :
        functionCounter+=1
        foundFunction   = True
        if role[1]!='Functions'                           : raise Exception('A class function is required as function in an adaptive step, in the step '+self.name)
    if foundSampler ==False: raise Exception('It is not possible to run an adaptive step without a sampler in step '           +self.name)
    if foundTargEval==False: raise Exception('It is not possible to run an adaptive step without a target output in step '     +self.name)
    if foundFunction==False: raise Exception('It is not possible to run an adaptive step without a proper function, in step '  +self.name)
    if samplCounter   >1   : raise Exception('More than one sampler found in step '                                            +self.name)
    if targEvalCounter>1   : raise Exception('More than one target defined for the adaptive sampler found in step '            +self.name)
    if solExpCounter  >1   : raise Exception('More than one output to export the solution of the goal function, found in step '+self.name)
    if functionCounter>1   : raise Exception('More than one function defined in the step '                                     +self.name)
    
  def localInitializeStep(self,inDictionary):
    '''this is the initialization for a generic step performing runs '''
    #checks
    if 'Model'            not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without a model!'                     )
    if 'Input'            not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without an Input!'                    )
    if 'Output'           not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without an Output!'                   )
    if 'Sampler'          not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without an Sampler!'                  )
    if 'TargetEvaluation' not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without an a target for the function!')
    if 'Function'         not in inDictionary.keys(): raise IOError ('It is not possible run '+self.name+' step without an a function!'               )
    #Initialize model
    inDictionary['Model'].initialize(inDictionary['jobHandler'].runInfoDict,inDictionary['Input'])
    if self.debug: print('The model '+inDictionary['Model'].name+' has been initialized')
    #Initialize sampler
    if 'SolutionExport' in inDictionary.keys(): inDictionary['Sampler'].initialize(externalSeeding=self.initSeed,goalFunction=inDictionary['Function'],solutionExport=inDictionary['SolutionExport'])
    else                                      : inDictionary['Sampler'].initialize(externalSeeding=self.initSeed,goalFunction=inDictionary['Function'])
    if self.debug: print('The sampler '+inDictionary['Sampler'].name+' has been initialized')
    #HDF5 initialization
    for i in range(len(inDictionary['Output'])):
      try: #try is used since files for the moment have no type attribute
        if 'HDF5' in inDictionary['Output'][i].type:
          inDictionary['Output'][i].addGroupInit(self.name)
          if self.debug: print('The HDF5 '+inDictionary['Output'][i].name+' has been initialized')
        elif inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPlot']: inDictionary['Output'][i].initialize(inDictionary)
      except AttributeError as ae: print("Error2: "+repr(ae))    
    #the first batch of input is generated (and run if the model is not a code)
    newInputs = inDictionary['Sampler'].generateInputBatch(inDictionary['Input'],inDictionary["Model"],inDictionary['jobHandler'].runInfoDict['batchSize'])
    for newInput in newInputs:
      inDictionary["Model"].run(newInput,inDictionary['jobHandler'])
      if inDictionary["Model"].type != 'Code':
        # if the model is not a code, collect the output right after the evaluation => the response is overwritten at each "run"
        newOutputLoop = True
        for output in inDictionary['Output']: 
          if output.type not in ['OutStreamPlot','OutStreamPrint'] : inDictionary['Model'].collectOutput(inDictionary['jobHandler'],output,newOutputLoop=newOutputLoop)
          newOutputLoop = False
        for output in inDictionary['Output']: 
          if output.type in ['OutStreamPlot','OutStreamPrint'] : output.addOutput()

  def localTakeAstepRun(self,inDictionary):
    jobHandler = inDictionary['jobHandler']
    print('I am running')
    while True:
      if inDictionary["Model"].type == 'Code': 
        finishedJobs = jobHandler.getFinished()
        #loop on the finished jobs
        for finishedJob in finishedJobs:
          if 'Sampler' in inDictionary.keys(): inDictionary['Sampler'].finalizeActualSampling(finishedJob,inDictionary['Model'],inDictionary['Input'])
          if not finishedJob.getReturnCode() == 1:
            # if the return code is == 1 => means the system code crashed... we do not want to make the statistics poor => we discard this run
            newOutputLoop = True
            for output in inDictionary['Output']:                                                      #for all expected outputs
              if output.type not in ['OutStreamPlot','OutStreamPrint']:inDictionary['Model'].collectOutput(finishedJob,output,newOutputLoop=newOutputLoop) #the model is tasked to provide the needed info to harvest the output
              newOutputLoop = False
            for output in inDictionary['Output']:                                                      #for all expected outputs
              if output.type in ['OutStreamPlot','OutStreamPrint']:output.addOutput()                  #the model is tasked to provide the needed info to harvest the output
          if 'ROM' in inDictionary.keys(): inDictionary['ROM'].trainROM(inDictionary['Output'])      #train the ROM for a new run
          for freeSpot in xrange(jobHandler.howManyFreeSpots()):                                     #the harvesting process is done moving forward with the convergence checks
            if inDictionary['Sampler'].amIreadyToProvideAnInput(inLastOutput=inDictionary['TargetEvaluation']):
              newInput = inDictionary['Sampler'].generateInput(inDictionary['Model'],inDictionary['Input'])
              inDictionary['Model'].run(newInput,inDictionary['jobHandler'])
        if jobHandler.isFinished() and len(jobHandler.getFinishedNoPop()) == 0:
          break
        time.sleep(self.sleepTime)
      else:
        finishedJob = 'empty'
        if inDictionary['Sampler'].amIreadyToProvideAnInput(inLastOutput=inDictionary['TargetEvaluation']):
          newInput = inDictionary['Sampler'].generateInput(inDictionary['Model'],inDictionary['Input'])
          inDictionary['Model'].run(newInput,inDictionary['jobHandler'])
          newOutputLoop = False
          for output in inDictionary['Output']:
            if output.type not in ['OutStreamPlot','OutStreamPrint'] : inDictionary['Model'].collectOutput(inDictionary['jobHandler'],output,newOutputLoop=newOutputLoop)
            newOutputLoop = False
          for output in inDictionary['Output']:
            if output.type in ['OutStreamPlot','OutStreamPrint']     : output.addOutput()
        else:
          break
        time.sleep(self.sleepTime)
    #remember to close the rom to decouple the data stroed in the rom from the framework
    if 'ROM' in inDictionary.keys(): inDictionary['ROM'].close()
#
#
#
class InOutFromDataBase(Step):
  '''
    This step type is used only to extract or push information from/into a DataBase
    @Input, DataBase (for example, HDF5) or Datas
    @Output,Data(s) (for example, History) or DataBase
  '''
  def localInitializeStep(self,inDictionary):
    avail_out = ['TimePoint','TimePointSet','History','Histories']
    print('STEPS         : beginning of step named: ' + self.name)
    # check if #inputs == #outputs
    if len(inDictionary['Input']) != len(inDictionary['Output']):
      # This condition is an error if the n Inputs > n Outputs. if the n Outputs > n Inputs, it is an error as well except in case the additional outputs are OutStreams => check for this
      if len(inDictionary['Input']) < len(inDictionary['Output']):
        noutputs = len(inDictionary['Output'])
        for i in xrange(len(inDictionary['Output'])): 
          if inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPrint']: noutputs -= 1
        if len(inDictionary['Input']) != noutputs: raise IOError('STEPS         : ERROR: In Step named ' + self.name + ', the number of Inputs != number of Outputs')
      else: raise IOError('STEPS         : ERROR: In Step named ' + self.name + ', the number of Inputs != number of Outputs')
    self.actionType = []
    incnt = -1
    for i in range(len(inDictionary['Output'])):
      try: 
        if inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPrint']: 
          incnt -= 1
          continue
        else: incnt += 1
      except AttributeError as ae: pass
      if (inDictionary['Input'][incnt].type != 'HDF5'):
        if (not (inDictionary['Input'][incnt].type in ['TimePoint','TimePointSet','History','Histories'])): raise IOError('STEPS         : ERROR: In Step named ' + self.name + '. This step accepts HDF5 as Input only. Got ' + inDictionary['Input'][incnt].type)
        else:
          if(inDictionary['Output'][i].type != 'HDF5'): raise IOError('STEPS         : ERROR: In Step named ' + self.name + '. This step accepts ' + 'HDF5' + ' as Output only, when the Input is a Datas. Got ' + inDictionary['Output'][i].type)
          else: self.actionType.append('DATAS-HDF5')
      else:
        if (not (inDictionary['Output'][i].type in ['TimePoint','TimePointSet','History','Histories'])): raise IOError('STEPS         : ERROR: In Step named ' + self.name + '. This step accepts A Datas as Output only, when the Input is an HDF5. Got ' + inDictionary['Output'][i].type)
        else: self.actionType.append('HDF5-DATAS')
    databases = []
    for i in range(len(inDictionary['Output'])):
      try: #try is used since files for the moment have no type attribute
        if 'HDF5' in inDictionary['Output'][i].type:
          if inDictionary['Output'][i].name not in databases:
            databases.append(inDictionary['Output'][i].name)
            inDictionary['Output'][i].initialize(self.name)
        if inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPrint']: inDictionary['Output'][i].initialize(inDictionary)
      except AttributeError as ae: print("Error3: "+repr(ae))    
      
    
  def localTakeAstepRun(self,inDictionary):
    incnt = -1
    for i in range(len(inDictionary['Output'])):
      try: 
        if inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPrint']: 
          incnt -= 1
          continue
        else: incnt += 1
      except AttributeError as ae: pass
      if self.actionType[i] == 'HDF5-DATAS':
        inDictionary['Output'][i].addOutput(inDictionary['Input'][incnt])
      else: inDictionary['Output'][i].addGroupDatas({'group':inDictionary['Input'][incnt].name},inDictionary['Input'][incnt])
    for output in inDictionary['Output']:
      try: 
        if output.type in ['OutStreamPlot','OutStreamPrint']: output.addOutput() 
      except AttributeError as ae: pass
  
  def localAddInitParams(self,tempDict):
    pass # no inputs

  def localInputAndChecks(self,xmlNode):
    pass 
#
#
#
class RomTrainer(Step):
  '''This step type is used only to train a ROM
    @Input, DataBase (for example, HDF5)
  '''

  def addCurrentSetting(self,originalDict):
    Step.addCurrentSetting(self,originalDict)

  def localInitializeStep(self,inDictionary):
    '''The initialization step  for a ROM is copying the data out to the ROM (it is a copy not a reference) '''
    for i in xrange(len(inDictionary['Output'])):
      inDictionary['Output'][i].initializeTrain(inDictionary['jobHandler'].runInfoDict,inDictionary['Input'][0])
    try: #try is used since files for the moment have no type attribute
      if 'HDF5' in inDictionary['Output'][i].type: inDictionary['Output'][i].initialize(self.name)
      
      if inDictionary['Output'][i].type in ['OutStreamPlot','OutStreamPlot']: inDictionary['Output'][i].initialize(inDictionary)
    except AttributeError as ae: print("Error4: "+repr(ae))

  def takeAstepIni(self,inDictionary):
    print('STEPS         : beginning of step named: ' + self.name)
    for i in xrange(len(inDictionary['Output'])):
      if (inDictionary['Output'][i].type != 'ROM'):
        raise IOError('STEPS         : ERROR: In Step named ' + self.name + '. This step accepts a ROM as Output only. Got ' + inDictionary['Output'][i].type)
    if len(inDictionary['Input']) > 1: raise IOError('STEPS         : ERROR: In Step named ' + self.name + '. This step accepts an Input Only. Number of Inputs = ' + str(len(inDictionary['Input'])))
    self.localInitializeStep(inDictionary)
    
  def localTakeAstepRun(self,inDictionary):
    #Train the ROM... It is not needed to add the trainingSet since it's already been added in the initialization method
    for i in xrange(len(inDictionary['Output'])):
      inDictionary['Output'][i].train()
      inDictionary['Output'][i].close()
    return

  def localAddInitParams(self,tempDict):
    #TODO implement
    pass

  def localInputAndChecks(self,xmlNode):
    #TODO implement
    pass
#
#
#
__interFaceDict                      = {}
__interFaceDict['SingleRun'        ] = SingleRun
__interFaceDict['MultiRun'         ] = MultiRun
#__interFaceDict['SCRun'            ] = SCRun
__interFaceDict['Adaptive'         ] = Adaptive
__interFaceDict['InOutFromDataBase'] = InOutFromDataBase 
__interFaceDict['RomTrainer'       ] = RomTrainer
__base                               = 'Step'

def returnInstance(Type):
  return __interFaceDict[Type]()
  raise NameError('not known '+__base+' type '+Type)
  
