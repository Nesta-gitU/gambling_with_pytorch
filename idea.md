1. get data for player locations over time for a bunch of games. 
2. use this as input into a neural network with pytorch 
3. train the network to predict if a goal will be scored in the next minutes
4. maybe make the first activation function learn from a family of distance measures. 

## ISSUES
1. as far as I know there is no priciple of certainty in neural networks (like confidence intervals in linear regression)
   so making the decision to bet or not bet might be tricky doing it this way. 
   solution could be to aim for very high (f1 idk the one that minimizes false positives) because falls negatives are just mist oportunities so dont cost money. 
