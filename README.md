<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->




<!-- PROJECT LOGO -->
<br />
<div align="center">


  <h1 style= font-size: 150px align="center">Sigmafold</h1>

  <p align="center">
    Solving the inverse protein folding using Machine Learning techniques, step by step.
    <br />
    <a href="https://www.notion.so/SigmaFold-ce3f051d258c4eba8e7edd5cf590055f"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Introduction

Inverse protein folding is the problem of finding the structure of a protein from its amino acid sequence. In this project, we are using the HP lattice model to approach the 2D inverse protein folding problem. The HP lattice model is a simple model in which the protein sequence is represented as a string of two types of amino acids, H and P, with H representing hydrophobic (water-fearing) residues and P representing hydrophilic (water-loving) residues.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Approaches

In this project, we are proposing two approaches to solve the inverse protein folding problem:


### Placing Algorithm

The placing algorithm takes as input a Hamiltonian path, corresponding to a desired shape of the protein, and learns to place Hs and Ps in strategic locations to get the sequence with the minimum degeneracy. This will be done using Deep Reinforcement Learning, and a training dataset will be used to define its reward function. The idea is to find all heuristic rules that encompass the placement of Hs and Ps on the lattice and use that to extrapolate to higher sequence lengths. This algorithm uses Deep Q-Learning, and a custom dataset that we have generated and stored on Supabase.

### Tweaking Algorithm

The tweaking algorithm is similar to the placing algorithm, although it takes as input a sequence that is "close to the goal" and tweaks specific Hs or Ps to improve the overall sequence.

## Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python 3.x
* Required packages specified in the requirements.txt file

To install the required packages, run the following command:
  ```sh
pip install -r requirements.txt
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Nicolas: njd20@ic.ac.uk (repo owner), feel free to send me an email if you have any suggerstions or are interested in contributing!
Other Contributors: Gloria, Alex, Joshua, Nabeel, Mateusz from the Imperial College London Department of Bioengineering.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Dr. Thomas Ouldridge - https://www.imperial.ac.uk/people/t.ouldridge


<p align="right">(<a href="#readme-top">back to top</a>)</p>

