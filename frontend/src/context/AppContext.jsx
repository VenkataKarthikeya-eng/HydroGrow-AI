import React, { createContext, useState, useEffect } from 'react';
import client from '../api/client';
import { predictGrowth } from '../api/predictionApi';
import { sendMessage } from '../api/assistantApi';

export const AppContext = createContext();

const DEFAULT_INPUTS = {
  air_temperature: 22.0,
  humidity: 60.0,
  co2: 450.0,
  water_ph: 6.2,
  water_ec: 2.0,
  water_temperature: 23.0,
  nutrient_solution: 400.0,
  water_consumption: 170.0,
  seedling_height: 12.0,
  seedling_weight: 4.0,
  root_length: 7.0
};

export const AppProvider = ({ children }) => {
  // Load token from localStorage
  const [token, setToken] = useState(() => localStorage.getItem('hydrogrow_token'));
  
  // Theme State
  const [theme, setTheme] = useState(() => localStorage.getItem('hydrogrow_theme') || 'light');

  // Dynamic User Profile Context
  const [user, setUser] = useState({
    name: 'Karthikeya',
    farmName: 'Demo Hydro Farm',
    role: 'Lead Grower',
    email: 'karthikeya@hydrogrow.ai'
  });

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    localStorage.setItem('hydrogrow_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  // Auth state
  const [userProfile, setUserProfile] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Prediction Inputs & calculated results
  const [predictionInputs, setPredictionInputs] = useState(() => {
    const saved = localStorage.getItem('hydrogrow_inputs');
    return saved ? JSON.parse(saved) : DEFAULT_INPUTS;
  });

  const [predictionResult, setPredictionResult] = useState(() => {
    const saved = localStorage.getItem('hydrogrow_prediction');
    return saved ? JSON.parse(saved) : null;
  });

  // DB-synchronized prediction and conversation histories
  const [savedPredictions, setSavedPredictions] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(() => {
    const saved = localStorage.getItem('hydrogrow_active_conv_id');
    return saved ? parseInt(saved, 10) : null;
  });

  const [chatHistory, setChatHistory] = useState(() => {
    const saved = localStorage.getItem('hydrogrow_chat_history');
    return saved ? JSON.parse(saved) : [];
  });

  const [isPredicting, setIsPredicting] = useState(false);
  const [isChatting, setIsChatting] = useState(false);
  const [predictionError, setPredictionError] = useState(null);
  const [chatError, setChatError] = useState(null);

  // Synchronize localStorage
  useEffect(() => {
    localStorage.setItem('hydrogrow_inputs', JSON.stringify(predictionInputs));
  }, [predictionInputs]);

  useEffect(() => {
    if (predictionResult) {
      localStorage.setItem('hydrogrow_prediction', JSON.stringify(predictionResult));
    } else {
      localStorage.removeItem('hydrogrow_prediction');
    }
  }, [predictionResult]);

  useEffect(() => {
    localStorage.setItem('hydrogrow_chat_history', JSON.stringify(chatHistory));
  }, [chatHistory]);

  useEffect(() => {
    if (activeConversationId) {
      localStorage.setItem('hydrogrow_active_conv_id', activeConversationId.toString());
    } else {
      localStorage.removeItem('hydrogrow_active_conv_id');
    }
  }, [activeConversationId]);

  // Decode username and ID from JWT locally for profile details (future-ready)
  const parseJwt = (t) => {
    try {
      const base64Url = t.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        window
          .atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      return null;
    }
  };

  // Check login validation on load
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        localStorage.setItem('hydrogrow_token', token);
        const payload = parseJwt(token);
        if (payload) {
          setUserProfile({
            id: payload.user_id,
            username: payload.sub,
            email: payload.email || `${payload.sub}@hydrogrow.ai`,
            role: 'Head Grower',
            greenhouseId: 'GH-Alpha-01'
          });
          setIsAuthenticated(true);
        } else {
          // Token corrupted
          logout();
        }
      } else {
        localStorage.removeItem('hydrogrow_token');
        setUserProfile(null);
        setIsAuthenticated(false);
      }
      setAuthLoading(false);
    };
    initAuth();
  }, [token]);

  // Load history records from backend when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchPredictionHistory();
      fetchConversations();
    } else {
      setSavedPredictions([]);
      setConversations([]);
    }
  }, [isAuthenticated]);

  // Helper APIs
  const fetchPredictionHistory = async () => {
    try {
      const res = await client.get('/api/history/predictions');
      setSavedPredictions(res.data);
    } catch (err) {
      console.error('Failed to fetch predictions history:', err);
    }
  };

  const fetchConversations = async () => {
    try {
      const res = await client.get('/api/history/chats');
      setConversations(res.data);
    } catch (err) {
      console.error('Failed to fetch conversations:', err);
    }
  };

  const fetchConversationMessages = async (convId) => {
    setIsChatting(true);
    setChatError(null);
    try {
      const res = await client.get(`/api/history/chats/${convId}`);
      // Map API messages (role, content, sources) to local structure
      const mapped = res.data.map((m) => ({
        id: m.id,
        role: m.role,
        content: m.content,
        sources: m.sources || [],
        timestamp: new Date(m.created_at).toLocaleTimeString()
      }));
      setChatHistory(mapped);
      setActiveConversationId(convId);
    } catch (err) {
      setChatError(err.message || 'Failed to fetch conversation history.');
    } finally {
      setIsChatting(false);
    }
  };

  // Authentications
  const login = async (username, password) => {
    setAuthError(null);
    try {
      const res = await client.post('/api/auth/login', { username, password });
      setToken(res.data.access_token);
      return res.data;
    } catch (err) {
      const msg = err.response?.data?.detail || 'Authentication failed.';
      setAuthError(msg);
      throw new Error(msg);
    }
  };

  const register = async (username, email, password) => {
    setAuthError(null);
    try {
      const res = await client.post('/api/auth/register', { username, email, password });
      return res.data;
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed.';
      setAuthError(msg);
      throw new Error(msg);
    }
  };

  const logout = () => {
    setToken(null);
    setIsAuthenticated(false);
    setUserProfile(null);
    setChatHistory([]);
    setActiveConversationId(null);
    setPredictionResult(null);
    localStorage.removeItem('hydrogrow_token');
    localStorage.removeItem('hydrogrow_prediction');
    localStorage.removeItem('hydrogrow_chat_history');
    localStorage.removeItem('hydrogrow_active_conv_id');
  };

  // Prediction action
  const runPrediction = async (inputs) => {
    setIsPredicting(true);
    setPredictionError(null);
    try {
      setPredictionInputs(inputs);
      const result = await predictGrowth(inputs);
      setPredictionResult(result);
      if (isAuthenticated) {
        fetchPredictionHistory(); // reload history
      }
      return result;
    } catch (err) {
      setPredictionError(err.message || 'An error occurred during prediction.');
      throw err;
    } finally {
      setIsPredicting(false);
    }
  };

  const resetPrediction = () => {
    setPredictionResult(null);
    setPredictionInputs(DEFAULT_INPUTS);
    setPredictionError(null);
  };

  const saveCurrentPrediction = async (label) => {
    const newEntry = {
      id: Date.now(),
      label: label || 'Saved Batch Run',
      timestamp: new Date().toLocaleDateString(),
      predicted_weight: predictionResult?.predicted_yield_grams || 382.7,
      inputs: predictionInputs,
      result: predictionResult
    };
    setSavedPredictions((prev) => [newEntry, ...prev]);
    try {
      if (token) {
        await client.post('/api/history/predictions', newEntry);
      }
    } catch (err) {
      console.warn('API save fallback: Saved locally', err);
    }
  };

  // Helper to extract clean prediction context
  const getContextPayload = () => {
    if (!predictionResult) return {};
    
    return {
      user_inputs: {
        water_ph: predictionInputs.water_ph,
        water_ec: predictionInputs.water_ec,
        water_tds: predictionInputs.water_ec * 0.5,
        water_temperature: predictionInputs.water_temperature,
        air_temperature: predictionInputs.air_temperature,
        humidity: predictionInputs.humidity,
        co2: predictionInputs.co2,
        nutrient_solution_ml: predictionInputs.nutrient_solution,
        water_consumption_l: predictionInputs.water_consumption,
        acid_consumption_ml: 40.0,
        initial_height_cm: predictionInputs.seedling_height,
        initial_weight_g: predictionInputs.seedling_weight,
        initial_root_length_cm: predictionInputs.root_length
      },
      prediction_result: {
        prediction_value: predictionResult.prediction?.predicted_weight,
        growth_category: predictionResult.prediction?.growth_category
      },
      recommendation_outputs: predictionResult.recommendations || [],
      explanation_output: predictionResult.explanation || {}
    };
  };

  // Chat action
  const sendChatMessage = async (text) => {
    if (!text.trim()) return;
    
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setChatHistory((prev) => [...prev, userMsg]);
    setIsChatting(true);
    setChatError(null);

    const assistantMsgId = Date.now() + 1;
    const assistantMsgPlaceholder = {
      id: assistantMsgId,
      role: 'assistant',
      content: '',
      sources: [],
      timestamp: new Date().toLocaleTimeString()
    };
    
    setChatHistory((prev) => [...prev, assistantMsgPlaceholder]);
    
    try {
      const activeContext = getContextPayload();
      const payload = {
        message: text,
        conversation_history: chatHistory.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        context: activeContext,
        conversation_id: activeConversationId
      };

      const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const token = localStorage.getItem('hydrogrow_token');
      const headers = {
        'Content-Type': 'application/json'
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${baseURL}/api/chat/stream`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;
      let accumulatedText = '';
      let resolvedConvId = activeConversationId;
      let resolvedSources = [];

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunkStr = decoder.decode(value, { stream: true });
          const lines = chunkStr.split('\n');
          for (const line of lines) {
            if (line.trim()) {
              try {
                const parsed = JSON.parse(line.trim());
                if (parsed.chunk) {
                  accumulatedText += parsed.chunk;
                }
                if (parsed.conversation_id && !resolvedConvId) {
                  resolvedConvId = parsed.conversation_id;
                }
                if (parsed.sources && parsed.sources.length > 0) {
                  resolvedSources = parsed.sources;
                }
                
                setChatHistory((prev) => 
                  prev.map((msg) => 
                    msg.id === assistantMsgId
                      ? { ...msg, content: accumulatedText, conversation_id: resolvedConvId, sources: resolvedSources }
                      : msg
                  )
                );
              } catch (e) {
                // handle JSON boundaries cut across buffers
              }
            }
          }
        }
      }

      if (resolvedConvId && resolvedConvId !== activeConversationId) {
        setActiveConversationId(resolvedConvId);
        fetchConversations();
      }
    } catch (err) {
      setChatError(err.message || 'An error occurred during communication.');
      setChatHistory((prev) => 
        prev.map((msg) => 
          msg.id === assistantMsgId
            ? { 
                ...msg, 
                content: `⚠️ **Error:** ${err.message || 'Failed to connect to the agricultural intelligence service.'}`,
                isError: true 
              }
            : msg
        )
      );
    } finally {
      setIsChatting(false);
    }
  };

  const createNewThread = async (title) => {
    if (!isAuthenticated) {
      clearChat();
      return;
    }
    try {
      const res = await client.post('/api/history/chats', { title });
      setActiveConversationId(res.data.id);
      setChatHistory([]);
      fetchConversations();
      return res.data;
    } catch (err) {
      console.error('Failed to create new conversation thread:', err);
    }
  };

  const clearChat = () => {
    setChatHistory([]);
    setActiveConversationId(null);
    setChatError(null);
  };

  return (
    <AppContext.Provider value={{
      theme,
      toggleTheme,
      user,
      setUser,
      token,
      userProfile,
      isAuthenticated,
      authError,
      authLoading,
      predictionInputs,
      setPredictionInputs,
      predictionResult,
      chatHistory,
      savedPredictions,
      conversations,
      activeConversationId,
      isPredicting,
      isChatting,
      predictionError,
      chatError,
      login,
      register,
      logout,
      runPrediction,
      resetPrediction,
      saveCurrentPrediction,
      sendChatMessage,
      createNewThread,
      clearChat,
      fetchConversationMessages,
      fetchPredictionHistory
    }}>
      {children}
    </AppContext.Provider>
  );
};
