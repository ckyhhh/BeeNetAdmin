import request from './request'

export const getInstantHistory = () => request.get('/terminal/instant/history/')
export const deleteInstantHistory = (id: number) => request.delete(`/terminal/instant/history/${id}/`)
export const getInstantLog = (id: number) => request.get(`/terminal/instant/${id}/log/`)
