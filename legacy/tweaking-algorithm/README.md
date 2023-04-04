# Folder structure:

Main idea: the Deep Reinforcement Learning part has 2 main components:
<ul>
<li>The agent: basically an intelligent entity. Once placed in a environment, it can learn from it to maximise the reward provided by it. The idea is to optimise the learning function of the agent to be adapted to our problem</li>
<li>Environments: where the agent will be placed. The environment can be acted upon by the agent, be affected accordingly and will output the corresponding reward. Our task is to design a environment that correctly reflects our protein models, and provided a good reward at each step.</li>
</ul>

## Core (root folder)

The core_training.py and core_prediction.py are the main files of the Deep RL parts. The former implements the training part, where the agent infinitely trains (trapped in a while true loop). The neural network weights are regularly saved in the saved_weights folder so that they can be used by the prediction part.

## Learning Environments (folder invenv)

Custom package made using OpenAI gym that contains all the necessary environments to train the agent.  
Currently, there implemented environments are:

<ol>
<li>Primitive Environment: mainly a debugging/dummy environment</li>
<li>Tweaking Environment: environment that implement the "tweaking" learning idea</li>
</ol>

The strcture is strange but it is to follow the standard implementation explained in the official documentation.

## Testing Area

Contains the UI that is used to emulate agent-environment interactions. This UI is mainly useful for debugging purposes and to test the environments before moving to the next stage of the process, which combining an agent and an environment for the training part.




