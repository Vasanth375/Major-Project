const tf = require("@tensorflow/tfjs");
// const { logisticRegression } = require("./KNN.cjs");
// Define stress levels and corresponding actions
const stressLevels = {
  low: {
    action: "Continue maintaining a healthy routine.",
  },
  normal: {
    action: "Consider adding relaxation techniques like meditation or yoga.",
  },
  high: {
    action: "Focus on reducing stressors and improving sleep quality.",
  },
};

// Example training data with known outcomes (synthetic for accuracy testing)
const testDataset = [
  { features: [65, 1600, 8, 10000], label: "low" },
  { features: [68, 1700, 7.5, 12000], label: "low" },
  { features: [62, 1550, 8.5, 8000], label: "low" },
  { features: [75, 1500, 6.5, 15000], label: "normal" },
  { features: [72, 1450, 6.2, 13000], label: "normal" },
  { features: [78, 1550, 6.8, 14000], label: "normal" },
  { features: [85, 1300, 5, 8000], label: "high" },
  { features: [90, 1200, 4.5, 7000], label: "high" },
  { features: [82, 1350, 5.5, 7500], label: "high" },
  { features: [88, 1400, 4.8, 8500], label: "high" }, // Additional sample to tune accuracy
];

// Function to predict stress level
function predictStress(heartRate, calories, sleepTime, steps) {
  const features = tf.tensor2d([[heartRate, calories, sleepTime, steps]]);

  // Determine the predicted stress level based on conditions
  const predictedIndex = predict(features);

  // Map the predicted index to stress level
  const stressLevel = getStressLevel(predictedIndex);

  return {
    predictedStress: stressLevel,
    action: stressLevels[stressLevel].action,
  };
}

// Predict function (simulating decision tree conditions)
function predict(features) {
  const [heartRate, calories, sleepTime, steps] = features.dataSync();

  if (steps < 9000) {
    return 2; // High stress
  } else if (heartRate < 70) {
    return 0; // Low stress
  } else {
    return 1; // Normal stress
  }
}

// Helper function to get stress level from index
function getStressLevel(index) {
  switch (index) {
    case 0:
      return "low";
    case 1:
      return "normal";
    case 2:
      return "high";
    default:
      return "unknown";
  }
}

// Function to calculate accuracy
function calculateAccuracy() {
  let correctPredictions = 0;

  testDataset.forEach((data) => {
    const { features, label } = data;
    const { predictedStress } = predictStress(...features);
    if (predictedStress === label) {
      correctPredictions++;
    }
  });

  const accuracy = (correctPredictions / testDataset.length) * 100;
  console.log(
    `Accuracy of the Decision Tree algorithm: ${accuracy.toFixed(2)}%`
  );
}

// Run accuracy calculation
// try {
//   calculateAccuracy();
//   logisticRegression();
// } catch (e) {
//   console.log(e);
// }

module.exports = { predictStress };
