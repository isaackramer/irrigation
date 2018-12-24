## Information from Aviva
- Email from Aviva about TDR data: Hi Isaac, I am sending a Google Drive link which consists of TDR data for May, June and July. Please check that it really downloaded the required time frame (its downloaded directly from the Meteo-tech server so I hope the required dates were actually downloaded). Pay attention that missing data (sensors which are not recording) is being input sometimes as zeroes or as hyphens (-) and not as "NULL", so these data must be removed in order not to insert errors into the analysis. I will be sending also swp data and irrigation data for that period.
- Other data: Units are: swp (mpa) irrigation (m3/dunam) / mm


## First look
### TDR Data:
- We have interfaces A, B, C, D, E, F, G, H, I, J (assuming these are locations in the field)
- For each "interface" there are three sensors. Corresponding to depth or location?
- Variables:
  - Volumetric water content $(\frac{V_w}{V_t})$, where $V_w$ is the volume of water and $V_t$ is the total volume of the soil (i.e., the volume of the solid, air, and water fractions together). A fully "saturated" soil (a soil where all of the pore space is occupied by water) would have a VWC of around 45.0.
  - Soil temperature (Celsius)
  - Permittivity: describes the amount of charge needed to generate one unit of electrical flux in a particular medium.
  - Bulk Electrical Conductivity (uS/cm): ECB is a consequence of highly complex interactions of soil physical and chemical properties, as texture (for instance, clay content), cation exchange capacity, organic matter, and soil water content (Alldred et al., 2008). Water content and electrical conductivity of the soil solution are the major factors affecting its bulk electrical conductivity (Friedman, 2005).
  - Pore Electrical Conductivity (uS/cm)
  - IRT: ??? Only available for a few of the interfaces
  - IRbodyT: ??? Only available for a few of the interfaces

Helpful for understanding the variables measured: https://www.stevenswater.com/resources/documentation/1922HilHorst.pdf
