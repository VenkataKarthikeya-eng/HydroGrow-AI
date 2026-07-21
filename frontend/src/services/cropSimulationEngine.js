/**
 * HydroGrow AI - Crop Simulation Engine (Digital Twin Simulation)
 * Simulates hydroponic lettuce growth dynamics based on environmental parameters.
 */

/**
 * Optimal Ranges for Hydroponic Lettuce:
 * - Temperature: 20°C - 24°C
 * - Humidity: 60% - 75%
 * - EC: 1.8 - 2.5 mS/cm
 * - pH: 5.8 - 6.5
 */
export const OPTIMAL_RANGES = {
  temperature: { min: 20, max: 24, devScale: 0.08 },
  humidity: { min: 60, max: 75, devScale: 0.02 },
  ec: { min: 1.8, max: 2.5, devScale: 0.40 },
  ph: { min: 5.8, max: 6.5, devScale: 0.50 }
};

/**
 * Calculate individual environmental factors.
 * @param {Object} params - Environmental parameters { temperature, humidity, ec, ph }
 * @returns {Object} { temperatureFactor, humidityFactor, ecFactor, phFactor }
 */
export function calculateFactors(params = {}) {
  const {
    temperature = 22.0,
    humidity = 65,
    ec = 2.2,
    ph = 6.2
  } = params;

  const calcFactor = (val, min, max, devScale) => {
    if (val >= min && val <= max) return 1.0;
    const dev = val < min ? min - val : val - max;
    return Math.max(0.1, Math.min(1.0, 1.0 - dev * devScale));
  };

  const temperatureFactor = Number(calcFactor(temperature, OPTIMAL_RANGES.temperature.min, OPTIMAL_RANGES.temperature.max, OPTIMAL_RANGES.temperature.devScale).toFixed(4));
  const humidityFactor = Number(calcFactor(humidity, OPTIMAL_RANGES.humidity.min, OPTIMAL_RANGES.humidity.max, OPTIMAL_RANGES.humidity.devScale).toFixed(4));
  const ecFactor = Number(calcFactor(ec, OPTIMAL_RANGES.ec.min, OPTIMAL_RANGES.ec.max, OPTIMAL_RANGES.ec.devScale).toFixed(4));
  const phFactor = Number(calcFactor(ph, OPTIMAL_RANGES.ph.min, OPTIMAL_RANGES.ph.max, OPTIMAL_RANGES.ph.devScale).toFixed(4));

  return {
    temperatureFactor,
    humidityFactor,
    ecFactor,
    phFactor
  };
}

/**
 * Calculate overall growth multiplier combining environmental factors.
 * growthMultiplier = temperatureFactor * humidityFactor * ecFactor * phFactor
 * @param {Object} params - { temperature, humidity, ec, ph }
 * @returns {number} Growth multiplier
 */
export function calculateGrowthMultiplier(params = {}) {
  const factors = calculateFactors(params);
  const multiplier = factors.temperatureFactor * factors.humidityFactor * factors.ecFactor * factors.phFactor;
  return Number(multiplier.toFixed(4));
}

/**
 * Calculate expected yield prediction (harvest weight and percentage gain).
 * @param {Object|number} input - Parameter object or growth multiplier
 * @param {number} [baseWeight=310] - Baseline harvest weight of standard unoptimized control cycle (in grams)
 * @param {number} [maxOptimalWeight=380] - Maximum harvest weight achievable under optimal conditions (in grams)
 * @returns {Object} { expectedWeight, baselineWeight, yieldGainPercent }
 */
export function calculateYieldPrediction(input = {}, baseWeight = 310, maxOptimalWeight = 380) {
  const growthMultiplier = typeof input === 'number'
    ? input
    : calculateGrowthMultiplier(input);

  const expectedWeight = Math.max(50, Math.round(maxOptimalWeight * growthMultiplier));
  const yieldGainPercent = Math.round(((expectedWeight - baseWeight) / baseWeight) * 100);

  return {
    expectedWeight,
    baselineWeight: baseWeight,
    yieldGainPercent
  };
}

/**
 * Calculate estimated harvest day based on growth multiplier.
 * Standard baseline harvest is Day 28. Accelerated growth shortens time; stressed growth extends it.
 * @param {Object|number} input - Parameter object or growth multiplier
 * @param {number} [targetWeight=380] - Target harvest weight in grams
 * @returns {number} Harvest day number
 */
export function calculateHarvestDay(input = {}, targetWeight = 380) {
  const growthMultiplier = typeof input === 'number'
    ? input
    : calculateGrowthMultiplier(input);

  if (growthMultiplier <= 0) return 45;
  const baseHarvestDay = 28;
  const harvestDay = Math.min(45, Math.max(18, Math.round(baseHarvestDay / Math.sqrt(growthMultiplier))));
  return harvestDay;
}

/**
 * Generate intelligent biological recommendations based on environmental inputs.
 * @param {Object} params - { temperature, humidity, ec, ph }
 * @returns {Array<Object>} List of recommendation objects
 */
export function generateRecommendations(params = {}) {
  const {
    temperature = 22.0,
    humidity = 65,
    ec = 2.2,
    ph = 6.2
  } = params;

  const recs = [];

  // Temperature Recommendations
  if (temperature > 28) {
    recs.push({
      type: 'warning',
      category: 'Temperature',
      title: `High Air Temperature (${temperature}°C)`,
      message: 'Temperature is high. Reduce cooling load to improve lettuce growth.'
    });
  } else if (temperature < 18) {
    recs.push({
      type: 'warning',
      category: 'Temperature',
      title: `Low Air Temperature (${temperature}°C)`,
      message: 'Temperature is low. Increase temperature for faster growth.'
    });
  } else if (temperature < OPTIMAL_RANGES.temperature.min) {
    recs.push({
      type: 'warning',
      category: 'Temperature',
      title: `Sub-Optimal Air Temperature (${temperature}°C)`,
      message: `Temperature is slightly below optimal (${OPTIMAL_RANGES.temperature.min}-${OPTIMAL_RANGES.temperature.max}°C). Increase temperature for faster growth.`
    });
  } else if (temperature > OPTIMAL_RANGES.temperature.max) {
    recs.push({
      type: 'warning',
      category: 'Temperature',
      title: `Elevated Air Temperature (${temperature}°C)`,
      message: `Temperature exceeds ${OPTIMAL_RANGES.temperature.max}°C. Reduce heat load to improve lettuce growth.`
    });
  } else {
    recs.push({
      type: 'success',
      category: 'Temperature',
      title: `Optimal Air Temperature (${temperature}°C)`,
      message: `Air temperature is optimal (${OPTIMAL_RANGES.temperature.min}-${OPTIMAL_RANGES.temperature.max}°C) for lettuce growth.`
    });
  }

  // Humidity Recommendations
  if (humidity < OPTIMAL_RANGES.humidity.min) {
    recs.push({
      type: 'warning',
      category: 'Humidity',
      title: `Low Relative Humidity (${humidity}%)`,
      message: 'Increase humidity to reduce plant stress.'
    });
  } else if (humidity > OPTIMAL_RANGES.humidity.max) {
    recs.push({
      type: 'warning',
      category: 'Humidity',
      title: `High Relative Humidity (${humidity}%)`,
      message: 'Reduce humidity to prevent fungal pathogen growth and leaf rot.'
    });
  } else {
    recs.push({
      type: 'success',
      category: 'Humidity',
      title: `Optimal Relative Humidity (${humidity}%)`,
      message: `Relative humidity is within optimal range (${OPTIMAL_RANGES.humidity.min}-${OPTIMAL_RANGES.humidity.max}%).`
    });
  }

  // EC Recommendations
  if (ec < OPTIMAL_RANGES.ec.min) {
    recs.push({
      type: 'warning',
      category: 'EC',
      title: `Low Nutrient Concentration (EC ${ec} mS/cm)`,
      message: 'Increase nutrient concentration for better biomass.'
    });
  } else if (ec > OPTIMAL_RANGES.ec.max) {
    recs.push({
      type: 'warning',
      category: 'EC',
      title: `High Nutrient Concentration (EC ${ec} mS/cm)`,
      message: 'Reduce nutrient concentration to prevent root stress.'
    });
  } else {
    recs.push({
      type: 'success',
      category: 'EC',
      title: `Optimal Nutrient EC (${ec} mS/cm)`,
      message: `Nutrient concentration (EC ${OPTIMAL_RANGES.ec.min}-${OPTIMAL_RANGES.ec.max} mS/cm) is optimal.`
    });
  }

  // pH Recommendations
  if (ph < 5.5) {
    recs.push({
      type: 'warning',
      category: 'pH',
      title: `Acidic Solution pH (${ph})`,
      message: 'Increase pH.'
    });
  } else if (ph < OPTIMAL_RANGES.ph.min) {
    recs.push({
      type: 'warning',
      category: 'pH',
      title: `Slightly Acidic pH (${ph})`,
      message: 'Increase pH.'
    });
  } else if (ph > 7.0) {
    recs.push({
      type: 'warning',
      category: 'pH',
      title: `Alkaline Solution pH (${ph})`,
      message: 'Reduce pH.'
    });
  } else if (ph > OPTIMAL_RANGES.ph.max) {
    recs.push({
      type: 'warning',
      category: 'pH',
      title: `Slightly High pH (${ph})`,
      message: 'Reduce pH.'
    });
  } else {
    recs.push({
      type: 'success',
      category: 'pH',
      title: `Optimal Solution pH (${ph})`,
      message: `Solution pH is optimal (${OPTIMAL_RANGES.ph.min}-${OPTIMAL_RANGES.ph.max}) for nutrient uptake.`
    });
  }

  return recs;
}

/**
 * Main Digital Twin Crop Simulation function.
 * Calculates dynamic 30-day growth curve, yield prediction, harvest day, health score, and recommendations.
 * 
 * @param {Object} input - { temperature, humidity, ec, ph }
 * @returns {Object} { growthCurve, yield, harvestDay, healthScore, recommendations, factors }
 */
export function calculateGrowthSimulation(input = {}) {
  const {
    temperature = 22.0,
    humidity = 65,
    ec = 2.2,
    ph = 6.2
  } = input;

  const factors = calculateFactors({ temperature, humidity, ec, ph });
  const growthMultiplier = calculateGrowthMultiplier({ temperature, humidity, ec, ph });
  const yieldPrediction = calculateYieldPrediction(growthMultiplier);
  const harvestDay = calculateHarvestDay(growthMultiplier);
  const recommendations = generateRecommendations({ temperature, humidity, ec, ph });

  // Calculate health score (0-100) based on average of environmental factors
  const avgFactor = (factors.temperatureFactor + factors.humidityFactor + factors.ecFactor + factors.phFactor) / 4;
  const healthScore = Math.min(100, Math.max(0, Math.round(avgFactor * 100)));

  // Generate dynamic 30-day growth data
  // Starting weight at Day 1: 5g
  const initialWeight = 5;
  const simulatedFinalWeight = yieldPrediction.expectedWeight;

  const growthCurve = [];
  for (let day = 1; day <= 30; day++) {
    const progress = (day - 1) / 29;
    const weight = Math.max(initialWeight, Math.round(initialWeight + (simulatedFinalWeight - initialWeight) * Math.pow(progress, 2.2)));
    growthCurve.push({ day, weight });
  }

  return {
    growthCurve,
    yield: yieldPrediction,
    harvestDay,
    healthScore,
    recommendations,
    factors
  };
}

export default {
  calculateGrowthSimulation,
  calculateGrowthMultiplier,
  calculateYieldPrediction,
  calculateHarvestDay,
  generateRecommendations,
  calculateFactors,
  OPTIMAL_RANGES
};
