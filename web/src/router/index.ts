import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import DashboardView from '../views/DashboardView.vue';
import EquipmentDetailView from '../views/EquipmentDetailView.vue';
import EquipmentListView from '../views/EquipmentListView.vue';
import LoginView from '../views/auth/LoginView.vue';
import OTPVerificationView from '../views/auth/OTPVerificationView.vue';

const routes: RouteRecordRaw[] = [
  // Public routes
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/verify-otp',
    name: 'otp-verification',
    component: OTPVerificationView,
    meta: { requiresAuth: false }
  },
  
  // Protected routes - Admin Dashboard (default)
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: { 
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/equipos',
    name: 'equipment-list',
    component: EquipmentListView,
    meta: { 
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('../views/UsersView.vue'),
    meta: { 
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/equipment/:id',
    name: 'equipment-detail',
    component: EquipmentDetailView,
    props: true,
    meta: { 
      requiresAuth: true,
      roles: ['admin', 'staff', 'customer']
    }
  },
  
  // Staff Dashboard (TODO: create StaffDashboardView.vue)
  {
    path: '/staff',
    name: 'staff-dashboard',
    component: () => import('../views/StaffDashboardView.vue'),
    meta: { 
      requiresAuth: true,
      roles: ['staff']
    }
  },
  
  // Customer Dashboard (TODO: create CustomerDashboardView.vue)
  {
    path: '/customer',
    name: 'customer-dashboard',
    component: () => import('../views/CustomerDashboardView.vue'),
    meta: { 
      requiresAuth: true,
      roles: ['customer']
    }
  },
  
  // Catch-all redirect
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  console.log('🛣️  Router Guard:', { 
    to: to.name, 
    from: from.name, 
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.currentUser?.email,
    role: authStore.currentUser?.role 
  })
  
  // Restore session from localStorage if not already loaded
  if (!authStore.isAuthenticated && localStorage.getItem('auth_token')) {
    console.log('🔄 Restaurando sesión desde localStorage')
    authStore.restoreSession();
  }
  
  const requiresAuth = to.meta.requiresAuth !== false; // Default to true
  const allowedRoles = to.meta.roles as string[] | undefined;
  
  // Allow access to login and OTP verification pages when not authenticated
  if ((to.name === 'login' || to.name === 'otp-verification') && !authStore.isAuthenticated) {
    console.log('✅ Acceso permitido a página pública')
    next();
    return;
  }
  
  // If route requires auth and user is not authenticated
  if (requiresAuth && !authStore.isAuthenticated) {
    console.log('🚫 No autenticado, redirigiendo a login')
    next({ name: 'login' });
    return;
  }
  
  // If user is authenticated and trying to access login/otp pages, redirect to their dashboard
  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'otp-verification')) {
    console.log('🔄 Usuario ya autenticado, redirigiendo a dashboard')
    const role = authStore.currentUser?.role;
    if (role === 'admin') {
      next({ name: 'dashboard' });
    } else if (role === 'staff') {
      next({ name: 'staff-dashboard' });
    } else if (role === 'customer') {
      next({ name: 'customer-dashboard' });
    } else {
      next({ name: 'dashboard' });
    }
    return;
  }
  
  // Check role-based access
  if (requiresAuth && allowedRoles && allowedRoles.length > 0) {
    if (!authStore.hasRole(allowedRoles)) {
      // Redirect to appropriate dashboard based on user's role
      const role = authStore.currentUser?.role;
      if (role === 'admin') {
        next({ name: 'dashboard' });
      } else if (role === 'staff') {
        next({ name: 'staff-dashboard' });
      } else if (role === 'customer') {
        next({ name: 'customer-dashboard' });
      } else {
        next({ name: 'login' });
      }
      return;
    }
  }
  
  next();
});

export default router;