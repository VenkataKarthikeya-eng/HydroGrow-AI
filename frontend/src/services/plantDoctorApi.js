import axios from 'axios';

const BASE_URL = (import.meta.env.VITE_AI_API_URL && import.meta.env.VITE_AI_API_URL.trim() !== '') 
  ? import.meta.env.VITE_AI_API_URL 
  : (import.meta.env.VITE_API_BASE_URL || 'https://hydrogrow-ai-plant-doctor.onrender.com');
const TIMEOUT_MS = 45000; // 45 second timeout to allow for Render free tier cold-start model loading

/**
 * Plant Doctor API Service for HydroGrow AI Render Backend Integration
 */
export const plantDoctorApi = {
  /**
   * Combined plant analysis scanner (Growth Stage, Growth Day, Nutrient Condition, Recommendations)
   * POST /api/vision/plant-analysis
   * @param {File} file - Plant leaf image file
   */
  async analyzePlantCombined(file, onRetryNotice = null) {
    const makeRequest = async () => {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post(`${BASE_URL}/api/vision/plant-analysis`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: TIMEOUT_MS,
      });
      return response.data;
    };

    // Attempt 1: Maximum 45 seconds timeout
    try {
      return await makeRequest();
    } catch (error1) {
      console.warn('Plant Doctor Attempt 1 failed:', error1.message || error1);

      const isTimeout = error1.code === 'ECONNABORTED' || error1.message?.includes('timeout') || !error1.response;

      if (isTimeout) {
        if (onRetryNotice) {
          onRetryNotice('Render AI server was cold-starting. Retrying connection in 5 seconds (Attempt 2)...');
        }
        // Wait 5 seconds before Attempt 2
        await new Promise((resolve) => setTimeout(resolve, 5000));

        // Attempt 2: Maximum 45 seconds timeout
        try {
          if (onRetryNotice) {
            onRetryNotice('Re-connecting to Render AI Server (Attempt 2)...');
          }
          return await makeRequest();
        } catch (error2) {
          console.error('Plant Doctor Attempt 2 failed:', error2.message || error2);
          if (error2.response?.data && typeof error2.response.data === 'object') {
            throw error2.response.data;
          }
          throw { 
            code: 'ECONNABORTED', 
            reason: 'Render AI server cold-start timeout after 2 attempts. Render free instance may need extra time to wake up.' 
          };
        }
      }

      if (error1.response?.data && typeof error1.response.data === 'object') {
        throw error1.response.data;
      }
      throw { reason: error1.message || 'Plant analysis failed due to network error.' };
    }
  },

  /**
   * Predict growth stage and growth day
   * POST /api/vision/predict-growth
   * @param {File} file - Plant leaf image file
   */
  async predictGrowth(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BASE_URL}/api/vision/predict-growth`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: TIMEOUT_MS,
      });
      return response.data;
    } catch (error) {
      console.error('API Error /api/vision/predict-growth:', error);
      if (error.response?.data) {
        throw error.response.data;
      }
      if (error.code === 'ECONNABORTED') {
        throw { code: 'ECONNABORTED', reason: 'Connection timeout while predicting growth stage.' };
      }
      throw { reason: error.message || 'Growth prediction failed.' };
    }
  },

  /**
   * Predict nutrient condition
   * POST /api/vision/predict-nutrient
   * @param {File} file - Plant leaf image file
   */
  async predictNutrient(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BASE_URL}/api/vision/predict-nutrient`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: TIMEOUT_MS,
      });
      return response.data;
    } catch (error) {
      console.error('API Error /api/vision/predict-nutrient:', error);
      if (error.response?.data) {
        throw error.response.data;
      }
      if (error.code === 'ECONNABORTED') {
        throw { code: 'ECONNABORTED', reason: 'Connection timeout while evaluating nutrient deficiency.' };
      }
      throw { reason: error.message || 'Nutrient analysis failed.' };
    }
  },
};

export default plantDoctorApi;
