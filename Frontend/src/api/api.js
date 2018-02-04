import axios from 'axios';

let base = '';

let my_router = axios.create({
    baseURL: '/v1'
});

// 自带的登陆接口(之后扩展)
export const requestLogin = params => { return axios.post(`${base}/login`, params).then(res => res.data); };

// Markdown的接口(发布Markdown和获取一个或多个markdown)
export const postMarkdown = params => {
    return my_router.post(`/article/postArticle`, { params: params }).then(res => res.data)
};

export const get_one = params => {
    return my_router.get(`/article/getArticle`, { params: params }).then(res => res.data)
};

export const get_article_list = params => {
    return my_router.get(`/article/getAll`, { params: params }).then(res => res.data)
};

// 获取后端封装好的echarts的画图json
export const getLibraryBorrowPeopleType = params => {
    return my_router.get(`/charts/dif_people`, { params: params }).then(res => res.data)
};

export const getGzccTop15 = params => {
    return my_router.get(`/charts/gzcc_top`, { params: params }).then(res => res.data)
};

export const getKdTop15 = params => {
    return my_router.get(`/charts/kd_top`, { params: params }).then(res => res.data)
};

export const getGzccDifFaculty = params => {
    return my_router.get(`/charts/gzcc_faculty`, { params: params }).then(res => res.data)
};

export const getKdDifFaculty = params => {
    return my_router.get(`/charts/kd_faculty`, { params: params }).then(res => res.data)
};

export const getSexData = params => {
    return my_router.get(`/charts/sex`, { params: params }).then(res => res.data)
};

export const getDuplicateSexData = params => {
    return my_router.get(`/charts/sex_1`, { params: params }).then(res => res.data)
};

export const getGradeData = params => {
    return my_router.get(`/charts/grade`, { params: params }).then(res => res.data)
};

export const getBRMonthInfo = params => {
    return my_router.get(`/charts/br_months`, { params: params }).then(res => res.data)
};

export const getBRWeekInfo = params => {
    return my_router.get(`/charts/br_weekdays`, { params: params }).then(res => res.data)
};

export const getBRQuantumInfo = params => {
    return my_router.get(`/charts/br_quantum`, { params: params }).then(res => res.data)
};

export const getLibDifFloor = params => {
    return my_router.get(`/charts/dif_floor`, { params: params }).then(res => res.data)
};

export const getPublishAuthor = params => {
    return my_router.get(`/charts/p_a`, { params: params }).then(res => res.data)
};

export const getFacultySex = params => {
    return my_router.get(`/charts/faculty_sex`, { params: params }).then(res => res.data)
};