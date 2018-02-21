from __future__ import division
import pandas as pd
import math

class Calculator:
    """A simple example class"""
    BSFC = 0.55
    INJ_NUMBER = 4
    INJ_PER_REV = 2
    INJ_FLOW_RATE = 52.4 # BOSH 550 cc/m = 52.4 lb/h
    INJ_FLOW_PSI_TESTED = 43.5
    INJ_DEAD_TIME = 1.151
    MINI_FUEL_REG_PSI = 55


    ACTUAL_INJ_FLOW_RATE = math.sqrt(INJ_FLOW_RATE/INJ_FLOW_PSI_TESTED)*INJ_FLOW_RATE


    pd.set_option('precision',10)

    #from kilogram per hour to gallons per hour
    def kghToGs(self, df):
        return pd.Series(df*0.277777777777778)

    def kghToLbh(selfself, df):
        return pd.Series(df*2.204623)

    # MAF = HP * AFR * BSFC / 60
    # MAF - Mass airflow rate in pounts per minute  (to covert kgh to lpm  -> kgh * 0.03674371)
    # HP - Horse Power at flywheel
    # AFR - Air fuel ratio
    # BSFC - break specific fuel consumption (pounds fuel per horsepower)
    def airmassKghToBhp(self, mafKgH, afr):
        hp = pd.Series((mafKgH*0.03674371)/(afr*(self.BSFC/60)))
        return hp/1.16

    def rpmToRadianPerSecond(self, rpm):
        return pd.Series(rpm * 0.1047198)

    def flowRateLbH(self,airmassLbh, afr):
        return pd.Series(airmassLbh/afr)

    def pulseFlowRate(self, pulsems , rpm):
        injFlowRateLbMs = (((self.ACTUAL_INJ_FLOW_RATE/60)/60)/1000) # per hour -> per minute (60) -> per second (60) -> per milisecond (1000)
        totalFlowRateLbMsPerRev = injFlowRateLbMs * self.INJ_PER_REV #  times 2 because we have 2 injections per rev


        actualFlowLbPerRev = totalFlowRateLbMsPerRev * (pulsems)
        flowPerMinute = actualFlowLbPerRev * rpm #lb per rev * revs per minutes = lb per min
        flowPerHr = flowPerMinute * 60
        return flowPerHr



