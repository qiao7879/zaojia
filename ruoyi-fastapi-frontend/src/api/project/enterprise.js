import request from '@/utils/request'

// 查询菜单列表
export function listEnt(query) {
  return request({
    url: '/project/ent/list',
    method: 'get',
    params: query
  })
}

// 查询菜单详细
export function getEnt(entId) {
  return request({
    url: '/project/ent/' + entId,
    method: 'get'
  })
}


// 新增菜单
export function addEnt(data) {
  return request({
    url: '/project/ent',
    method: 'post',
    data: data
  })
}

// 修改菜单
export function updateEnt(data) {
  return request({
    url: '/project/ent',
    method: 'put',
    data: data
  })
}

// 删除菜单
export function delEnt(entId) {
  return request({
    url: '/project/ent/' + entId,
    method: 'delete'
  })
}