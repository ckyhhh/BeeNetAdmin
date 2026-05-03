import request from './request'

export const login = (data: { username: string; password: string }) =>
  request.post('/auth/login/', data)

export const setup = (data: { username: string; password: string }) =>
  request.post('/setup/', data)

export const getSetupStatus = () => request.get('/setup/status/')

export const getMe = () => request.get('/auth/me/')

export const changePassword = (data: { old_password: string; new_password: string }) =>
  request.put('/auth/password/', data)

export const unlock = (master_password: string) =>
  request.post('/auth/unlock/', { master_password })

export const lock = () => request.post('/auth/lock/')
