import { defineStore } from 'pinia';
import { api } from '../api';
export const useAuthStore = defineStore('auth', {
    state: () => ({ user: JSON.parse(localStorage.getItem('user') || 'null') }),
    actions: {
        async login(username, password) {
            const result = await api('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) });
            localStorage.setItem('access_token', result.access_token);
            localStorage.setItem('user', JSON.stringify(result.user));
            this.user = result.user;
        },
        logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            this.user = null;
        },
    },
});
