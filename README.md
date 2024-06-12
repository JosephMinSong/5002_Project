<h1 align="center">Probability & Prediction: Bicycle-Car Collision Risk in Seattle. A Predictive Model using Naive-Bayes Model Regression and Logistic Learning Models</h1>

<h1 align="center">Preprocessing Data</h1>
<p>Our project aims to analyze cyclist accidents in downtown Seattle spanning from 2016 to 2023, focusing on factors such as weather, light, and road conditions in relation to accident probability.</p>
<p>Our primary objective is to build a machine learning model capable of accurately predicting whether a cycling accident was going to occur, given a set of environmental circumstances.</p>
<p>After downloading public incident reports from the City of Seattle website, we initially parsed the data from a CSV file.</p>
<p>After developing and using algorithms to parse the data and making sure we had complete weather, road, and light conditions, we organized the data to fit our models.</p>

<div align="center">
  <img src="https://github.com/JosephMinSong/5002_Project/assets/129890601/c3de2c16-7c15-4de3-8e43-0dcae6711986" />
  <p>Figure 1: Screenshot of report illustrating total incident count, total cycling incidents, adjusted incidents and percentages, and all environment variables in the database</p>
</div>

<p>Out of the 189908 viable incidents that had a complete set of environment data, only 6325 were cycling incidents, giving us a 3.33% cycling incident rate. 
  Because there was an obvious bias towards non-cycling accidents, the data was balanced by reducing non-cycling accidents by a quarter, increasing the cycling accident percentage to 13.32% to better suit the Naive-Bayes learning model. 
</p>

<h1 align="center">Developing Naive Bayes calculation</h1>

<div align="center">
  <img src="https://github.com/JosephMinSong/5002_Project/assets/129890601/864f905a-7b13-4cc8-9efd-5fa954ee5e59" />
  <p>Figure 2: Applied Bayes Theorem Equation</p>
</div>

Where: 
<ul>
  <li>A1 is a weather condition happening</li>
  <li>B1 is a cycling accident</li>
  <li>B2 is not a cycling accident</li>
  <li>P(B1 | A1) is the probability of a cycling accident occurring given a weather condition</li>
  <li>P(A1 | B1) is the probability of a weather condition occurring given an accident has occurred</li>
  <li>P(B1) is the probability of a cycling accident occurring</li>
  <li>P(A1 | B2) is the probability of a weather condition occurring given there is no accident</li>
</ul>

<h3 align="left">Naive-Bayes Probability Results</h3>

<div align="center">
  <img src="https://github.com/JosephMinSong/5002_Project/assets/129890601/28b0b27e-0309-411b-99f0-9ef3bbeefdf3" />
  <p>Figure 3: Accidents occurring given an environment condition probabilities using Naive Bayes theorem</p>
</div>

<h1 align="center">Model Building</h1>

<h3>Model Performances: </h3>
<div align="center" display="flex-grow">
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/6ca095b8-e9c7-4919-b097-6bc2753aa891" />
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/80509dda-3f64-4db7-8a87-13447bd7f5e7" />
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/37f1897b-fec0-4736-85de-b1cef152d5c0" />
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/c7b93641-8f00-4e97-865e-19e31650ae67" />
</div>
<p align="center">Figure 4: Plot of Confusion Matrix for Visual Representation of Multinomial, Guassian, Bernoulli, and Complement NB Model Performances</p>

<h3>Model Comparison: </h3>
<div align="center">
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/469c6792-9b5f-4f5b-8c6a-37808ee599b6" />
  <img width="450" src="https://github.com/JosephMinSong/5002_Project/assets/129890601/9a47a967-f825-46ef-b06d-ed44b5f08674" />
</div>
<p align="center">Figure 5: Class 0 (No Accident Cases) and 1 (Accident Cases) comparison graph comparing accuracy, precision, and recall percentages across the different models</p>


