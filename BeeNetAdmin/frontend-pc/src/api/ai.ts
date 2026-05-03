import request from './request'

export const getAIConfig = () => request.get('/ai/config/')
export const updateAIConfig = (data: any) => request.put('/ai/config/', data)
export const analyzeTerminal = (output: string) => request.post('/ai/analyze/terminal/', { output })
export const aiChat = (message: string) => request.post('/ai/chat/', { message })
