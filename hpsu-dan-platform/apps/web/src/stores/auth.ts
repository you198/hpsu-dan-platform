import { defineStore } from 'pinia'
import { api, type User } from '../api'

interface LoginResponse { access_token: string; user: User }

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: JSON.parse(localStorage.getItem('user') || 'null') as User | null }),
  actions: {
    async login(username: string, password: string) {
      const result = await api<LoginResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) })
      localStorage.setItem('access_token', result.access_token)
      localStorage.setItem('user', JSON.stringify(result.user))
      this.user = result.user
    },
    logout() {
      localStorage.removeItem('access_token'); localStorage.removeItem('user'); this.user = null
    },
  },
})

