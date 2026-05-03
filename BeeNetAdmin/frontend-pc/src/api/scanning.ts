import request from './request'

export const getScanTasks = () => request.get('/scanning/tasks/')
export const createScanTask = (data: any) => request.post('/scanning/tasks/', data)
export const getScanTask = (id: number) => request.get(`/scanning/tasks/${id}/`)
export const updateScanTask = (id: number, data: any) => request.put(`/scanning/tasks/${id}/`, data)
export const deleteScanTask = (id: number) => request.delete(`/scanning/tasks/${id}/`)
export const runScanTask = (id: number) => request.post(`/scanning/tasks/${id}/run/`)
export const toggleScanTask = (id: number) => request.post(`/scanning/tasks/${id}/toggle/`)
export const getScanResults = (id: number) => request.get(`/scanning/tasks/${id}/results/`)
