# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:20:31 2022

@author: BIPIN
"""
import streamlit as st
from math import exp
import random
import time
from operator import add
import numpy as np
import matplotlib.pyplot as plt


st.title("Insurance Business Modelling and Basic Actuarial Calculations")
st.markdown("This application is a simple dashboard that is used to do risk and revenue assessment for an insurance company using Risk Process") 
st.markdown("##### Note: Input all the data as shown below and then switch to results and plotting because without data the variables will take default value")  
st.image('https://www.strimgroup.com/wp-content/uploads/2021/03/Underwriting-Analytics.png')    



with st.form(key="my_form"):
    MAXTIME = st.number_input("Enter Maximum Simulation Time Period")
    INCOME_INTENSITY = st.slider("Select Income Intensity Per Time Unit From 1 to 10", min_value=1, max_value=10)
    CLAIM_INTENSITY = st.slider("Select Time Between Claims From 1 to 10", min_value=1, max_value=10)   
    CLAIM_MEAN =  st.number_input("Enter Mean Of Claim", min_value = 0.1)    
    TRAJEC_NUM =  st.number_input("Enter Number Of Trajectories")
    seed_capital = st.number_input("Enter Seed Capital")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Your Data is stored Successfully")
    st.write("This is your data:")
    st.write("Your Maximum Simulation Time Period Is",  MAXTIME)
    st.write("Your Income Intensity Per Time Unit Is",  INCOME_INTENSITY)
    st.write("Your Time Between Claim Is",  CLAIM_INTENSITY)
    st.write("Your Mean Of Claim Is", CLAIM_MEAN)
    st.write("Your Number Of Trajectories Is",  TRAJEC_NUM)
    st.write("Your Seed Capital Is",  seed_capital)    

    
#MAXTIME = 10000          simulation period
#INCOME_INTENSITY = 1   income intensity per time unit
#CLAIM_INTENSITY = 1    time between claims is exponentially distributed 
#CLAIM_MEAN = 0.8        claims are exponentially distributed with CLAIM MEAN, should be >0
#TRAJEC_NUM = 100     number of trajectories simulated

def riskprocess_theo(seed_capital): 
  Ro=(INCOME_INTENSITY)/(CLAIM_INTENSITY*CLAIM_MEAN)-1
  if (Ro>0):
    RuinProb_Theo=exp(-Ro*seed_capital/((Ro+1)*CLAIM_INTENSITY))/(Ro+1) #Calculating Ruin Probability on infinite time interval
  else: RuinProb_Theo=1
  Mean_Theo=(1-RuinProb_Theo)*(seed_capital+(INCOME_INTENSITY-CLAIM_INTENSITY*CLAIM_MEAN)*MAXTIME) #Calculating Mean
  return [RuinProb_Theo,Mean_Theo] 

TRAJEC_NUM = int(TRAJEC_NUM)

def riskprocess(seed_capital): 
  RuinProb_MC = 0
  Mean_MC = 0
  i=0
  for i in range(TRAJEC_NUM):
    time = 0
    capital=seed_capital
    while (time < MAXTIME)and(capital>=0):
      time_step=random.expovariate(CLAIM_INTENSITY)
      time+=time_step
      capital += INCOME_INTENSITY * time_step - random.expovariate(1/CLAIM_MEAN)
    if (capital<0): #in case of ruin
      RuinProb_MC+=1/TRAJEC_NUM 
    else: 
      Mean_MC+=capital/TRAJEC_NUM # we add obtained capital if we do not ruin
  return [RuinProb_MC,Mean_MC]
    
[RuinProbMC,MeanMC]=riskprocess(seed_capital)
[RuinProb_Theo,Mean_Theo]=riskprocess_theo(seed_capital)
seed_capital_array = np.arange(0, 20, 2).tolist() # Generating Seed Capital array 
[RuinProbMCarray,MeanMCarray]=np.array([riskprocess(u) for u in seed_capital_array]).transpose() # Starting Monte Carlo simulation for each Seed Capital value
[RuinProbTheoarray,MeanTheoarray]=np.array([riskprocess_theo(u) for u in seed_capital_array]).transpose() # Applying theoretical fourmulas for each Seed Capital value
    

with st.form(key="my_form1", clear_on_submit=False):
    st.write("To Get Ruin Probability And The Mean Capital Earned, Click Below")
    Res = st.form_submit_button(label = "Click Here")
    
    if Res:
        st.markdown("## RESULTS")
        st.write("Resunts for MonteCarlo. Mean capital earned = ", MeanMC)
        st.write("Ruin Probability = ", RuinProbMC*100)
        st.write("Theoretical resuts Mean Value = ",Mean_Theo)
        st.write("Ruin Probability (infinite time) = ",RuinProb_Theo*100)
    
with st.form(key="my_form2", clear_on_submit=False):
    st.write("To Get Graphical Representation Of Seed Capital vs Ruin Probability & Expected Capital, Click Below")
    Res1 = st.form_submit_button(label = "Click Here")          
            
if Res1:    
    st.markdown("## Plotting")
            
    fig, ax = plt.subplots()
    ax.plot(seed_capital_array, RuinProbTheoarray, label = 'Theoretical Ruin Probability, $\infty $ time interval')
    ax.plot(seed_capital_array, RuinProbMCarray, label = 'Monte Carlo Ruin Probability')
    ax.set_ylabel('Ruin Probability')
    ax.set_xlabel('Seed Capital')
    ax.legend()
    fig.set_figheight(10)
    fig.set_figwidth(15)
    st.pyplot(fig)
            
    fig1, ax1 = plt.subplots()
    ax1.plot(seed_capital_array, MeanTheoarray, label = 'Theoretical Expected Capital')
    ax1.plot(seed_capital_array, MeanMCarray, label = 'Monte Carlo Expected Capital')
    ax1.set_ylabel('Expected Capital')
    ax1.set_xlabel('Seed Capital')
    ax1.legend()
    fig1.set_figheight(10)
    fig1.set_figwidth(15)
    st.pyplot(fig1)
