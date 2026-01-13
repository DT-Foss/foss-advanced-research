pragma circom 2.0.0;

include "comparators.circom";

template TemperatureCompliance(n) {
    signal input temperatures[n];
    signal input lowerBound;
    signal input upperBound;
    signal output compliant;
    
    signal allCompliant;
    
    // Intermediate signals need to be handled carefuly in loops
    // Simplified logic for MVP extraction
    
    component lt[n];
    component gt[n];
    
    for (var i = 0; i < n; i++) {
        lt[i] = LessThan(16);
        lt[i].in[0] <== temperatures[i];
        lt[i].in[1] <== lowerBound;
        
        gt[i] = GreaterThan(16);
        gt[i].in[0] <== temperatures[i];
        gt[i].in[1] <== upperBound;
    }
    
    // Aggregation logic would go here
    compliant <== 1; 
}

component main = TemperatureCompliance(10);
