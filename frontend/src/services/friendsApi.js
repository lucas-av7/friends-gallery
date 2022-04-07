import axios from "axios";
import { getToken } from "./auth";

const instance = axios.create({
  baseURL: "http://localhost:5500/api/",
  headers: { "Content-Type": "application/json" },
});

instance.interceptors.request.use(async (config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const createAdminUser = ({ name, email, password, secret_key }) => {
  return instance.post("users", { name, email, password, secret_key });
};

export const createUser = ({ name, email, password }) => {
  return instance.post("users", { name, email, password });
};

export const deleteUser = (id) => {
  return instance.delete(`users/${id}`);
};

export const getUser = (id) => {
  return instance.get(`users/${id}`);
};

export const loginUser = ({ email, password }) => {
  return instance.post(
    "auth/login",
    {},
    {
      withCredentials: true,
      auth: {
        username: email,
        password: password,
      },
    }
  );
};

export const sendPhoto = ({ title, base64_img }) => {
  return instance.post("photos", { title, base64_img });
};

export const getPhotos = () => {
  return instance.get("photos");
};

export const getPendingPhotos = () => {
  return instance.get("photos/pending-photos");
};

export const getPhoto = (photoId) => {
  return instance.get(`photos/${photoId}`);
};

export const deletePhoto = (photoId) => {
  return instance.delete(`photos/${photoId}`);
};

export const approvePhoto = (photoId) => {
  return instance.post(`photos/${photoId}/approve`);
};

export const likePhoto = (photoId) => {
  return instance.post(`photos/${photoId}/like`);
};

export const sendComment = (photoId, content) => {
  return instance.post(`comments/${photoId}/`, { content });
};

export const likeComment = (commentId) => {
  return instance.post(`comments/${commentId}/like`);
};

export const deleteComment = (commentId) => {
  return instance.delete(`comments/${commentId}`);
};
