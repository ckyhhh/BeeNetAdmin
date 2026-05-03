import request from './request'

export const getInspectionTemplates = () => request.get('/inspection/templates/')
export const createInspectionTemplate = (data: any) => request.post('/inspection/templates/', data)
export const getInspectionTemplate = (id: number) => request.get(`/inspection/templates/${id}/`)
export const updateInspectionTemplate = (id: number, data: any) => request.put(`/inspection/templates/${id}/`, data)
export const deleteInspectionTemplate = (id: number) => request.delete(`/inspection/templates/${id}/`)
export const cloneInspectionTemplate = (id: number) => request.post(`/inspection/templates/${id}/clone/`)

export const getInspectionTasks = () => request.get('/inspection/tasks/')
export const createInspectionTask = (data: any) => request.post('/inspection/tasks/', data)
export const getInspectionTask = (id: number) => request.get(`/inspection/tasks/${id}/`)
export const updateInspectionTask = (id: number, data: any) => request.put(`/inspection/tasks/${id}/`, data)
export const deleteInspectionTask = (id: number) => request.delete(`/inspection/tasks/${id}/`)
export const runInspectionTask = (id: number) => request.post(`/inspection/tasks/${id}/run/`)
export const toggleInspectionTask = (id: number) => request.post(`/inspection/tasks/${id}/toggle/`)
export const getInspectionResults = (id: number) => request.get(`/inspection/tasks/${id}/results/`)
export const getInspectionResult = (id: number) => request.get(`/inspection/results/${id}/`)
export const getInspectionReport = (id: number) => request.get(`/inspection/results/${id}/report/`)
