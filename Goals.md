# Overall goal
- To look at how irrigation patterns affect soil moisture (VWC), plant health (SWP), and other variables

## Sub-goals

### 1. Clean the data

#### Done so far
- Remove "0" and "-" values from data
- Modified SWP and Irrigation csvs so that they can be plotted together with VWC.
- Removed bad data

#### Needs to be done
- Can we smooth curves?

## 3. Clustering/Community Detection.
Can we determine which soils behave most similarly? For each sensor we have data for the following variables: Water Content, Temperature, and Electrical Conductivity. If we make these three values a vector (i.e., one vector per sensor per time step) can we identify soils that are most similar to each other?

I think dynamic time warping could be the best tool for this goal. If this can't be done using a vector of variables, let's try it just for the water content.

Once we determine which soils are most similar, we can try and determine if they have similar patterns in the stem water potential.

### 4. Affects of slope and soil depth on rate of drying
If you look at the plots of the water content, you will notice that some soils appear to dry much faster after they were irrigated than others. As an example, look at the plots for areas C and D. Area C appears to lose water much faster than Area D.

We now have data for the slope and soil depth at each of the sensors. Can we try and explain the rate at which the soils by using these two variables?


### Scatter plots
- Leaf water vs. Soil water content
- Soil water content vs. irrigation input
