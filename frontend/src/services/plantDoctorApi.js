import axios from 'axios';

const BASE_URL = import.meta.env.VITE_AI_API_URL || import.meta.env.VITE_API_URL || 'https://hydrogrow-ai-plant-doctor.onrender.com';

/**
 * Plant Doctor API Service for HydroGrow AI Render Backend Integration
 */
export const plantDoctorApi = {
  /**
   * Combined plant analysis scanner (Growth Stage, Growth Day, Nutrient Condition, Recommendations)
   * POST /api/vision/plant-analysis
   * @param {File} file - Plant leaf image file
   */
  async analyzePlantCombined(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BASE_URL}/api/vision/plant-analysis`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('API Error /api/vision/plant-analysis:', error);
      throw error.response?.data || { reason: error.message || 'Plant analysis failed.' };
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
      });
      return response.data;
    } catch (error) {
      console.error('API Error /api/vision/predict-growth:', error);
      throw error.response?.data || { reason: error.message || 'Growth prediction failed.' };
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
      });
      return response.data;
    } catch (error) {
      console.error('API Error /api/vision/predict-nutrient:', error);
      throw error.response?.data || { reason: error.message || 'Nutrient analysis failed.' };
    }
  },
};

export default plantDoctorApi;
