import request from './request'

export const getNotifications = (params?: any) => request.get('/notifications/', { params })
export const markNotificationRead = (id: number) => request.put(`/notifications/${id}/read/`)
export const markAllRead = () => request.post('/notifications/read-all/')
export const getEmailConfig = () => request.get('/notifications/email-config/')
export const updateEmailConfig = (data: any) => request.put('/notifications/email-config/', data)
export const testEmail = () => request.post('/notifications/email-config/test/')
