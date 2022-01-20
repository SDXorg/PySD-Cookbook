[PySD Cookbook](http://pysd-cookbook.readthedocs.org/)
=============
## Simple recipes for powerful analysis of system dynamics models
*by James Houghton*

### Try out in Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JamesPHoughton/PySD-Cookbook/HEAD)

This cookbook is intended as a resource for system dynamics practitioners working to use big data to 
improve their modeling practice. I strive to make each recipe short, simple to understand, and transferable, 
so that the script can be copied and adapted to the desired problem.

Each recipe is structured as follows:

1. Introduction to the technique and its relevance to System Dynamics
2. Ingredients necessary to use the technique
 1. Description of the Demo Model
 2. Description of the Demo Data
 3. Notes on the particular third party python libraries in use
3. Steps necessary to conduct the analysis with code examples

### How to use this cookbook
An easily readable, linked version of this cookbook is available on [Read the Docs](http://pysd-cookbook.readthedocs.org/)

Every recipe in this cookbook is an executable ipython notebook. Because of this, I recommend that you download a copy of the cookbook, and follow along by executing the steps in each notebook as you read, playing with the parameters, etc.

If you want to implement a recipe, you can then make a copy of the notebook you are interested in, and modify it to analyze your own problem with your own data.

To download the cookbook in its entirity, use [this link](https://github.com/JamesPHoughton/PySD-Cookbook/archive/master.zip) or select one of the options in the righthand panel of the github window.

### Structure of this repository
As several recipes may use the same models or the same data, I've separated the recipes into a directory called [Analyses](https://github.com/JamesPHoughton/PySD-Cookbook/tree/master/analyses) where individual recipes are grouped by category. The [Data](https://github.com/JamesPHoughton/PySD-Cookbook/tree/master/data) directory contains all of the data used in the analyses, and in most cases notebooks describing the data, where it came from, and how it is formatted. The [Models](https://github.com/JamesPHoughton/PySD-Cookbook/tree/master/models) directory includes the various model files that are used throughout the analyses.
