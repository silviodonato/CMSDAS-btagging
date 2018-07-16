import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 10,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('outputFilename', 'exerciseIPartI_histos.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 100)

options.parseArguments()

process = cms.Process("USER")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        '/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/5C8C50A4-EEF4-E711-962D-008CFA1C6564.root'    
        '/store/mc/RunIIFall17MiniAOD/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/50000/004C666D-C0E0-E711-AADB-0CC47A6C183A.root'    
    )
)

## Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(options.outputFilename)
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
    allowUnscheduled = cms.untracked.bool(True)
)

## Initialize analyzer
process.bTaggingExerciseIPartI = cms.EDAnalyzer('BTaggingExerciseI',
    jets = cms.InputTag('slimmedJets'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
         'pfCombinedInclusiveSecondaryVertexV2BJetTags',
	 'pfDeepCSVJetTags:probb',
	 'pfDeepCSVJetTags:probbb',
	 'pfDeepCSVJetTags:probc',
	 'pfDeepCSVJetTags:probudsg'	 	 	
    )
)

## Let it run
process.p = cms.Path(process.bTaggingExerciseIPartI)
