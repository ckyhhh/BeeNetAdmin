import request from './request'

export const getDashboardCounts = () => request.get('/dashboard/counts/')
export const getDashboardVendors = () => request.get('/dashboard/vendors/')
export const getRecentInspections = () => request.get('/dashboard/recent-inspections/')
export const getRecentScans = () => request.get('/dashboard/recent-scans/')
export const getAliveAlerts = () => request.get('/dashboard/alive-alerts/')
export const getNotifications = () => request.get('/dashboard/notifications/')
