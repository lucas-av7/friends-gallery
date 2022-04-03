export const TOKEN_KEY = "user_token";
export const USER_ID = "user_id";

export const isAuthenticated = () => localStorage.getItem(TOKEN_KEY) !== null;
export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const getUserId = () => localStorage.getItem(USER_ID);

export const login = (userId, token) => {
  localStorage.setItem(USER_ID, userId);
  localStorage.setItem(TOKEN_KEY, token);
};

export const logout = () => {
  localStorage.removeItem(USER_ID);
  localStorage.removeItem(TOKEN_KEY);
};
