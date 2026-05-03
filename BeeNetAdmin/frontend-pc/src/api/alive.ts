import request from './request'

export const getAliveTasks = () => request.get('/alive/tasks/')
export const createAliveTask = (data: any) => request.post('/alive/tasks/', data)
export const getAliveTask = (id: number) => request.get(`/alive/tasks/${id}/`)
export const updateAliveTask = (id: number, data: any) => request.put(`/alive/tasks/${id}/`, data)
export const deleteAliveTask = (id: number) => request.delete(`/alive/tasks/${id}/`)
export const runAliveTask = (id: number) => request.post(`/alive/tasks/${id}/run/`)
export const toggleAliveTask = (id: number) => request.post(`/alive/tasks/${id}/toggle/`)
export const getAliveResults = (id: number) => request.get(`/alive/tasks/${id}/results/`)
export const getAliveStatus = (id: number) => request.get(`/alive/tasks/${id}/status/`)
