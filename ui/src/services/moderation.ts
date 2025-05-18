import axiosInstance from './interceptor.ts';
import endpoints from './endpoints.ts';

// Fetch the list of pending moderation content
const listPendingContent = async () => {
  const response = await axiosInstance.get(endpoints.moderation.listPending);
  return response.data;
};

// Fetch analysis for a single piece of content by contentId
const getContentAnalysis = async (contentId: string) => {
  const response = await axiosInstance.get(endpoints.moderation.getContentAnalysis(contentId));
  return response.data;
};

// Approve a piece of content by contentId
const approveContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.approveContent(contentId));
  return response.data;
};

// Reject a piece of content by contentId
const rejectContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.rejectContent(contentId));
  return response.data;
};

// Flag content manually by contentId
const flagContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.flagContent(contentId));
  return response.data;
};

export { listPendingContent, getContentAnalysis, approveContent, rejectContent, flagContent };
