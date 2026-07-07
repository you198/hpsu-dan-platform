import { createRouter, createWebHistory } from 'vue-router';
import LoginView from './views/LoginView.vue';
import AppShell from './views/AppShell.vue';
const DashboardView = () => import('./views/DashboardView.vue');
const DigitalTwinView = () => import('./views/VisitorTwinView.vue');
const DiagnosisView = () => import('./views/VisitorDiagnosisView.vue');
const ResultsView = () => import('./views/ResultsView.vue');
const AnalysisView = () => import('./views/AnalysisView.vue');
const SystemView = () => import('./views/SystemView.vue');
export const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/login', component: LoginView },
        { path: '/', component: AppShell, children: [
                { path: '', redirect: '/dashboard' },
                { path: 'dashboard', component: DashboardView },
                { path: 'digital-twin', component: DigitalTwinView },
                { path: 'diagnosis', component: DiagnosisView },
                { path: 'results', component: ResultsView },
                { path: 'analysis', component: AnalysisView },
                { path: 'system', component: SystemView, meta: { role: 'admin' } },
            ] },
    ],
});
router.beforeEach((to) => {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    if (to.path !== '/login' && !token)
        return '/login';
    if (to.path === '/login' && token)
        return '/dashboard';
    if (to.meta.role && user?.role !== to.meta.role)
        return '/dashboard';
});
