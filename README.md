# House Market Analysis with Interactive Interface
<p> Author : Ricardo Barbosa de Almeida Campos </p>

<img src  = "https://nationalmortgageprofessional.com/sites/default/files/Housing_Market_Decline_Pic.jpg">

## Introduction
<p>This is an data science insight project that has as an objective to validate a buying and selling strategy of assets inside the housing market utilizing an analysis tool. So in this project, an scenario was created to illustrate that said tool is capable of delivering insights that can be turned in real life value. </p>

## Business Problem
<p>In each there are numerous possibilities for buying and selling properties with the intention of making a profit, but since the number of assets is quite high, this task becomes very difficult without some kind assistance. So a company called House Rocket, based in the Seattle area, ordered the development of tool to boost their performance in the housing market, since it would enable the business team to make  faster and more asserted decisions.</p>
<p>Some premises were taken into consideration before starting this project:
  <ul>
    <li> Prices above U$ 100.000.000,00 were discarded</li>
    <li> Houses with waterfront view were at least 2X more expensive than houses with no waterfront view</li>
    <li> Most of the properties are in good condition</li>
  </ul></p>

## Dataset
<p>The dataset was fetched in the following link :<a href = "https://www.kaggle.com/datasets/shivachandel/kc-house-data"> Housing Market Dataset</a></p>
<p>A more detailed description of said dataset can be found in the link.</p>

## Business Solution
<p>As mentioned before, to help with the problem that the business team is facing an interactive analysis tool was developed that is capable of filter data and present tables, plots and maps that can be used to provide insights.</p><p>For more accessibility, the tool will be available online and can be accessed anywhere the people responsible might need.</p>

## Businees Insight
<p>During the development the interactive tool, some insights that might the business team were found. They are as follow:
  <ul>
    <li> Houses with Waterfront view on average are 4x more expensive that those with no waterfront view</li>
    <li> There are no discernable price difference between houses in regards the year that they were built</li>
    <li> Properties with no basement on average have only 20% more lot area that those with no basement</li>
    <li> The Year over Year price fluctuation was near 0 between the years of 2014 and 2015 built</li>
    <li> The highest Month over Month price fluctuation was 10% and the lowest was -14% and there was no considerable rise in average               price during the period </li>
    <li> Houses that are bought during summer and spring on average are 5% to 10% more expensive compared to other seasons</li>
  </ul></p>

  ## Financial Results
  <p>An operating strategy was developed with the assist of the interactive analysis tool. Said strategy can be divided in two stages:   deciding which to buy and defining the selling price </p>

  ### Buying Strategy
  <p> The buying strategy consists of the following points :
  <ul>
    <li> Collecting data </li>
    <li> Grouping by zip code </li>
    <li> Finding the medians for each group </li>
    <li> The houses that the price were below the median for the group will be suggested to be bought</li>
  </ul>  
  </p>

   ### Selling Strategy
  <p> The selling strategy consists of the following points :
  <ul>
    <li> Collecting data from the Buying Strategy </li>
    <li> Find in which season the house was bought </li>
    <li> Adding 30% to the buying price the house is good condition, was bought during winter of autumn and the price was below the median     </li>
    <li> Adding 10% to houses that did not fit any of criteria mentioned above, since their buying price higher and applying the same    profit margin might make the house very hard to sell </li>
  </ul>  
  </p>


  ## Financial Results
  <p>Using the strategy mentioned in the paragraphs above an profit around U$ 3,794,940.00 would be expected.</p>


  ## Conclusion
  <p>The interactive analysis tool for the housing market meet their expectation of delivering financial results for the House Rocket company and assist in faster decision making for the business team.</p>
  <p>The tool can be accessed using the following link :<a href = "https://house-rocket-analytics-ricardo.herokuapp.com/"> Analysis Tool</a></p>
