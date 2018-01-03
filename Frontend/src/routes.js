import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import LibraryBook from './views/nav1/LibraryBook.vue'
import SexGrade from './views/nav1/SexGrade.vue'
import BorrowReturn from './views/nav1/BRInfo.vue'
import MarkDown from './views/nav2/MarkDown.vue'
import echarts from './views/charts/echarts.vue'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/',
        component: Home,
        name: '数据面板',
        iconCls: 'fa fa-bar-chart',
        leaf: true,
        children: [
            { path: '/', component: echarts, name: '数据面板', hidden: true},
            // { path: '/echarts', component: echarts, name: '面板' }
        ]
    },
    {
        path: '/moreCharts',
        component: Home,
        name: '各种图表',
        iconCls: 'fa fa fa-cube',//图标样式class
        children: [
            { path: '/sexGrade', component: SexGrade, name: '性别和年级的对比' },
            { path: '/brinfo', component: BorrowReturn, name: '借阅及归还情况对比' },
            { path: '/libinfo', component: LibraryBook, name: '图书馆和图书的相关情况' },
        ]
    },
    {
        path: '/edit',
        component: Home,
        name: '笔记',
        iconCls: 'fa fa-pencil-square-o',
        children: [
            { path: '/markdown', component: MarkDown, name: 'MarkDown' }
        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;