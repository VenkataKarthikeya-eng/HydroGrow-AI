import assert from 'node:assert';
import {
  calculateGrowthSimulation,
  calculateGrowthMultiplier,
  calculateYieldPrediction,
  calculateHarvestDay,
  generateRecommendations,
  calculateFactors
} from './cropSimulationEngine.js';

console.log('Running Crop Simulation Engine Tests...');

// Test 1: Optimal Baseline Input
const optimalInput = { temperature: 22.0, humidity: 65, ec: 2.2, ph: 6.2 };
const optimalSim = calculateGrowthSimulation(optimalInput);

assert.strictEqual(optimalSim.healthScore, 100, 'Optimal health score should be 100');
assert.strictEqual(optimalSim.factors.temperatureFactor, 1.0);
assert.strictEqual(optimalSim.factors.humidityFactor, 1.0);
assert.strictEqual(optimalSim.factors.ecFactor, 1.0);
assert.strictEqual(optimalSim.factors.phFactor, 1.0);
assert.strictEqual(optimalSim.yield.expectedWeight, 380);
assert.strictEqual(optimalSim.yield.baselineWeight, 310);
assert.strictEqual(optimalSim.yield.yieldGainPercent, 23, 'Optimal parameters should produce +23% positive yield improvement');
assert.strictEqual(optimalSim.harvestDay, 28);
assert.strictEqual(optimalSim.growthCurve.length, 30);
assert.strictEqual(optimalSim.growthCurve[0].day, 1);
assert.strictEqual(optimalSim.growthCurve[0].weight, 5);
assert.strictEqual(optimalSim.growthCurve[29].day, 30);
assert.strictEqual(optimalSim.growthCurve[29].weight, 380);

console.log('✔ Test 1 Passed: Optimal Baseline');

// Test 2: Sub-optimal Input (Cold, Low Humidity, Low EC, Acidic pH)
const subOptimalInput = { temperature: 16.0, humidity: 45, ec: 1.2, ph: 5.0 };
const subOptimalSim = calculateGrowthSimulation(subOptimalInput);

assert.ok(subOptimalSim.healthScore < 100, 'Sub-optimal health score should be less than 100');
assert.ok(subOptimalSim.factors.temperatureFactor < 1.0);
assert.ok(subOptimalSim.factors.humidityFactor < 1.0);
assert.ok(subOptimalSim.factors.ecFactor < 1.0);
assert.ok(subOptimalSim.factors.phFactor < 1.0);
assert.ok(subOptimalSim.yield.expectedWeight < 310, 'Sub-optimal yield weight should be lower than baseline 310g');
assert.ok(subOptimalSim.yield.yieldGainPercent < 0, 'Sub-optimal parameters should produce negative yield improvement');
assert.ok(subOptimalSim.harvestDay > 28, 'Sub-optimal harvest day should be longer than 28 days');

console.log('✔ Test 2 Passed: Sub-optimal parameters lower health, yield & extend harvest day');

// Test 3: High Temperature Stress
const heatStressInput = { temperature: 30.0, humidity: 65, ec: 2.2, ph: 6.2 };
const heatSim = calculateGrowthSimulation(heatStressInput);

assert.ok(heatSim.factors.temperatureFactor < 1.0);
assert.strictEqual(heatSim.factors.humidityFactor, 1.0);

console.log('✔ Test 3 Passed: Individual factor response');

// Test 4: Different Inputs Return Different Outputs
assert.notDeepStrictEqual(optimalSim, subOptimalSim, 'Different inputs must produce different outputs');
assert.notStrictEqual(optimalSim.yield.expectedWeight, subOptimalSim.yield.expectedWeight);
assert.notStrictEqual(optimalSim.harvestDay, subOptimalSim.harvestDay);
assert.notStrictEqual(optimalSim.healthScore, subOptimalSim.healthScore);

console.log('✔ Test 4 Passed: Input variance produces distinct outputs');

// Test 5: Verify recommendations generation
const recs = generateRecommendations(subOptimalInput);
assert.ok(Array.isArray(recs) && recs.length === 4, 'Should generate 4 recommendation items');
assert.ok(recs.some(r => r.category === 'Temperature' && r.message === 'Temperature is low. Increase temperature for faster growth.'));
assert.ok(recs.some(r => r.category === 'Humidity' && r.message === 'Increase humidity to reduce plant stress.'));
assert.ok(recs.some(r => r.category === 'EC' && r.message === 'Increase nutrient concentration for better biomass.'));
assert.ok(recs.some(r => r.category === 'pH' && r.message === 'Increase pH.'));

// Test 6: Verify High Parameters Recommendations
const highInput = { temperature: 30.0, humidity: 85, ec: 3.0, ph: 7.5 };
const highRecs = generateRecommendations(highInput);
assert.ok(highRecs.some(r => r.category === 'Temperature' && r.message === 'Temperature is high. Reduce cooling load to improve lettuce growth.'));
assert.ok(highRecs.some(r => r.category === 'Humidity' && r.message === 'Reduce humidity to prevent fungal pathogen growth and leaf rot.'));
assert.ok(highRecs.some(r => r.category === 'EC' && r.message === 'Reduce nutrient concentration to prevent root stress.'));
assert.ok(highRecs.some(r => r.category === 'pH' && r.message === 'Reduce pH.'));

console.log('✔ Test 5 & 6 Passed: Dynamic Intelligent Recommendations');

console.log('ALL CROP SIMULATION ENGINE TESTS PASSED SUCCESSFULLY!');
