import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import VueRouter from 'vue-router'
import store from './vuex/store'
import Vuex from 'vuex'
import routes from './routes'
import Mock from './mock'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

import '../static/css/bootstrap.min.css'
import 'font-awesome/css/font-awesome.min.css'
import 'admin-lte/dist/css/AdminLTE.min.css'
import 'admin-lte/dist/css/skins/_all-skins.min.css'

Mock.login();

Vue.use(ElementUI);
Vue.use(VueRouter);
Vue.use(Vuex);

NProgress.inc();
NProgress.configure({ easing: 'ease', speed: 500, showSpinner: false });

const router = new VueRouter({
    mode: 'history',
    routes
});

// 暂时去除登录页面(2018-01-02)
// router.beforeEach((to, from, next) => {
//     if (to.path === '/login') {
//         sessionStorage.removeItem('user');
//     }
//     let user = JSON.parse(sessionStorage.getItem('user'));
//     if (!user && to.path !== '/login') {
//         next({ path: '/login' })
//     } else {
//         NProgress.start();
//         next()
//     }
// });

router.afterEach(transition => {
    NProgress.done();
});

new Vue({
  //el: '#app',
  //template: '<App/>',
  router,
  store,
  //components: { App }
  render: h => h(App)
}).$mount('#app');

