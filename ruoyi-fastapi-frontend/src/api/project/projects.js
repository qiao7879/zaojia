import request from '@/utils/request'

// 查询菜单列表
export function listProject(query) {
  return request({
    url: '/system/project/list',
    method: 'get',
    params: query
  })
}

// 查询菜单详细
export function getProject(ProjectId) {
  return request({
    url: '/system/project/' + ProjectId,
    method: 'get'
  })
}


// 新增菜单
export function addProject(data) {
  return request({
    url: '/system/project',
    method: 'post',
    data: data
  })
}

// 修改菜单
export function updateProject(data) {
  return request({
    url: '/system/project/',
    method: 'put',
    data: data
  })
}

// 删除菜单
export function delProject(ProjectId) {
  return request({
    url: '/system/project/' + ProjectId,
    method: 'delete'
  })
}

export function secondReviewProject(data) {
  return request({
    url: '/system/project/prefect/second-review',
    method: 'put',
    data
  })
}

export function secondReviewProjectBatch(data) {
  return request({
    url: '/system/project/prefect/second-review/batch',
    method: 'put',
    data
  })
}

export function thirdReviewProject(data) {
  return request({
    url: '/system/project/prefect/third-review',
    method: 'put',
    data
  })
}

export function thirdReviewProjectBatch(data) {
  return request({
    url: '/system/project/prefect/third-review/batch',
    method: 'put',
    data
  })
}
