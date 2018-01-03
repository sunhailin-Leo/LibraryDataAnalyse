import axios from 'axios';

let base = '';

let my_router = axios.create({
    baseURL: '/v1'
});

export const requestLogin = params => { return axios.post(`${base}/login`, params).then(res => res.data); };

// export const getUserList = params => { return axios.get(`${base}/user/list`, { params: params }); };

// export const getUserListPage = params => { return axios.get(`${base}/user/listpage`, { params: params }); };

// export const removeUser = params => { return axios.get(`${base}/user/remove`, { params: params }); };

// export const batchRemoveUser = params => { return axios.get(`${base}/user/batchremove`, { params: params }); };

// export const editUser = params => { return axios.get(`${base}/user/edit`, { params: params }); };

// export const addUser = params => { return axios.get(`${base}/user/add`, { params: params }); };


// 获取信息
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