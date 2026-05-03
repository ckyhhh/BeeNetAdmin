import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const user = ref<any>(null)

  async function login(username: string, password: string) {
    const data: any = await authApi.login({ username, password })
    token.value = data.access
    user.value = data.user
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function fetchUser() {
    try {
      user.value = await authApi.getMe()
    } catch {
      logout()
    }
  }

  return { token, user, login, logout, fetchUser }
})
