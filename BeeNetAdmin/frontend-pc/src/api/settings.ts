import request from './request'

export const getSystemSettings = () => request.get('/system/settings/')
export const updateSystemSettings = (data: any) => request.put('/system/settings/', data)
export const getAutoBackup = () => request.get('/system/auto-backup/')
export const updateAutoBackup = (data: any) => request.put('/system/auto-backup/', data)
export const backupNow = () => request.post('/system/backup/')
export const getHealth = () => request.get('/health/')
export const getTextFSMTemplates = () => request.get('/system/templates/textfsm/')
export const getJinja2Templates = () => request.get('/system/templates/jinja2/')
