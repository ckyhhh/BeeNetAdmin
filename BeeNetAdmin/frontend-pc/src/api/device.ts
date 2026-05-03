import request from './request'

// 设备
export const getDevices = (params?: any) => request.get('/devices/', { params })
export const getDevice = (id: number) => request.get(`/devices/${id}/`)
export const createDevice = (data: any) => request.post('/devices/', data)
export const updateDevice = (id: number, data: any) => request.put(`/devices/${id}/`, data)
export const deleteDevice = (id: number) => request.delete(`/devices/${id}/`)
export const testDevice = (id: number) => request.post(`/devices/${id}/test/`)
export const collectDevice = (id: number) => request.post(`/devices/${id}/collect/`)
export const getDeviceInfo = (id: number) => request.get(`/devices/${id}/info/`)
export const getRunningConfig = (id: number) => request.get(`/devices/${id}/config/running/`)
export const getStartupConfig = (id: number) => request.get(`/devices/${id}/config/startup/`)
export const backupConfig = (id: number) => request.post(`/devices/${id}/config/backup/`)
export const getConfigDiff = (id: number) => request.get(`/devices/${id}/config/diff/`)
export const exportDevices = (data: any) => request.post('/devices/export/', data)
export const batchDeleteDevices = (ids: number[]) => request.post('/devices/batch_delete/', { ids })

// 设备组
export const getDeviceGroups = () => request.get('/device-groups/')
export const createDeviceGroup = (data: any) => request.post('/device-groups/', data)
export const updateDeviceGroup = (id: number, data: any) => request.put(`/device-groups/${id}/`, data)
export const deleteDeviceGroup = (id: number) => request.delete(`/device-groups/${id}/`)

// 凭据
export const getCredentials = () => request.get('/credentials/')
export const createCredential = (data: any) => request.post('/credentials/', data)
export const updateCredential = (id: number, data: any) => request.put(`/credentials/${id}/`, data)
export const deleteCredential = (id: number) => request.delete(`/credentials/${id}/`)
