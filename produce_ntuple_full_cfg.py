import FWCore.ParameterSet.Config as cms 
from Configuration.StandardSequences.Eras import eras


process = cms.Process('DIGI',eras.Phase2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('/store/mc/PhaseIITDRFall17DR/SingleElectronPt5_100Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/00000/D85D8A36-08AE-E711-94A4-001E677923A0.root') )

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('SingleElectronPt10_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple.root")
    )

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)

# load ntuplizer
process.load('L1Trigger.L1THGCal.hgcalTriggerNtuples_cff')

process.ntuple_triggercells.FilterCellsInMulticlusters=cms.bool(False)
process.ntuple_clusters.FilterClustersInMulticlusters = cms.bool(False)
process.hgcalTriggerNtuplizer.Ntuples = cms.VPSet(
        process.ntuple_event,
        process.ntuple_gen,
        process.ntuple_genjet,
        process.ntuple_gentau,
        #process.ntuple_digis,
        process.ntuple_triggercells,
        process.ntuple_clusters,
        process.ntuple_multicluster
        )
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.ntuple_step)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

